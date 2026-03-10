#!/usr/bin/env python3
"""
test_api.py

선박 운행 최적화 API 테스트 및 문서화 도구

사용법:
    python test_api.py                    # 전체 테스트 실행
    python test_api.py --endpoint info    # 특정 엔드포인트만 테스트
    python test_api.py --help             # 도움말
"""

import argparse
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import sys

# ================================================================
# 설정
# ================================================================
BASE_URL = "http://127.0.0.1:8000" # "http://localhost:8000"
TIMEOUT = 10

# 테스트용 데이터
TEST_DATETIME = "2025-12-17T01:00:00"
TEST_LATITUDE = 35.1
TEST_LONGITUDE = 129.05

# ================================================================
# 색상 코드 (터미널 출력용)
# ================================================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ================================================================
# 유틸리티 함수
# ================================================================

def print_header(text: str):
    """헤더 출력"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")


def print_section(text: str):
    """섹션 출력"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}[{text}]{Colors.ENDC}")
    print(f"{Colors.CYAN}{'-' * 60}{Colors.ENDC}")


def print_success(text: str):
    """성공 메시지 출력"""
    print(f"{Colors.GREEN} {text}{Colors.ENDC}")


def print_error(text: str):
    """에러 메시지 출력"""
    print(f"{Colors.RED} {text}{Colors.ENDC}")


def print_info(text: str):
    """정보 메시지 출력"""
    print(f"{Colors.BLUE}ℹ  {text}{Colors.ENDC}")


def print_json(data: Any, indent: int = 2):
    """JSON 데이터를 예쁘게 출력"""
    print(json.dumps(data, indent=indent, ensure_ascii=False))


def make_request(
    method: str,
    endpoint: str,
    params: Optional[Dict] = None,
    json_data: Optional[Dict] = None
) -> tuple[bool, Optional[Dict], str]:
    """
    API 요청 실행
    
    Returns:
        (success: bool, data: Dict or None, message: str)
    """
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, timeout=TIMEOUT)
        elif method.upper() == "POST":
            response = requests.post(url, json=json_data, timeout=TIMEOUT)
        else:
            return False, None, f"지원하지 않는 HTTP 메서드: {method}"
        
        if response.ok:
            return True, response.json(), f"성공 (HTTP {response.status_code})"
        else:
            error_data = None
            try:
                error_data = response.json()
            except:
                pass
            
            msg = f"실패 (HTTP {response.status_code})"
            if error_data and 'error' in error_data:
                msg += f": {error_data['error']}"
            
            return False, error_data, msg
    
    except requests.exceptions.Timeout:
        return False, None, f"타임아웃 ({TIMEOUT}초)"
    except requests.exceptions.ConnectionError:
        return False, None, "연결 실패 (서버가 실행 중인지 확인하세요)"
    except Exception as e:
        return False, None, f"예외 발생: {str(e)}"


# ================================================================
# 테스트 함수들
# ================================================================

def test_api_info():
    """API 정보 조회 테스트"""
    print_section("API 정보 조회")
    
    print_info("GET /api/info")
    print_info("설명: API 메타데이터 조회 (이름, 버전, 엔드포인트 목록)")
    print_info("참고: 레거시 엔드포인트 /wind, /simulate도 사용 가능 (HTML 호환)")
    
    success, data, msg = make_request("GET", "/api/info")
    
    if success:
        print_success(msg)
        print("\n 응답 데이터:")
        print_json(data)
        
        # 주요 정보 하이라이트
        if data:
            print(f"\n{Colors.BOLD}API 이름:{Colors.ENDC} {data.get('name')}")
            print(f"{Colors.BOLD}버전:{Colors.ENDC} {data.get('version')}")
            print(f"{Colors.BOLD}최종 수정:{Colors.ENDC} {data.get('last_modified')}")
            print(f"{Colors.BOLD}엔드포인트 수:{Colors.ENDC} {len(data.get('endpoints', {}))}")
    else:
        print_error(msg)
        if data:
            print_json(data)
    
    return success


def test_health_check():
    """헬스 체크 테스트"""
    print_section("헬스 체크")
    
    print_info("GET /api/health")
    print_info("설명: 서버 상태 및 설정 확인")
    
    success, data, msg = make_request("GET", "/api/health")
    
    if success:
        print_success(msg)
        print("\n 응답 데이터:")
        print_json(data)
        
        # 상태 하이라이트
        if data:
            config = data.get('config', {})
            status = data.get('status')
            
            print(f"\n{Colors.BOLD}상태:{Colors.ENDC} ", end="")
            if status == 'healthy':
                print(f"{Colors.GREEN} {status}{Colors.ENDC}")
            else:
                print(f"{Colors.RED} {status}{Colors.ENDC}")
            
            print(f"{Colors.BOLD}그리드 크기:{Colors.ENDC} {config.get('grid_size')}")
            print(f"{Colors.BOLD}최대 스텝:{Colors.ENDC} {config.get('max_steps')}")
            print(f"{Colors.BOLD}기상청 API:{Colors.ENDC} {'O' if config.get('kma_api_configured') else 'X'}")
            print(f"{Colors.BOLD}CSV Fallback:{Colors.ENDC} {'O' if config.get('csv_fallback_available') else 'X'}")
    else:
        print_error(msg)
        if data:
            print_json(data)
    
    return success


def test_wind_data(datetime_str: str = TEST_DATETIME):
    """바람 데이터 조회 테스트"""
    print_section("바람 데이터 조회")
    
    print_info(f"GET /api/wind?datetime={datetime_str}")
    print_info("설명: 특정 시점의 바람 정보 조회")
    
    params = {'datetime': datetime_str}
    success, data, msg = make_request("GET", "/api/wind", params=params)
    
    if success:
        print_success(msg)
        print("\n 응답 데이터:")
        print_json(data)
        
        # 바람 정보 하이라이트
        if data and 'wind' in data:
            wind = data['wind']
            direction = wind.get('direction', {})
            speed = wind.get('speed', {})
            
            print(f"\n{Colors.BOLD}풍향:{Colors.ENDC}")
            print(f"  • 각도: {direction.get('degrees')}°")
            print(f"  • 방위 (한글): {direction.get('cardinal_kr')}")
            print(f"  • 방위 (영문): {direction.get('cardinal_en')}")
            
            print(f"{Colors.BOLD}풍속:{Colors.ENDC}")
            print(f"  • m/s: {speed.get('ms')}")
            print(f"  • knots: {speed.get('knots')}")
            
            print(f"{Colors.BOLD}출처:{Colors.ENDC} {data.get('source')}")
    else:
        print_error(msg)
        if data:
            print_json(data)
    
    return success


def test_guidance(
    start_time: str = TEST_DATETIME,
    latitude: float = TEST_LATITUDE,
    longitude: float = TEST_LONGITUDE
):
    """접안 가이던스 생성 테스트"""
    print_section("접안 가이던스 생성")
    
    print_info("POST /api/guidance")
    print_info("설명: 시작 시점 및 위치 기반 접안 경로 최적화")
    
    payload = {
        "start_time": start_time,
        "start_position": {
            "latitude": latitude,
            "longitude": longitude
        }
    }
    
    print(f"\n 요청 데이터:")
    print_json(payload)
    
    success, data, msg = make_request("POST", "/api/guidance", json_data=payload)
    
    if success:
        print_success(msg)
        print("\n 응답 데이터:")
        
        # 요약 정보만 먼저 표시
        if data:
            print(f"\n{Colors.BOLD}【 요청 정보 】{Colors.ENDC}")
            request_data = data.get('request', {})
            start_pos = request_data.get('start_position', {})
            print(f"출발 시간: {request_data.get('start_time')}")
            print(f"입력 위치: ({start_pos.get('input', {}).get('latitude')}, "
                  f"{start_pos.get('input', {}).get('longitude')})")
            print(f"그리드 좌표: ({start_pos.get('grid', {}).get('i')}, "
                  f"{start_pos.get('grid', {}).get('j')})")
            print(f"실제 위치: ({start_pos.get('actual', {}).get('latitude')}, "
                  f"{start_pos.get('actual', {}).get('longitude')})")
            
            print(f"\n{Colors.BOLD}【 기상 정보 】{Colors.ENDC}")
            weather = data.get('weather', {})
            wind = weather.get('wind', {})
            print(f"풍향: {wind.get('direction', {}).get('cardinal_kr')} "
                  f"({wind.get('direction', {}).get('degrees')}°)")
            print(f"풍속: {wind.get('speed', {}).get('knots')} knots "
                  f"({wind.get('speed', {}).get('ms')} m/s)")
            print(f"출처: {weather.get('source')}")
            
            print(f"\n{Colors.BOLD}【 가이던스 요약 】{Colors.ENDC}")
            guidance = data.get('guidance', {})
            summary = guidance.get('summary', {})
            print(f"평균 속도: {summary.get('average_speed_knots')} knots")
            print(f"총 스텝: {summary.get('total_steps')}")
            print(f"목표 ETA: {summary.get('target_eta_minutes')} 분")
            print(f"실제 ETA: {summary.get('actual_eta_minutes')} 분")
            
            print(f"\n{Colors.BOLD}【 시뮬레이션 결과 】{Colors.ENDC}")
            simulation = data.get('simulation', {})
            emissions = simulation.get('emissions', {})
            print(f"운영 비용: {simulation.get('cost'):,.0f} 원")
            print(f"CO₂ 배출: {emissions.get('co2_kg'):,.2f} kg")
            print(f"SOx 배출: {emissions.get('sox_kg'):,.2f} kg")
            
            viz_url = simulation.get('visualization_url')
            if viz_url:
                print(f"시각화: {viz_url}")
            
            # 스텝 상세 정보 (처음 5개만)
            steps = guidance.get('steps', [])
            if steps:
                print(f"\n{Colors.BOLD}【 경로 상세 (처음 5개 스텝) 】{Colors.ENDC}")
                for i, step in enumerate(steps[:5]):
                    print(f"  Step {step.get('step')}:")
                    print(f"    • 시각: {step.get('time_display')}")
                    pos = step.get('position', {})
                    grid = pos.get('grid', {})
                    coord = pos.get('coordinates', {})
                    print(f"    • 위치: Grid({grid.get('i')}, {grid.get('j')}) → "
                          f"({coord.get('latitude'):.6f}, {coord.get('longitude'):.6f})")
                    heading = step.get('heading', {})
                    print(f"    • 방향: 의도 {heading.get('intended')} → 실제 {heading.get('actual')}")
                    speed = step.get('speed', {})
                    print(f"    • 추천 속도: {speed.get('recommended_knots')} knots")
                    eta = step.get('eta', {})
                    print(f"    • 시간: 경과 {eta.get('elapsed_minutes'):.1f}분, "
                          f"남은 시간 {eta.get('remaining_minutes'):.1f}분")
                
                if len(steps) > 5:
                    print(f"  ... (총 {len(steps)}개 스텝)")
        
        # 전체 JSON 출력 옵션
        print(f"\n{Colors.YELLOW} 전체 JSON 응답을 보려면 --verbose 옵션을 사용하세요{Colors.ENDC}")
    else:
        print_error(msg)
        if data:
            print_json(data)
    
    return success


def test_legacy_wind(datetime_str: str = TEST_DATETIME):
    """레거시 바람 데이터 조회 테스트 (HTML 호환)"""
    print_section("레거시 바람 데이터 조회 (HTML 호환)")
    
    print_info(f"GET /wind?datetime={datetime_str}")
    print_info("설명: 기존 HTML과 호환되는 바람 정보 조회")
    
    params = {'datetime': datetime_str}
    success, data, msg = make_request("GET", "/wind", params=params)
    
    if success:
        print_success(msg)
        print("\n  응답 데이터:")
        print_json(data)
        
        if data:
            print(f"\n{Colors.BOLD}풍향:{Colors.ENDC} {data.get('dir')}° ({data.get('dir8')})")
            print(f"{Colors.BOLD}풍속:{Colors.ENDC} {data.get('speed')} m/s")
            print(f"{Colors.BOLD}타임스탬프:{Colors.ENDC} {data.get('tm')}")
    else:
        print_error(msg)
        if data:
            print_json(data)
    
    return success


def test_legacy_simulate():
    """레거시 시뮬레이션 테스트 (HTML 호환)"""
    print_section("레거시 시뮬레이션 (HTML 호환)")
    
    print_info("POST /simulate")
    print_info("설명: 기존 HTML과 호환되는 시뮬레이션")
    
    payload = {
        "grid_i": 7,
        "grid_j": 3,
        "wind_dir": 270.0,
        "wind_speed": 5.2
    }
    
    print(f"\n 요청 데이터:")
    print_json(payload)
    
    success, data, msg = make_request("POST", "/simulate", json_data=payload)
    
    if success:
        print_success(msg)
        print("\n🎮 응답 데이터 (요약):")
        
        if data:
            print(f"{Colors.BOLD}평균 속도:{Colors.ENDC} {data.get('rec_speed')} knots")
            print(f"{Colors.BOLD}ETA:{Colors.ENDC} {data.get('eta')} 분")
            print(f"{Colors.BOLD}비용:{Colors.ENDC} {data.get('cost'):,.0f} 원")
            print(f"{Colors.BOLD}CO₂:{Colors.ENDC} {data.get('emission_co2'):,.4f} ton")
            print(f"{Colors.BOLD}SOx:{Colors.ENDC} {data.get('emission_sox'):,.4f} ton")
            print(f"{Colors.BOLD}스텝 수:{Colors.ENDC} {len(data.get('rec_speed_list', []))}")
    else:
        print_error(msg)
        if data:
            print_json(data)
    
    return success


# ================================================================
# 메인 함수
# ================================================================

def main():
    global BASE_URL
    parser = argparse.ArgumentParser(
        description="선박 운행 최적화 API 테스트 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  %(prog)s                          # 모든 엔드포인트 테스트
  %(prog)s --endpoint info          # API 정보만 테스트
  %(prog)s --endpoint health        # 헬스 체크만 테스트
  %(prog)s --endpoint wind          # 바람 데이터 조회만 테스트
  %(prog)s --endpoint guidance      # 접안 가이던스만 테스트
  %(prog)s --endpoint legacy-wind   # 레거시 바람 조회만 테스트
  %(prog)s --endpoint legacy-simulate  # 레거시 시뮬레이션만 테스트
  %(prog)s --base-url http://server:8000  # 다른 서버 테스트
        """
    )
    
    parser.add_argument(
        '--endpoint',
        choices=['info', 'health', 'wind', 'guidance', 'legacy-wind', 'legacy-simulate', 'all'],
        default='all',
        help='테스트할 엔드포인트 (기본: all)'
    )
    
    parser.add_argument(
        '--base-url',
        default=BASE_URL,
        help=f'API 서버 주소 (기본: {BASE_URL})'
    )
    
    parser.add_argument(
        '--datetime',
        default=TEST_DATETIME,
        help=f'테스트용 시간 (기본: {TEST_DATETIME})'
    )
    
    parser.add_argument(
        '--latitude',
        type=float,
        default=TEST_LATITUDE,
        help=f'테스트용 위도 (기본: {TEST_LATITUDE})'
    )
    
    parser.add_argument(
        '--longitude',
        type=float,
        default=TEST_LONGITUDE,
        help=f'테스트용 경도 (기본: {TEST_LONGITUDE})'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='전체 JSON 응답 출력'
    )
    
    args = parser.parse_args()
    
    # 글로벌 설정 업데이트
    BASE_URL = args.base_url
    
    # 헤더 출력
    print_header("선박 운행 최적화 API 테스트")
    print(f"{Colors.BOLD}서버 주소:{Colors.ENDC} {BASE_URL}")
    print(f"{Colors.BOLD}테스트 시간:{Colors.ENDC} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 테스트 실행
    results = {}
    
    if args.endpoint in ['info', 'all']:
        results['info'] = test_api_info()
    
    if args.endpoint in ['health', 'all']:
        results['health'] = test_health_check()
    
    if args.endpoint in ['wind', 'all']:
        results['wind'] = test_wind_data(args.datetime)
    
    if args.endpoint in ['guidance', 'all']:
        results['guidance'] = test_guidance(args.datetime, args.latitude, args.longitude)
    
    if args.endpoint in ['legacy-wind', 'all']:
        results['legacy-wind'] = test_legacy_wind(args.datetime)
    
    if args.endpoint in ['legacy-simulate', 'all']:
        results['legacy-simulate'] = test_legacy_simulate()
    
    # 결과 요약
    print_header("테스트 결과 요약")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    for endpoint, success in results.items():
        status = f"{Colors.GREEN} PASS{Colors.ENDC}" if success else f"{Colors.RED} FAIL{Colors.ENDC}"
        print(f"{endpoint.upper():15} {status}")
    
    print(f"\n{Colors.BOLD}총 {total}개 테스트:{Colors.ENDC} "
          f"{Colors.GREEN}{passed} 성공{Colors.ENDC}, "
          f"{Colors.RED}{failed} 실패{Colors.ENDC}")
    
    # 종료 코드
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()