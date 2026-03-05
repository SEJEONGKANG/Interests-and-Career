# environment.py
import os
import csv
import math
import random
import numpy as np
from core.gridboard import *

# ================================================================
# 부산항 주변 위경도 <-> 15x15 그리드 매핑 설정
# ================================================================
# Leaflet에서 사용 중인 ECA/VSRZ 좌표 범위를 모두 포함하는 박스
LAT_MIN = 33.8704
LAT_MAX = 35.3935
LON_MIN = 128.3367
LON_MAX = 130.1110

def grid_to_latlon(r, c, size):
    """
    격자 인덱스 (row=r, col=c) -> 해당 칸 중심의 (lat, lon)
    row=0은 북쪽(LAT_MAX)에, col=0은 서쪽(LON_MIN)에 대응
    """
    dLat = (LAT_MAX - LAT_MIN) / size
    dLon = (LON_MAX - LON_MIN) / size
    lat = LAT_MAX - (r + 0.5) * dLat
    lon = LON_MIN + (c + 0.5) * dLon
    return lat, lon

def latlon_to_grid(lat, lon, size):
    """
    위경도(lat, lon) -> 가장 가까운 격자 칸 인덱스 (r, c)
    """
    dLat = (LAT_MAX - LAT_MIN) / size
    dLon = (LON_MAX - LON_MIN) / size

    i_float = (LAT_MAX - lat) / dLat - 0.5
    j_float = (lon - LON_MIN) / dLon - 0.5

    r = int(round(i_float))
    c = int(round(j_float))

    r = max(0, min(size - 1, r))
    c = max(0, min(size - 1, c))
    return (r, c)

# ---------------------------------------------------------------
# 실제 ECA / VSRZ 폴리곤 (Leaflet index.html 과 동일)
# lat, lon 순서
# ---------------------------------------------------------------
ECA_POLY = [
    (35.094771, 128.714361),
    (34.966718, 128.730240),
    (34.916517, 128.833280),
    (34.974876, 129.074249),
    (34.977802, 129.113344),
    (34.966386, 129.141338),
    (34.963849, 129.171464),
    (34.970423, 129.200973),
    (34.985509, 129.227173),
    (35.007729, 129.247673),
    (35.035056, 129.260604),
    (35.064998, 129.264785),
    (35.094822, 129.259836),
    (35.121808, 129.246207),
    (35.143494, 129.225142),
    (35.157900, 129.198563),
    (35.159635, 129.192781),
]

VSR1_POLY = [
    (35.09133004385173, 129.12660598754886),
    (35.03730543262893, 129.09244537353518),
    (34.758114796197944, 128.86799812316897),
    (34.701647773382,   129.07592296600345),
    (35.01558716614377, 129.52275753021243),
    (35.047231,         129.530433),
    (35.079392,         129.533831),
    (35.11167,          129.533414),
    (35.143764,         129.529182),
    (35.175372,         129.521169),
    (35.206198,         129.509448),
    (35.235952,         129.494124),
    (35.264353,         129.475337),
    (35.291134,         129.453261),
    (35.316041,         129.428101),
    (35.33915291306285, 129.40043807029727),
]

VSR2_POLY = [
    (34.9895,   128.82906),
    (34.71917,  128.60417),
    (34.684002, 128.680160),
    (34.664838, 128.764349),
    (34.661093, 128.851571),
    (34.672945, 128.937721),
    (34.699833, 129.018736),
    (34.740492, 129.090793),
    (34.793002, 129.150474),
    (34.854880, 129.194933),
    (34.923196, 129.222026),
    (34.994705, 129.230425),
    (35.06639,  129.22139),
]

# 부산 인근 MAINLAND 폴리곤 (lat, lon)
LAND_POLY_MAINLAND = [
    (35.08957427943165, 128.70758056640628),
    (35.05360791102561, 128.71788024902347),
    (35.02999636902566, 128.7906646728516),
    (34.97656414322785, 128.81538391113284),
    (34.72016869311106, 128.59771728515628),
    (34.66935854524545, 127.99621582031251),
    (34.31621838080741, 126.09008789062501),
    (37.49229399862877, 126.43066406250001),
    (37.96152331396614, 124.84863281250001),
    (39.2832938689385, 125.39794921875001),
    (39.707186656826565, 124.23339843750001),
    (41.68932225997044, 126.87011718750001),
    (41.343824581185714, 128.14453125000003),
    (42.87596410238256, 130.05615234375003),
    (42.24478535602799, 130.73730468750003),
    (41.50857729743935, 129.77050781250003),
    (40.713955826286046, 129.85839843750003),
    (39.605688178320804, 127.63916015625001),
    (39.04478604850143, 127.63916015625001),
    (38.548165423046584, 128.36425781250003),
    (38.013476231041935, 128.64990234375003),
    (37.42252593456307, 129.28710937500003),
    (36.54494944148322, 129.46289062500003),
    (35.991340960635405, 129.42443847656253),
    (36.071302299422406, 129.56726074218753),
    (35.35993616287676, 129.39971923828128),
    (35.17268577075072, 129.1978454589844),
    (35.097439809364204, 128.71032714843753),
]

# 대마도 폴리곤 (lat, lon)
LAND_POLY_TSUSHIMA = [
    (34.6987193245323, 129.44915771484378),
    (34.638857487069885, 129.38598632812503),
    (34.639987356029515, 129.32281494140628),
    (34.54728700119802, 129.2912292480469),
    (34.35137289731883, 129.24316406250003),
    (34.110667538759024, 129.16763305664065),
    (34.08451193447477, 129.22805786132815),
    (34.21180215769026, 129.3241882324219),
    (34.26289150646404, 129.3461608886719),
    (34.290126479407164, 129.3955993652344),
    (34.39444542699783, 129.38598632812503),
    (34.48165602990584, 129.41482543945315),
    (34.551811369170494, 129.47387695312503),
    (34.68404023638139, 129.4889831542969),
]

# 여러 육지를 함께 쓰고 싶으면 이렇게 묶어서 사용
LAND_POLYS = [LAND_POLY_MAINLAND, LAND_POLY_TSUSHIMA]

def _point_in_poly(lat, lon, poly):
    """
    lat, lon 이 다각형(poly) 내부에 있는지 여부 (ray casting)
    poly: [(lat, lon), ...]
    """
    x = lon
    y = lat
    inside = False
    n = len(poly)
    for i in range(n):
        lat_i, lon_i = poly[i]
        lat_j, lon_j = poly[(i - 1) % n]
        xi, yi = lon_i, lat_i
        xj, yj = lon_j, lat_j

        intersect = ((yi > y) != (yj > y)) and \
                    (x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi)
        if intersect:
            inside = not inside
    return inside

def cell_in_poly(r, c, poly, size):
    """
    grid cell (r, c)의 중심과 네 모서리 중
    하나라도 poly 안에 들어가면 True.
    """
    dLat = (LAT_MAX - LAT_MIN) / size
    dLon = (LON_MAX - LON_MIN) / size

    # 중심
    lat_c, lon_c = grid_to_latlon(r, c, size)

    # 모서리
    lat_top    = LAT_MAX - r * dLat
    lat_bottom = LAT_MAX - (r + 1) * dLat
    lon_left   = LON_MIN + c * dLon
    lon_right  = LON_MIN + (c + 1) * dLon

    samples = [
        (lat_c,      lon_c),      # center
        (lat_top,    lon_left),   # TL
        (lat_top,    lon_right),  # TR
        (lat_bottom, lon_left),   # BL
        (lat_bottom, lon_right),  # BR
    ]

    return any(_point_in_poly(lt, ln, poly) for (lt, ln) in samples)

# ================================================================
# 전역 상수
# ================================================================
DECAY_RATE = 0.99
SHAPING_ETA_PENALTY = 0.80

# 8방향 (N, NE, E, SE, S, SW, W, NW)
DIR_DELTAS = {
    0: (-1,  0),  # N
    1: (-1,  1),  # NE
    2: ( 0,  1),  # E
    3: ( 1,  1),  # SE
    4: ( 1,  0),  # S
    5: ( 1, -1),  # SW
    6: ( 0, -1),  # W
    7: (-1, -1),  # NW
}
# 헤딩 인덱스 → 도수(0° = N)
HEADING_DEG = {i: (i * 45) % 360 for i in range(8)}

# ================================================================
# Environment 클래스
# ================================================================
class Environment:
    """항로 최적화 학습용 해상 환경"""

    # ------------------------------------------------------------
    # ▶ 초기화 및 기본 구성
    # ------------------------------------------------------------
    def __init__(self, size, mode='static', wind_csv_path='./data/OBS_BUOY_TIM_20251111222621.csv'):
        self.size = size
        self.board = GridBoard(size=size)

        # 기본 상태 변수
        self.epsilon_end = 0.01
        self.decay_rate = DECAY_RATE
        self.VA = False
        self.distance = 5  # grid cell 거리(km)
        self.rc_speed = 0
        self.p_operational = 0
        self.cnt_VSRIPmet = 0
        self.CO2, self.SOx = 0, 0

        # 구성요소 등록
        self.board.addPiece('Player', 'P', (0, 0))
        self.board.addPiece('Goal', '+', (2, 6))
        self.board.addPiece('ECA', 'E', [])
        self.board.addPiece('VSRZ', 'V', [])
        self.board.addPiece('Land', 'X', [])
        self.board.addPiece('Sea', ' ', [])
        self.board.addPiece('ETA', 'T', (0, 0))

        self.initGridStatic()

        # 출발점을 바다 중 무작위로 설정
        sea_positions = self.board.components['Sea'].pos
        start_pos = random.choice(sea_positions)
        self.board.components['Player'].pos = start_pos
        self.board.components['ETA'].pos = start_pos
        
        self.ETA = self.compute_ETA(speed_kn=15.0)

        # 바람 데이터
        self.wind_series = self._load_wind_csv(wind_csv_path)
        if self.wind_series:
            w = random.choice(self.wind_series)
            self.wind_dir_deg = w['dir_deg']
            self.wind_spd_kn = w['spd_kn']
        else:
            self.wind_dir_deg, self.wind_spd_kn = 0.0, 0.0

        # 현재 heading/speed
        self.current_heading = None  # 0~7
        self.current_STW = None      # knots
        self._prev_goal_dist_km = self._dist8_km(
            self.board.components['Player'].pos,
            self.board.components['Goal'].pos
        )

    # ------------------------------------------------------------
    # ▶ Grid 초기화
    # ------------------------------------------------------------
    def initGridStatic(self):
        """
        15x15 부산항 해역 grid 구성 (실제 위경도 근사 반영)

        - Grid 전체는 LAT_MIN~LAT_MAX, LON_MIN~LON_MAX 를 균등 분할
        - 각 cell 중심 위경도 기준으로
          · LAND_POLYS 내부면 Land
          · ECA_POLY 내부면 ECA
          · VSR1_POLY 혹은 VSR2_POLY 내부면 VSRZ
        - 목적지는 실제 좌표:
          북위 35° 04′ 42″, 동경 129° 01′ 01″
        """
        size = self.size

        # -------------------------------
        # 1) Goal 위치: 실제 위경도 → 격자
        # -------------------------------
        GOAL_LAT = 35 + 4 / 60 + 42 / 3600      # 35.078333...
        GOAL_LON = 129 + 1 / 60 + 1 / 3600      # 129.016944...
        goal = latlon_to_grid(GOAL_LAT, GOAL_LON, size)
        self.board.components['Goal'].pos = goal

        # -------------------------------
        # 2) Land / ECA / VSRZ 초기화
        #    - 각 cell 중심 기준으로 point-in-polygon 판정
        # -------------------------------
        land = []
        ECA = []
        VSRZ = []

        for r in range(size):
            for c in range(size):
                lat, lon = grid_to_latlon(r, c, size)

                # 1) Land: 그냥 중심 기준으로만 판정 (지형은 거칠어도 크게 문제 X)
                is_land = any(
                    _point_in_poly(lat, lon, poly)
                    for poly in LAND_POLYS
                )
                if is_land:
                    land.append((r, c))
                    continue

                # 2) ECA: 셀 중심 + 모서리까지 포함해서 판정
                if cell_in_poly(r, c, ECA_POLY, size):
                    ECA.append((r, c))

                # 3) VSRZ: VSR1/VSR2 모두 동일 방식
                if cell_in_poly(r, c, VSR1_POLY, size) or \
                cell_in_poly(r, c, VSR2_POLY, size):
                    VSRZ.append((r, c))

        # -------------------------------
        # 3) Goal은 항상 바다/항로 칸으로 취급
        # -------------------------------
        if goal in land:
            land.remove(goal)

        self.board.components['Land'].pos = land
        self.board.components['ECA'].pos = ECA
        self.board.components['VSRZ'].pos = VSRZ

        # -------------------------------
        # 4) Sea = 나머지
        # -------------------------------
        sea = [
            (r, c)
            for r in range(size)
            for c in range(size)
            if (r, c) not in land + ECA + VSRZ + [goal]
        ]
        self.board.components['Sea'].pos = sea

    # ------------------------------------------------------------
    # ▶ 거리/ETA 계산
    # ------------------------------------------------------------
    def _dist8_km(self, a, b):
        """8방향 격자 최소 경로거리 (km 단위)"""
        dx, dy = abs(a[0]-b[0]), abs(a[1]-b[1])
        diag, straight = min(dx, dy), max(dx, dy) - min(dx, dy)
        return self.distance * (diag * math.sqrt(2) + straight)

    def compute_ETA(self, speed_kn=15.0):
        """현재 위치에서 Goal까지 ETA(분) 계산"""
        goal = self.board.components['Goal'].pos
        player = self.board.components['Player'].pos
        dist_km = self._dist8_km(player, goal)
        speed_kmh = speed_kn * 1.852
        return 60.0 * (dist_km / speed_kmh)

    # ------------------------------------------------------------
    # ▶ Wind 관련
    # ------------------------------------------------------------
    def _load_wind_csv(self, path):
        """풍향/풍속 CSV 로드 (컬럼명 자동 탐지)"""
        data = []
        if not path or not os.path.exists(path):
            return data

        with open(path, newline='', encoding='cp949') as f:
            reader = csv.DictReader(f)
            cols = [c.lower() for c in reader.fieldnames]

            def find_col(cands):
                for c in cands:
                    if c.lower() in cols:
                        return reader.fieldnames[cols.index(c.lower())]
                return None

            dir_col = find_col(['wd', 'wind_dir', 'direction', 'dir'])
            spd_col = find_col(['ws', 'wind_spd', 'wind_speed', 'spd', 'speed'])

            for row in reader:
                try:
                    deg = float(row[dir_col]) if dir_col else 0.0
                    spd = float(row[spd_col]) if spd_col else 0.0
                except Exception:
                    continue
                data.append({'dir_deg': deg % 360, 'spd_kn': max(0.0, spd * 1.94384)})
        return data

    # ------------------------------------------------------------
    # ▶ 이동 검증 (육지/경계 충돌 방지)
    # ------------------------------------------------------------
    def _in_bounds(self, pos):
        """그리드 내부인지 확인"""
        r, c = pos
        return 0 <= r < self.size and 0 <= c < self.size

    def _is_land(self, pos):
        """해당 칸이 육지인지 확인"""
        return pos in self.board.components['Land'].pos

    def validateMove(self, piece, addpos=(0, 0)):
        """이동이 유효한지(경계·육지 충돌 여부) 검사"""
        cur_pos = self.board.components[piece].pos
        new_pos = addTuple(cur_pos, addpos)
        if not self._in_bounds(new_pos):
            return 1  # 경계 밖
        if self._is_land(new_pos):
            return 1  # 육지로 이동 시도
        return 0  # 이동 가능

    # ------------------------------------------------------------
    # ▶ 이동 및 Drift
    # ------------------------------------------------------------
    def makeMove(self, action_dir_):
        """이동하고 (moved, actual_heading) 반환"""
        def try_move(addpos):
            if self.validateMove('Player', addpos) == 0:
                player = self.board.components['Player']
                self.board.movePiece('Player', addTuple(player.pos, addpos))
                self.board.components['ETA'].pos = player.pos
                return True
            return False

        chosen = action_dir_
        actual = self._wind_drift(chosen)

        # drift 방향이 육지라면 무효
        dx_d, dy_d = DIR_DELTAS[actual]
        if self.validateMove('Player', (dx_d, dy_d)) != 0:
            actual = chosen  # drift 취소

        # chosen도 육지면 이동 실패
        dx, dy = DIR_DELTAS[actual]
        moved = try_move((dx, dy))

        self.current_heading = actual
        return moved, actual

    def _wind_drift(self, chosen):
        """측풍 + 강풍 시 ±45° drift, 단 직전 heading 대비 ±90° 이상 회전 금지"""

        # Goal 도달 가능 여부 체크
        pr, pc = self.board.components['Player'].pos
        gr, gc = self.board.components['Goal'].pos
        dx, dy = DIR_DELTAS[chosen]
        next_pos = (pr + dx, pc + dy)

        # Goal 로 정확히 향하는 방향이라면 drift 금지
        if next_pos == (gr, gc):
            return chosen

        if self.current_heading is None:
            base_heading = chosen
        else:
            base_heading = self.current_heading

        heading_deg = HEADING_DEG[chosen]
        rel_angle = self._angle_diff_deg((self.wind_dir_deg + 180) % 360, heading_deg) # heading이 0일때 북쪽으로 향하는건데, 바람은 반대여서 180 더함
        sidewind = abs(abs(rel_angle) - 90) <= 20

        actual = chosen
        if sidewind and self.wind_spd_kn >= 12.0:
            p = min(0.6, 0.03 * self.wind_spd_kn)
            if random.random() < p:
                delta = 1 if rel_angle > 0 else -1  # ±45° drift
                actual = (chosen + delta) % 8

        # -------- drift 후 회전 제한 (±90° 이내로만 허용) --------
        diff = (actual - base_heading + 8) % 8
        if diff > 4:  # wrap-around 보정 (-4 ~ +4 범위로 정규화)
            diff -= 8
        if abs(diff) > 2:  # ±90° 초과 시 보정
            actual = (base_heading + (2 if diff > 0 else -2)) % 8

        return actual

    def _angle_diff_deg(self, a, b):
        """두 각도 차이를 [-180, 180] 범위로 반환"""
        return (a - b + 180) % 360 - 180

    # ------------------------------------------------------------
    # ▶ Action 선택 (epsilon-greedy)
    # ------------------------------------------------------------
    def get_safe_dirs(self, dirs):
        """dirs 중 실제 이동 가능한 방향만 남김"""
        current_pos = self.board.components['Player'].pos
        safe = []
        for d in dirs:
            dx, dy = DIR_DELTAS[d]
            next_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if self._in_bounds(next_pos) and (next_pos not in self.board.components['Land'].pos):
                safe.append(d)
        return safe

    def get_valid_actions(self):
        """KW: 실제 이동 가능한 action만 마스킹하여 반환"""

        # ------------------------------
        # 1) direction mask
        # ------------------------------
        if self.current_heading is None:
            # 첫 스텝이면 목표 방향 3개 먼저 고려
            g = self._goal_heading_idx()
            candidates = [g, (g+1)%8, (g-1)%8]
        else:
            h = self.current_heading
            # ±90도 범위 우선
            candidates = [(h+d) % 8 for d in (-2,-1,0,1,2)]
        
        # 후보 중 실제 이동 가능만 남김
        allowed_dirs = self.get_safe_dirs(candidates)

        # 그래도 없으면 → 8방향 전체 검사
        if not allowed_dirs:
            allowed_dirs = self.get_safe_dirs(range(8))

        # ------------------------------
        # 2) speed mask (기존 유지)
        # ------------------------------
        if self.current_STW is None:
            allowed_speeds = list(range(26))
        else:
            last_idx = int(round(self.current_STW - 5))
            lo, hi = max(0, last_idx - 3), min(25, last_idx + 3)
            allowed_speeds = list(range(lo, hi + 1))

        return allowed_dirs, allowed_speeds

    def select_action(self, model, state, action_size_dir, action_size_speed, epsilon):
        """KW: get_valid_actions()를 사용하여 단순화된 액션 선택"""
        q_dir, q_spd = model(state)
        q_dir, q_spd = q_dir.data.numpy()[0], q_spd.data.numpy()[0]

        # KW: 유효한 액션 마스크 가져오기
        allowed_dirs, allowed_speeds = self.get_valid_actions()

        # epsilon-greedy
        if random.random() < epsilon:
            a_dir = random.choice(allowed_dirs)
            a_spd = random.choice(allowed_speeds)
        else:
            mask_q_dir = np.full_like(q_dir, -1e9)
            mask_q_dir[allowed_dirs] = q_dir[allowed_dirs]
            a_dir = int(np.argmax(mask_q_dir))
            mask_q_spd = np.full_like(q_spd, -1e9)
            mask_q_spd[allowed_speeds] = q_spd[allowed_speeds]
            a_spd = int(np.argmax(mask_q_spd))
            
        if a_dir not in allowed_dirs:
            a_dir = max(allowed_dirs, key=lambda d: q_dir[d])
        if a_spd not in allowed_speeds:
            a_spd = max(allowed_speeds, key=lambda s: q_spd[s])

        self.current_STW = a_spd + 5
        return a_dir, a_spd

    def update_epsilon(self, eps):
        """epsilon decay"""
        return max(self.epsilon_end, eps * self.decay_rate)

    # ------------------------------------------------------------
    # ▶ 보상 함수
    # ------------------------------------------------------------
    def reward(self, action_dir_, action_speed_, done, mov, ETA):
        """운항비, 탄소, ETA mismatch, shaping 포함 보상 계산"""
        STW = action_speed_ + 5
        SOG = max(0.1, STW + self.convert_STW_to_SOG(action_dir_, STW))

        # step 거리 및 시간
        distance_step = self.distance * (math.sqrt(2) if self.current_heading in (1, 3, 5, 7) else 1.0)
        t = distance_step / (SOG * 0.0309)  # 분 단위
        ETA -= t
 
        # 연료/비용 계산
        consumption = self.cal_fuel_consumption(SOG)
        fuel_cost = t * consumption * (1000 if self.check_ECA() else 400) # SJ : 왜 1000 혹은 400을 곱함?
        time_cost = t * (20000 / 60)
        carbon_cost = t * 65.469 * consumption
        vsrz_refund = 0.5 * self.check_VSRZ() * int(STW <= 12) * 4800

        if vsrz_refund > 0:
            self.cnt_VSRIPmet += 1

        operational_cost = (-(fuel_cost + time_cost + carbon_cost) + vsrz_refund) * 1450 # SJ : 원래 없었음. 환율 여기서 곱해야 하지 않나? 
        scaled_cost = 2 * self.normalize_operational_cost(operational_cost)

        # 배출량 누적
        SOx_vals = (2, 0.4)  # (VLSFO, MGO)
        CO2_vals = (3.114, 3.206)
        self.SOx += consumption * (SOx_vals[0]*(1-self.check_ECA()) + SOx_vals[1]*self.check_ECA())
        self.CO2 += consumption * (CO2_vals[0]*(1-self.check_ECA()) + CO2_vals[1]*self.check_ECA())

        # 종료 조건
        if self.board.components['Player'].pos == self.board.components['Goal'].pos:
            done = True
            reward = self._reward_arrival(ETA)
            print(f' ARRIVED: mov {mov}, ETA {ETA:.2f}')
        elif mov > 50 or ETA < -200:
            done = True
            reward = -5  # 실패
            print(f' FAILED: mov {mov}, ETA {ETA:.2f}')
        else:
            reward = scaled_cost + self.reward_shaping(SOG)
            self.p_operational = operational_cost

        return reward, done, ETA

    def _reward_arrival(self, ETA):
        """목적지 도착 시 보상 계산"""
        ETA_mis = abs(ETA)
        # ETA 일치 정도
        if ETA >= 0:
            if ETA_mis < 5:
                ETA_score = 90
            elif ETA_mis < 10:
                ETA_score = 75
            else:
                ETA_score = 45
        else:
            if ETA_mis < 5:
                ETA_score = 60
            elif ETA_mis < 10:
                ETA_score = 45
            else:
                ETA_score = 15
        return ETA_score

    # ------------------------------------------------------------
    # ▶ 기타 유틸
    # ------------------------------------------------------------
    def _goal_heading_idx(self):
        """현재 위치에서 Goal까지의 8방향 헤딩 인덱스(0~7)를 반환"""
        pr, pc = self.board.components['Player'].pos
        gr, gc = self.board.components['Goal'].pos
        dr, dc = gr - pr, gc - pc

        # 방향 성분을 {-1,0,1}로 정규화
        sr = 0 if dr == 0 else (1 if dr > 0 else -1)
        sc = 0 if dc == 0 else (1 if dc > 0 else -1)

        # (sr, sc)에 대응하는 방향 인덱스 찾기
        inv = {v: k for k, v in DIR_DELTAS.items()}
        return inv.get((sr, sc), 0)  # 기본값 N(0)

    def _filter_land_directions(self, candidate_dirs):
        """KW: 유효하지 않은 방향 제거"""
        current_pos = self.board.components['Player'].pos
        land_positions = self.board.components['Land'].pos
        safe_dirs = []

        for dir_idx in candidate_dirs:
            dx, dy = DIR_DELTAS[dir_idx]
            next_pos = (current_pos[0] + dx, current_pos[1] + dy)

            # KW: 다음 위치가 유효한 경우만 허용
            if self._in_bounds(next_pos) and next_pos not in land_positions:
                safe_dirs.append(dir_idx)

        return safe_dirs

    def _get_safe_emergency_directions(self):
        """
        SJ : 모든 기본 후보 방향이 막혔을 때 사용하는 비상 로직.

        변경 사항:
        1) 현재 heading 기준 ±90° 범위(= h-2 ~ h+2) 우선 확인
        2) 그래도 없으면 8방향 전체 확인
        3) 8방향 중 반드시 하나는 바다이므로 마지막 fallback 필요 없음
        """
        current_pos = self.board.components['Player'].pos
        land_positions = self.board.components['Land'].pos

        # 현재 heading이 없으면 (첫 스텝 등) 8방향 전체 검사
        if self.current_heading is None:
            candidates = list(range(8))
        else:
            h = self.current_heading
            # 1) 현재 heading ± 2(총 5 방향) 우선 후보
            candidates = [(h + d) % 8 for d in (-2, -1, 0, 1, 2)]

        # 1차 후보 중 안전한 방향 찾기
        first_safe = []
        for dir_idx in candidates:
            dx, dy = DIR_DELTAS[dir_idx]
            next_pos = (current_pos[0] + dx, current_pos[1] + dy)

            if self._in_bounds(next_pos) and next_pos not in land_positions:
                first_safe.append(dir_idx)

        if first_safe:
            return first_safe

        # 2) 그래도 없으면 8방향 전체 검사
        all_safe = []
        for dir_idx in range(8):
            dx, dy = DIR_DELTAS[dir_idx]
            next_pos = (current_pos[0] + dx, current_pos[1] + dy)

            if self._in_bounds(next_pos) and next_pos not in land_positions:
                all_safe.append(dir_idx)

        return all_safe
    
    def cal_fuel_consumption(self, SOG):
        return 0.00047 * (SOG ** 3) # ton/min  # SJ : 1440 곱해져있었음. 왜지? 환율인가? 일단 환율 다른곳에서 계산해둠.

    def reward_shaping(self, SOG):
        """속도 셰이핑 (권장속도 rc에 근접하도록 유도)"""
        self.recommended_speed(self.ETA)
        rc = float(self.rc_speed)
        return -0.010 * (rc - SOG) ** 2 / 5

    def convert_STW_to_SOG(self, dir_idx, STW):
        """풍향에 따른 단순 속도 보정"""
        if STW <= 0:
            return 0.0
        k = 0.05
        delta = k * self.wind_spd_kn * math.cos(math.radians(self._angle_diff_deg(self.wind_dir_deg, HEADING_DEG[dir_idx])))
        return delta

    def recommended_speed(self, ETA):
        """목표 ETA를 기반으로 권장 속도 계산"""
        start = self.board.components['Player'].pos
        goal = self.board.components['Goal'].pos
        manh_dist = sum(abs(s - g) for s, g in zip(start, goal))
        self.rc_speed = max(min(((manh_dist * self.distance) / ETA) * 32.397, 30), 5)

    def check_ECA(self):
        return int(self.board.components['Player'].pos in self.board.components['ECA'].pos)

    def check_VSRZ(self):
        return int(self.board.components['Player'].pos in self.board.components['VSRZ'].pos)

    def normalize_operational_cost(self, val, orig_max=0, orig_min=-1e9, new_min=-1, new_max=0):
        return (new_max - new_min) * (val - orig_min) / (orig_max - orig_min) + new_min

    def render_text(self):
        """콘솔용 텍스트 보드"""
        grid = self.board.render()
        for r in range(self.size):
            print(' '.join(grid[r, :]))
