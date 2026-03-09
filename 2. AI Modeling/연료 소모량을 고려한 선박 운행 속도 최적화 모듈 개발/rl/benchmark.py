# benchmark.py
import random
import math

# ================================================================
# Heuristic (Benchmark) Algorithm
# ================================================================
def benchmark_main(env, ETA, *, debug=False, grid_size=None, max_steps=10000):
    """
    Simple rule-based benchmark algorithm for ship navigation.

    Heuristic logic:
      - Direction: choose the move that gets closer to Goal (8 directions)
      - Speed: estimate target SOG based on remaining distance (km) and remaining ETA (minutes)

    Returns:
        tuple: (
            total_reward, total_operational_cost, step_count, ETA_left,
            total_SOx_kg, total_CO2_kg, speed_idx_seq, heading_seq, eca_inout_bins
        )
    """
    # ------------------------------------------------------------
    # ▶ 내부 유틸리티
    # ------------------------------------------------------------
    DIRECTIONS = {
        0: (-1,  0),  # N
        1: (-1,  1),  # NE
        2: ( 0,  1),  # E
        3: ( 1,  1),  # SE
        4: ( 1,  0),  # S
        5: ( 1, -1),  # SW
        6: ( 0, -1),  # W
        7: (-1, -1),  # NW
    }

    def chebyshev_distance(a, b):
        """체비쇼프 거리 (8방향 격자 최단 경로)"""
        return max(abs(a[0]-b[0]), abs(a[1]-b[1]))

    def render_board(current, goal, grid_size, extra_marks=None):
        """디버그용 텍스트 보드 시각화"""
        H, W = grid_size
        board = [["." for _ in range(W)] for _ in range(H)]
        gx, gy = goal
        px, py = current
        if 0 <= gx < H and 0 <= gy < W:
            board[gx][gy] = "G"
        if 0 <= px < H and 0 <= py < W:
            board[px][py] = "P"
        if extra_marks:
            for (x, y), ch in extra_marks.items():
                if 0 <= x < H and 0 <= y < W and board[x][y] == ".":
                    board[x][y] = ch
        lines = ["    " + " ".join([f"{c:2d}" for c in range(W)])]
        for i, row in enumerate(board):
            lines.append(f"{i:2d}  " + " ".join([f"{cell:>2s}" for cell in row]))
        return "\n".join(lines)

    def heu_direction(current, goal, prev_dir=None):
        """현재 위치에서 Goal로 체비쇼프 거리가 줄어드는 방향 선택"""
        H, W = grid_size
        allowed = list(DIRECTIONS.keys())
        if prev_dir is not None:
            allowed = [prev_dir, (prev_dir+1) % 8, (prev_dir-1) % 8]

        best_dirs, best_dist = [], float("inf")
        for d in allowed:
            dx, dy = DIRECTIONS[d]
            nbr = (current[0] + dx, current[1] + dy)
            if not (0 <= nbr[0] < H and 0 <= nbr[1] < W):
                continue
            dist = chebyshev_distance(nbr, goal)
            if dist < best_dist:
                best_dist, best_dirs = dist, [d]
            elif dist == best_dist:
                best_dirs.append(d)

        if not best_dirs:  # 폴백: 전체 탐색
            for d, (dx, dy) in DIRECTIONS.items():
                nbr = (current[0] + dx, current[1] + dy)
                if not (0 <= nbr[0] < H and 0 <= nbr[1] < W):
                    continue
                dist = chebyshev_distance(nbr, goal)
                if dist < best_dist:
                    best_dist, best_dirs = dist, [d]
                elif dist == best_dist:
                    best_dirs.append(d)

        return random.choice(best_dirs)

    def remaining_km_with_diagonals(current, goal, cell_km):
        """대각선 이동 고려한 남은 거리(km)"""
        dx = abs(goal[0] - current[0])
        dy = abs(goal[1] - current[1])
        diag = min(dx, dy)
        straight = max(dx, dy) - diag
        return cell_km * (diag * math.sqrt(2) + straight)

    def speed_index_from_remaining_km(remaining_km, remaining_eta_min):
        """남은 거리/ETA로 목표 SOG 역산 후 속력 인덱스(0~25) 반환"""
        remaining_eta_min = max(1e-3, remaining_eta_min)
        sog_target = remaining_km / (0.0309 * remaining_eta_min)
        sog_target = max(5, min(sog_target, 30))
        idx = int(round(sog_target) - 5)
        idx = max(0, min(idx, 25))
        return idx, sog_target

    # ------------------------------------------------------------
    # ▶ 초기 설정
    # ------------------------------------------------------------
    grid_size = grid_size or (env.size, env.size)
    start = env.board.components["Player"].pos
    goal = env.board.components["Goal"].pos
    current = start

    done = False
    total_reward, total_oper, timestep = 0, 0, 0
    heu_ETA = ETA
    prev_dir = None

    speeds_idx, speeds_kn, headings, eca_bins = [], [], [], []

    if debug:
        print("\n=== Heuristic Benchmark Start ===")
        print(f"Grid: {grid_size}, Start: {start}, Goal: {goal}")
        print(f"Initial ETA: {ETA:.2f} min\n")
        print(render_board(current, goal, grid_size))
        print("-" * 60)

    # ------------------------------------------------------------
    # ▶ 메인 루프
    # ------------------------------------------------------------
    while not done and timestep < max_steps:
        action_dir = heu_direction(current, goal, prev_dir)
        remaining_km = remaining_km_with_diagonals(current, goal, env.distance)
        spd_idx, sog_kn = speed_index_from_remaining_km(remaining_km, heu_ETA)

        env.makeMove(action_dir)
        prev_dir = action_dir
        current = env.board.components["Player"].pos

        reward, done, heu_ETA = env.reward(action_dir, spd_idx, done, timestep, heu_ETA)

        total_reward += reward
        total_oper += env.p_operational
        timestep += 1

        speeds_idx.append(spd_idx)
        speeds_kn.append(round(sog_kn, 2))
        headings.append(action_dir)
        eca_bins.append(env.check_ECA())

        if debug:
            print(f"[t={timestep:03d}] Pos={current}, Dir={action_dir}, "
                  f"RemDist={remaining_km:.2f} km, "
                  f"Speed={sog_kn:.2f} kn, ETA={heu_ETA:.2f}, "
                  f"Reward={reward:.2f}, OperCost={env.p_operational:.2f}, "
                  f"ECA={int(eca_bins[-1])}")
            print(render_board(current, goal, grid_size))
            print("-" * 60)

    # ------------------------------------------------------------
    # ▶ 종료 및 결과
    # ------------------------------------------------------------
    if debug:
        print("=== Heuristic Summary ===")
        print(f"Steps: {timestep}, Done: {done}")
        print(f"Total Reward: {total_reward:.2f}, Operational Cost: {total_oper:.2f}")
        print(f"SOx: {env.SOx:.2f}, CO2: {env.CO2:.2f}, ETA left: {heu_ETA:.2f}")
        print(f"ECA Ratio: {sum(eca_bins)}/{len(eca_bins)} "
              f"({100 * sum(eca_bins)/len(eca_bins):.1f}%)" if eca_bins else "")

    return (
        total_reward,        # reward
        total_oper,          # accumulated operational cost
        timestep,            # step count
        heu_ETA,             # ETA left
        env.SOx,             # SOx emission
        env.CO2,             # CO2 emission
        speeds_idx,          # chosen speed indices
        headings,            # heading indices (0~7)
        eca_bins             # ECA binary timeline
    )
