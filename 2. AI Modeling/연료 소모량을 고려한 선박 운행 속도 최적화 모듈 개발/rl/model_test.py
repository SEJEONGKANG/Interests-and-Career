# model_test.py
import torch
import math
import numpy as np
from core.environment import *

# ================================================================
# 모델 테스트 (시뮬레이션)
# ================================================================
def run_model_simulation(model, size, display=True, max_steps=50, env=None, initial_ETA=None):
    """
    학습된 모델을 이용해 환경(Environment)을 시뮬레이션 테스트합니다.

    Args:
        model (torch.nn.Module): 학습된 네트워크
        size (int): Grid 크기
        display (bool): 출력 로그 표시 여부
        max_steps (int): 최대 이동 횟수

    Returns:
        tuple: (
            cumulative_reward, total_operational_cost, ETA, step_count,
            routes, speeds, ECAs, VSRZs, SOx, CO2,
            in_ECAs, intended_headings, actual_headings, ghost_lines
        )
    """
    # ------------------------------------------------------------
    # ▶ 초기화
    # ------------------------------------------------------------
    env = env
    ETA = env.ETA if initial_ETA is None else initial_ETA
    state = _compose_state_tensor(env)
    
    routes, speeds = [], []
    done = False
    status = 1
    step = 0
    cumul_r, oper_cost = 0.0, 0.0
    sox, co2 = 0.0, 0.0
    in_ECA_flag = 0

    # 기록용 리스트
    routes.append(env.board.components['Player'].pos)
    ECAs = env.board.components['ECA'].pos
    VSRZs = env.board.components['VSRZ'].pos
    headings, actual_headings, in_ECAs, ghost_lines = [], [], [], []
    eta_history = [ETA]  # 매 step의 ETA 기록

    # ------------------------------------------------------------
    # ▶ 시뮬레이션 루프
    # ------------------------------------------------------------
    while status == 1:
        # 모델 예측
        Q_dir, Q_speed = model(state)
        dir_idx = int(np.argmax(Q_dir.detach().cpu().numpy()))     # 0~7
        spd_idx = int(np.argmax(Q_speed.detach().cpu().numpy()))   # 0~25
        stw = spd_idx + 5

        if display:
            print(f"Step {step}: Action -> Heading {dir_idx}, Speed {stw} kn")

        prev_pos = env.board.components['Player'].pos

        # 이동 (풍향 영향 반영)
        env.makeMove(dir_idx)

        # 기록
        routes.append(env.board.components['Player'].pos)
        speeds.append(stw)
        headings.append(dir_idx)
        actual_headings.append(env.current_heading)

        if env.board.components['Player'].pos in ECAs:
            in_ECA_flag = 1
        in_ECAs.append(in_ECA_flag)

        # Drift 시 ghost line (시각화용)
        if env.current_heading != dir_idx:
            if display:
                print(f"  Wind drift! Intended {dir_idx} → Actual {env.current_heading}")
            ghost_lines.append(_make_ghost_line(prev_pos, dir_idx))

        # 보상 계산 및 상태 갱신
        reward, done, ETA = env.reward(env.current_heading, spd_idx, done, step, ETA)
        cumul_r += reward
        oper_cost += env.p_operational

        # 이번 step 종료 시점의 ETA 기록
        eta_history.append(ETA) 
        
        # wind / ETA 채널 갱신
        state = _compose_state_tensor(env, ETA)

        sox, co2 = env.SOx, env.CO2

        # 종료 조건
        if done:
            if display:
                print(f"Episode finished at step {step}")
            if -5 <= ETA <= 15:
                status = 2
                if display: print("Game WON (ETA within range)")
            else:
                status = 0
                if display: print("Game LOST (wrong ETA)")
        else:
            if display:
                print(f"   Reward = {reward:.2f}")

        step += 1
        if step > max_steps:
            if display:
                print("Game stopped: too many steps.")
            break

    # ------------------------------------------------------------
    # ▶ 결과 반환
    # ------------------------------------------------------------
    return (
        cumul_r, oper_cost, ETA, step, routes, speeds, ECAs, VSRZs,
        sox, co2, in_ECAs, headings, actual_headings, ghost_lines,
        env.wind_spd_kn, env.wind_dir_deg, env.board.components['Land'].pos,
        eta_history
    )

 
# ================================================================
# 내부 유틸리티
# ================================================================
def _compose_state_tensor(env, ETA=None):
    """보드 상태 + ETA + 바람 채널을 합친 상태 텐서 생성"""
    state_np = env.board.render_np()  # KW: Player, Goal, ECA, VSRZ, Land, Sea, ETA 채널 (7개)
    state = torch.from_numpy(state_np).unsqueeze(0).float()

    eta_val = env.ETA if ETA is None else ETA
    state[0, 6][state[0, 6] == 1] = eta_val  # KW: ETA 채널 인덱스 -1 -> 6으로 명시

    wind_speed = env.wind_spd_kn
    wind_dir = math.radians(env.wind_dir_deg)
    ws_norm = min(max(wind_speed / 40.0, 0.0), 1.0)
    ws_plane = torch.full_like(state[:, 0:1, :, :], ws_norm)
    sin_plane = torch.full_like(state[:, 0:1, :, :], math.sin(wind_dir))
    cos_plane = torch.full_like(state[:, 0:1, :, :], math.cos(wind_dir))

    return torch.cat([state, ws_plane, sin_plane, cos_plane], dim=1)  # KW: 총 10채널 (7 board + 3 wind)


def _make_ghost_line(prev_pos, intended_dir, scale=0.35):
    """풍향으로 틀어진 '의도된 방향'을 시각화할 점선 좌표 생성"""
    x0c, y0c = prev_pos[0] + 0.5, prev_pos[1] + 0.5
    dx, dy = DIR_DELTAS[intended_dir]
    x1c, y1c = x0c + dx * scale, y0c + dy * scale
    return (x0c, y0c, x1c, y1c)
