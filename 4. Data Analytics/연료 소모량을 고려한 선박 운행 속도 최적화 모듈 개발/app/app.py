# app.py
"""
선박 운행 속도 최적화 API 서버
Ship Route Optimization API Server
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import requests
import os
import csv
import logging
from typing import Dict, Any, Optional, Tuple

from inference.main_inference import run_once
from flasgger import Swagger
# ================================================================
# 설정 및 초기화
# ================================================================
app = Flask(__name__)

swagger_config = Swagger.DEFAULT_CONFIG
swagger_config.update({
    "headers": [],
    "specs": [
        {
            "endpoint": "openapi",
            "route": "/docs/openapi.json",
            # /api 로 시작하는 것만 노출 (레거시 제외)
            "rule_filter": lambda rule: rule.rule.startswith("/api/"),
            "model_filter": lambda tag: True,
        }
    ],
    "swagger_ui": True,
    "specs_route": "/docs/",
    "static_url_path": "/flasgger_static",

    # UI 정적파일을 CDN에서 로드 (로컬 /static 404 방지)
    "swagger_ui_bundle_js": "//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js",
    "swagger_ui_standalone_preset_js": "//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js",
    "swagger_ui_css": "//unpkg.com/swagger-ui-dist@3/swagger-ui.css",
    "jquery_js": "//unpkg.com/jquery@3/dist/jquery.min.js",
})

Swagger(app, config=swagger_config)

CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # 캐시 방지

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API 정보
API_INFO = {
    'name': 'Ship Route Optimization API',
    'version': '1.0.0',
    'last_modified': '2024-12-17',
    'description': '선박 접안 경로 최적화 및 기상 정보 제공 API'
}

# 환경변수
KMA_API_KEY = os.environ.get("KMA_API_KEY")
if not KMA_API_KEY:
    logger.warning("KMA_API_KEY 환경변수가 설정되지 않았습니다. CSV fallback만 사용됩니다.")

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, '..', 'data', 'OBS_BUOY_TIM_20251111222621.csv')

# 기상청 API 설정
KMA_URL = "https://apihub.kma.go.kr/api/typ01/url/sea_obs.php"
KMA_STATION = "22104"

# 모델 설정
DEFAULT_MODEL_IDX = 0
GRID_SIZE = 15
MAX_STEPS = 50

# 그리드 변환 설정 (부산항 주변)
LAT_MIN, LAT_MAX = 35.0, 35.3
LON_MIN, LON_MAX = 129.0, 129.3

# ================================================================
# 유틸리티 함수
# ================================================================

def latlon_to_grid(lat: float, lon: float) -> Tuple[int, int]:
    """
    위경도를 그리드 좌표로 변환
    
    Args:
        lat: 위도
        lon: 경도
    
    Returns:
        (grid_i, grid_j): 그리드 좌표
    """
    grid_i = int((LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * (GRID_SIZE - 1))
    grid_j = int((lon - LON_MIN) / (LON_MAX - LON_MIN) * (GRID_SIZE - 1))
    
    # 범위 제한
    grid_i = max(0, min(GRID_SIZE - 1, grid_i))
    grid_j = max(0, min(GRID_SIZE - 1, grid_j))
    
    return grid_i, grid_j


def grid_to_latlon(grid_i: int, grid_j: int) -> Tuple[float, float]:
    """
    그리드 좌표를 위경도로 역변환
    
    Args:
        grid_i: 그리드 i 좌표
        grid_j: 그리드 j 좌표
    
    Returns:
        (lat, lon): 위경도
    """
    lat = LAT_MAX - (grid_i / (GRID_SIZE - 1)) * (LAT_MAX - LAT_MIN)
    lon = LON_MIN + (grid_j / (GRID_SIZE - 1)) * (LON_MAX - LON_MIN)
    return round(lat, 6), round(lon, 6)


def load_wind_from_csv(dt: datetime) -> Optional[Tuple[float, float]]:
    """
    CSV 파일에서 바람 데이터 로드
    
    Args:
        dt: 조회할 시간
    
    Returns:
        (wind_dir, wind_spd): 풍향(도), 풍속(m/s) 또는 None
    """
    target = f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d} {dt.hour}:{dt.minute:02d}"
    
    try:
        with open(CSV_PATH, encoding='cp949') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('일시') == target:
                    wind_dir = float(row.get('wind_dir'))
                    wind_spd = float(row.get('wind_spd'))
                    logger.info(f"CSV 데이터 로드 성공: {wind_dir}° {wind_spd}m/s")
                    return wind_dir, wind_spd
    except FileNotFoundError:
        logger.error(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}")
    except Exception as e:
        logger.error(f"CSV 읽기 오류: {e}")
    
    return None


def fetch_wind_data(target_datetime: datetime) -> Optional[Dict[str, Any]]:
    """
    기상청 API 또는 CSV에서 바람 데이터 조회
    
    Args:
        target_datetime: 조회할 시간
    
    Returns:
        바람 데이터 딕셔너리 또는 None
    """
    tm = target_datetime.strftime('%Y%m%d%H%M')
    
    # 1차: 기상청 API 시도
    if KMA_API_KEY:
        try:
            params = {
                'tm': tm,
                'stn': KMA_STATION,
                'authKey': KMA_API_KEY,
                'help': '0'
            }
            res = requests.get(KMA_URL, params=params, timeout=3)
            res.raise_for_status()
            
            if res.text.strip():
                lines = [line.strip() for line in res.text.splitlines() if line.startswith('B,')]
                if lines:
                    parts = [x.strip() for x in lines[0].split(',')]
                    wind_dir = float(parts[7])
                    wind_spd = float(parts[8])
                    logger.info(f"기상청 API 성공: {wind_dir}° {wind_spd}m/s")
                    return {
                        'source': 'kma_api',
                        'wind_dir_deg': wind_dir,
                        'wind_spd_ms': wind_spd,
                        'timestamp': tm
                    }
        except Exception as e:
            logger.warning(f"기상청 API 오류: {e}")
    
    # 2차: CSV Fallback
    fallback = load_wind_from_csv(target_datetime)
    if fallback:
        wind_dir, wind_spd = fallback
        return {
            'source': 'csv',
            'wind_dir_deg': wind_dir,
            'wind_spd_ms': wind_spd,
            'timestamp': tm
        }
    
    return None


def deg_to_direction_kr(deg: float) -> str:
    """각도를 16방위 한국어로 변환"""
    dirs = ['북', '북북동', '북동', '동북동', '동', '동남동', '남동', '남남동',
            '남', '남남서', '남서', '서남서', '서', '서북서', '북서', '북북서']
    ix = int((deg + 11.25) / 22.5) % 16
    return dirs[ix]


def deg_to_direction_en(deg: float) -> str:
    """각도를 8방위 영어로 변환"""
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    ix = int((deg + 22.5) / 45) % 8
    return dirs[ix]


def ms_to_knots(ms: float) -> float:
    """m/s를 노트로 변환"""
    return round(ms * 1.94384, 2)


def format_guidance_steps(
    result: Dict[str, Any],
    start_grid_i: int,
    start_grid_j: int,
    start_datetime: datetime
) -> list:
    """
    시뮬레이션 결과를 시점별 가이던스로 포맷팅
    
    Args:
        result: run_once의 결과
        start_grid_i: 시작 그리드 i 좌표
        start_grid_j: 시작 그리드 j 좌표
        start_datetime: 출발 시간
    
    Returns:
        시점별 가이던스 리스트
    """
    steps = []
    num_steps = len(result.get('rec_speed_list', []))
    
    # 방향 인덱스 → 그리드 이동 매핑
    # 0: N, 1: NE, 2: E, 3: SE, 4: S, 5: SW, 6: W, 7: NW
    dir_map = {
        0: (-1, 0),   # N
        1: (-1, 1),   # NE
        2: (0, 1),    # E
        3: (1, 1),    # SE
        4: (1, 0),    # S
        5: (1, -1),   # SW
        6: (0, -1),   # W
        7: (-1, -1)   # NW
    }
    
    # 현재 위치 추적
    current_i = start_grid_i
    current_j = start_grid_j
    
    # 초기 ETA (첫 번째 스텝의 ETA)
    initial_eta = result['eta_history'][0] if result.get('eta_history') else 0
    
    for i in range(num_steps):
        # 경과 시간 계산
        eta_remaining = result['eta_history'][i] if i < len(result['eta_history']) else 0
        elapsed_minutes = initial_eta - eta_remaining
        
        # 실제 시점 계산
        actual_time = start_datetime + timedelta(minutes=elapsed_minutes)
        
        # 현재 위치의 위경도 변환
        lat, lon = grid_to_latlon(current_i, current_j)
        
        step = {
            'step': i + 1,
            'timestamp': actual_time.isoformat(),
            'time_display': actual_time.strftime('%Y-%m-%d %H:%M:%S'),
            'position': {
                'grid': {
                    'i': current_i,
                    'j': current_j
                },
                'coordinates': {
                    'latitude': lat,
                    'longitude': lon
                }
            },
            'heading': {
                'intended': result['intended_dir_idx'][i] if i < len(result['intended_dir_idx']) else None,
                'actual': result['dir_idx'][i] if i < len(result['dir_idx']) else None
            },
            'speed': {
                'recommended_knots': result['rec_speed_list'][i] if i < len(result['rec_speed_list']) else None
            },
            'eta': {
                'elapsed_minutes': round(elapsed_minutes, 2),
                'remaining_minutes': round(eta_remaining, 2)
            }
        }
        steps.append(step)
        
        # 다음 위치로 이동 (실제 방향 사용)
        if i < len(result['dir_idx']) and result['dir_idx'][i] is not None:
            actual_dir = result['dir_idx'][i]
            if actual_dir in dir_map:
                di, dj = dir_map[actual_dir]
                current_i += di
                current_j += dj
                # 그리드 범위 제한
                current_i = max(0, min(GRID_SIZE - 1, current_i))
                current_j = max(0, min(GRID_SIZE - 1, current_j))
    
    return steps


# ================================================================
# 웹 인터페이스 라우트
# ================================================================

@app.route('/')
def index():
    """메인 웹 페이지"""
    return render_template('index.html')


# ================================================================
# 레거시 API 엔드포인트 (HTML 호환성)
# ================================================================

@app.route('/wind', methods=['GET'])
def wind_legacy():
    """
    바람 데이터 조회 (레거시 - HTML 호환용)
    
    Query Parameters:
        datetime: ISO 8601 형식 또는 사용자 정의 형식
    
    Returns:
        레거시 형식의 바람 정보
    """
    user_datetime = request.args.get('datetime')
    if not user_datetime:
        return jsonify({'error': 'datetime required'}), 400

    try:
        dt = datetime.fromisoformat(user_datetime.replace('Z', '+00:00'))
    except Exception:
        return jsonify({'error': '잘못된 datetime 형식입니다.'}), 400

    wind_data = fetch_wind_data(dt)
    if not wind_data:
        return jsonify({'error': '바람 데이터를 조회할 수 없습니다'}), 500
    
    # 레거시 형식으로 응답
    return jsonify({
        'dir': wind_data['wind_dir_deg'],
        'dir8': deg_to_direction_kr(wind_data['wind_dir_deg']),
        'speed': wind_data['wind_spd_ms'],
        'tm': wind_data['timestamp']
    })


@app.route('/simulate', methods=['POST'])
def simulate_legacy():
    """
    시뮬레이션 실행 (레거시 - HTML 호환용)
    
    Request Body:
    {
        "grid_i": int,
        "grid_j": int,
        "wind_dir": float,
        "wind_speed": float
    }
    
    Returns:
        run_once 결과를 그대로 반환
    """
    data = request.get_json() or {}
    
    try:
        grid_i = int(data['grid_i'])
        grid_j = int(data['grid_j'])
        wind_dir = float(data['wind_dir'])      # degrees
        wind_speed = float(data['wind_speed'])  # m/s
    except Exception:
        return jsonify({'error': 'invalid payload'}), 400

    try:
        result = run_once(
            grid_i=grid_i,
            grid_j=grid_j,
            wind_dir_deg=wind_dir,
            wind_speed_ms=wind_speed,
            model_idx=DEFAULT_MODEL_IDX,
            size=GRID_SIZE,
            max_steps=MAX_STEPS
        )
        return jsonify(result)
    except Exception as e:
        logger.error(f"시뮬레이션 오류: {e}")
        return jsonify({'error': 'inference failed'}), 500


# ================================================================
# 신규 API 엔드포인트
# ================================================================

@app.route('/api/info', methods=['GET'])
def api_info():
    """
    API 정보 조회
    ---
    tags:
      - Meta
    produces:
      - application/json
    responses:
      200:
        description: "API 메타데이터 및 엔드포인트 목록"
        schema:
          type: object
          properties:
            name:
              type: string
            version:
              type: string
            last_modified:
              type: string
            description:
              type: string
            endpoints:
              type: object
              additionalProperties: true
    """
    return jsonify({
        'name': API_INFO['name'],
        'version': API_INFO['version'],
        'last_modified': API_INFO['last_modified'],
        'description': API_INFO['description'],
        'endpoints': {
            'info': {
                'path': '/api/info',
                'method': 'GET',
                'description': 'API 정보 조회'
            },
            'health': {
                'path': '/api/health',
                'method': 'GET',
                'description': '서버 상태 확인'
            },
            'wind': {
                'path': '/api/wind',
                'method': 'GET',
                'description': '바람 데이터 조회',
                'parameters': {
                    'datetime': 'ISO 8601 형식'
                }
            },
            'guidance': {
                'path': '/api/guidance',
                'method': 'POST',
                'description': '접안 가이던스 생성',
                'body': {
                    'start_time': 'ISO 8601 형식',
                    'start_position': {
                        'latitude': 'float',
                        'longitude': 'float'
                    }
                }
            }
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    헬스 체크
    ---
    tags:
      - Meta
    produces:
      - application/json
    responses:
      200:
        description: "서버 상태 및 설정 정보"
        schema:
          type: object
          properties:
            status:
              type: string
            timestamp:
              type: string
            config:
              type: object
              properties:
                model_loaded:
                  type: boolean
                grid_size:
                  type: string
                max_steps:
                  type: integer
                kma_api_configured:
                  type: boolean
                csv_fallback_available:
                  type: boolean
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'config': {
            'model_loaded': True,
            'grid_size': f"{GRID_SIZE}x{GRID_SIZE}",
            'max_steps': MAX_STEPS,
            'kma_api_configured': bool(KMA_API_KEY),
            'csv_fallback_available': os.path.exists(CSV_PATH)
        }
    })


@app.route('/api/wind', methods=['GET'])
def get_wind():
    """
    바람 데이터 조회
    ---
    tags:
      - Weather
    produces:
      - application/json
    parameters:
      - name: datetime
        in: query
        type: string
        required: true
        description: "ISO 8601 형식 (예시 2025-12-17T01:00:00)"
    responses:
      200:
        description: "바람 정보(방향/속도/출처)"
        schema:
          type: object
          properties:
            timestamp:
              type: string
            wind:
              type: object
              properties:
                direction:
                  type: object
                  properties:
                    degrees:
                      type: number
                    cardinal_kr:
                      type: string
                    cardinal_en:
                      type: string
                speed:
                  type: object
                  properties:
                    ms:
                      type: number
                    knots:
                      type: number
            source:
              type: string
      400:
        description: "잘못된 요청(파라미터 누락/형식 오류)"
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: "바람 데이터 조회 실패"
        schema:
          type: object
          properties:
            error:
              type: string
    """
    datetime_str = request.args.get('datetime')
    if not datetime_str:
        return jsonify({'error': 'datetime 파라미터가 필요합니다'}), 400
    
    try:
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
    except Exception:
        return jsonify({'error': '잘못된 datetime 형식입니다. ISO 8601 형식을 사용하세요.'}), 400
    
    wind_data = fetch_wind_data(dt)
    if not wind_data:
        return jsonify({'error': '바람 데이터를 조회할 수 없습니다'}), 500
    
    return jsonify({
        'timestamp': wind_data['timestamp'],
        'wind': {
            'direction': {
                'degrees': wind_data['wind_dir_deg'],
                'cardinal_kr': deg_to_direction_kr(wind_data['wind_dir_deg']),
                'cardinal_en': deg_to_direction_en(wind_data['wind_dir_deg'])
            },
            'speed': {
                'ms': wind_data['wind_spd_ms'],
                'knots': ms_to_knots(wind_data['wind_spd_ms'])
            }
        },
        'source': wind_data['source']
    })


@app.route('/api/guidance', methods=['POST'])
def generate_guidance():
    """
    접안 가이던스 생성
    ---
    tags:
      - Guidance
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        description: "ISO 8601 형식 (예시 2025-12-17T01:00:00)"
        schema:
          type: object
          required:
            - start_time
            - start_position
          properties:
            start_time:
              type: string
              description: "ISO 8601 형식 (예시 2025-12-17T01:00:00)"
            start_position:
              type: object
              required:
                - latitude
                - longitude
              properties:
                latitude:
                  type: number
                longitude:
                  type: number
    responses:
      200:
        description: "접안 가이던스 및 시뮬레이션 결과"
        schema:
          type: object
          properties:
            request:
              type: object
            weather:
              type: object
            guidance:
              type: object
            simulation:
              type: object
      400:
        description: "잘못된 요청(본문 누락/필수 값 누락/형식 오류/좌표 범위 오류)"
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: "서버 오류(바람 조회 실패/모델 추론 실패)"
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': '요청 본문이 필요합니다'}), 400
    
    # 필수 파라미터 검증
    start_time_str = data.get('start_time')
    start_position = data.get('start_position')
    
    if not start_time_str or not start_position:
        return jsonify({'error': 'start_time과 start_position이 필요합니다'}), 400
    
    try:
        start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
        lat = float(start_position.get('latitude'))
        lon = float(start_position.get('longitude'))
        
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return jsonify({'error': '잘못된 좌표 범위입니다'}), 400
    except Exception as e:
        return jsonify({'error': f'잘못된 입력 형식입니다: {str(e)}'}), 400
    
    # 1. 바람 데이터 조회
    wind_data = fetch_wind_data(start_time)
    if not wind_data:
        return jsonify({'error': '바람 데이터를 조회할 수 없습니다'}), 500
    
    # 2. 좌표 변환
    grid_i, grid_j = latlon_to_grid(lat, lon)
    grid_lat, grid_lon = grid_to_latlon(grid_i, grid_j)
    logger.info(f"📍 위치 변환: ({lat}, {lon}) → Grid({grid_i}, {grid_j}) → ({grid_lat}, {grid_lon})")
    
    # 3. 모델 추론
    try:
        result = run_once(
            grid_i=grid_i,
            grid_j=grid_j,
            wind_dir_deg=wind_data['wind_dir_deg'],
            wind_speed_ms=wind_data['wind_spd_ms'],
            model_idx=DEFAULT_MODEL_IDX,
            size=GRID_SIZE,
            max_steps=MAX_STEPS
        )
    except Exception as e:
        logger.error(f"❌ 모델 추론 오류: {e}")
        return jsonify({'error': f'모델 추론 실패: {str(e)}'}), 500
    
    # 4. 응답 구성
    response = {
        'request': {
            'start_time': start_time_str,
            'start_position': {
                'input': {
                    'latitude': lat,
                    'longitude': lon
                },
                'grid': {
                    'i': grid_i,
                    'j': grid_j
                },
                'actual': {
                    'latitude': grid_lat,
                    'longitude': grid_lon
                }
            }
        },
        'weather': {
            'timestamp': wind_data['timestamp'],
            'wind': {
                'direction': {
                    'degrees': wind_data['wind_dir_deg'],
                    'cardinal_kr': deg_to_direction_kr(wind_data['wind_dir_deg']),
                    'cardinal_en': deg_to_direction_en(wind_data['wind_dir_deg'])
                },
                'speed': {
                    'ms': wind_data['wind_spd_ms'],
                    'knots': ms_to_knots(wind_data['wind_spd_ms'])
                }
            },
            'source': wind_data['source']
        },
        'guidance': {
            'summary': {
                'average_speed_knots': result['rec_speed'],
                'total_steps': len(result.get('rec_speed_list', [])),
                'target_eta_minutes': result.get('target_eta', 0),
                'actual_eta_minutes': result['eta']
            },
            'steps': format_guidance_steps(result, grid_i, grid_j, start_time)
        },
        'simulation': {
            'cost': result['cost'],
            'emissions': {
                'sox_kg': result['emission_sox'],
                'co2_kg': result['emission_co2']
            },
            'visualization_url': result.get('viz_url', '')
        }
    }
    
    logger.info(f"가이던스 생성 완료: ETA {result['eta']}분, Cost {result['cost']:.2f}")
    return jsonify(response)


# ================================================================
# 캐시 제어
# ================================================================

@app.after_request
def add_no_cache_headers(resp):
    """시뮬레이션 이미지와 API 응답 캐시 비활성화"""
    if request.path.startswith('/static/infer/') or request.path.startswith('/api/'):
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '0'
    return resp


# ================================================================
# 실행
# ================================================================

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("선박 운행 최적화 API 서버 시작")
    logger.info("=" * 60)
    logger.info(f"API 버전: {API_INFO['version']}")
    logger.info(f"최종 수정: {API_INFO['last_modified']}")
    logger.info(f"그리드 크기: {GRID_SIZE}x{GRID_SIZE}")
    logger.info(f"기상청 API: {'설정됨' if KMA_API_KEY else '미설정 (CSV만 사용)'}")
    logger.info(f"CSV Fallback: {'사용 가능' if os.path.exists(CSV_PATH) else '파일 없음'}")
    logger.info("=" * 60)
    
    app.run(host='0.0.0.0', port=8000, debug=True)