# main_inference.py
import os, math, time
from datetime import datetime
import numpy as np
import torch
import matplotlib
matplotlib.use('Agg')   # 비대화형 백엔드 (Tk 미사용)
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import math

from core.environment import Environment            # 환경/보상/드리프트 등 로직 사용 
from core.network import Dueling_Network            # Dueling DQN 구조 로드
from rl.model_test import run_model_simulation    # 공통 시뮬레이션 로직 재사용
from core.visualize_results import draw_route_map  

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RESULT_DIR = os.path.join(BASE_DIR, "app", "static", "infer")
MODEL_DIR  = os.path.join(BASE_DIR, "results")

os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

def _plot_single_run(
    size,
    routes,
    speeds,
    ECAs,
    VSRZs,
    Lands,
    ghost_lines,
    wind_spd_kn,
    wind_dir_deg,
    save_path,
):
    fig, ax = plt.subplots(figsize=(5, 5))
    draw_route_map(
        ax=ax,
        size=size,
        routes=routes,
        speeds=speeds,
        ECAs=ECAs,
        VSRZs=VSRZs,
        Lands=Lands,
        ghost_lines=ghost_lines,
        wind_spd_kn=wind_spd_kn,
        wind_dir_deg=wind_dir_deg,
        title="Simulated Route",
    )
    plt.tight_layout()
    plt.savefig(save_path, dpi=200)
    plt.close(fig)

def _nearest_sea(env, r, c):
    """(r,c)에서 가장 가까운 Sea 셀 (row, col)을 반환.
    이미 Sea면 그대로 반환. 동률이면 (row, col) 오름차순으로 결정.
    """
    size = env.size
    # 격자 범위로 클램프
    r = max(0, min(size - 1, int(r)))
    c = max(0, min(size - 1, int(c)))

    sea = env.board.components['Sea'].pos

    # 빠른 경로: 이미 Sea
    if (r, c) in sea:
        return (r, c)

    # 가장 가까운 Sea 탐색 (유클리드 거리의 제곱)
    best = None
    best_d2 = None
    for (sr, sc) in sea:
        d2 = (sr - r) * (sr - r) + (sc - c) * (sc - c)
        if best_d2 is None or d2 < best_d2 or (d2 == best_d2 and (sr, sc) < best):
            best = (sr, sc)
            best_d2 = d2

    # Sea가 비어있는 특이 케이스 대비
    return best if best is not None else (r, c)

def run_once(grid_i, grid_j, wind_dir_deg, wind_speed_ms,
             *, model_idx=0, size=15, max_steps=50):
    """
    프런트에서 받은 값으로 환경/모델을 고정 세팅 후 1회 실행하고 결과+시각화 반환.
    """
    # 0) 모델 로드
    model_path = os.path.join(MODEL_DIR, f"{model_idx}_final.pt")
    ckpt = torch.load(model_path, map_location="cpu", weights_only=False)
    model = Dueling_Network(8, 26)
    model.load_state_dict(ckpt["model_state"])
    model.eval()

    # 1) 환경 구성 (CSV 바람 비활성)
    env = Environment(size=size, mode='static', wind_csv_path=None)
     
    # 시작점 주입
    start_pos = _nearest_sea(env, grid_i, grid_j)
    env.board.components['Player'].pos = start_pos
    env.board.components['ETA'].pos = start_pos
    env.current_heading = None

    # 바람 주입: m/s → kn
    env.wind_dir_deg = float(wind_dir_deg) % 360
    env.wind_spd_kn  = max(0.0, float(wind_speed_ms) * 1.94384)   

    # 초기 목표 ETA 설정
    ETA = env.compute_ETA(speed_kn=15.0)   

    # 2) 공통 시뮬레이션 로직 호출
    sim_result = run_model_simulation(
        model,
        size=size,
        display=False,
        max_steps=max_steps,
        env=env,
        initial_ETA=ETA,
    )

    (cumul_reward, total_oper_cost, final_ETA, step_count,
     routes, speeds, ECAs, VSRZs, sox, co2, in_ECAs,
     headings, actual_headings, ghost_lines,
     wind_spd_kn, wind_dir_deg_sim, Lands,
     eta_history) = sim_result
    
    # 3) 시각화 저장 (static/infer/)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    fname = f"infer_{ts}.png"
    save_path = os.path.join(RESULT_DIR, fname)
    _plot_single_run(size, routes, speeds, ECAs, VSRZs, Lands, ghost_lines,
                     env.wind_spd_kn, env.wind_dir_deg, save_path)

    # 4) 응답 페이로드
    result = {
        "wind": f"{wind_dir_deg_sim:.1f}° {wind_spd_kn/1.94384:.2f} m/s",
        "rec_speed": round(float(np.mean(speeds)), 1) if speeds else None,
        "rec_speed_list": [round(float(s), 1) for s in speeds] if speeds else [],
        "eta": round(float(final_ETA), 1),
        "eta_history": [round(float(e), 3) for e in eta_history],
        "dir_idx": actual_headings, # 실제 항해 방향(바람 반영 후 heading)
        "intended_dir_idx": headings, # 의도한 heading
        "emission_sox": round(float(sox), 4),
        "emission_co2": round(float(co2), 4),
        "cost": -int(total_oper_cost),
        "viz_url": f"/static/infer/{fname}",
        "start_pos": [int(start_pos[0]), int(start_pos[1])],
    }
    return result

if __name__ == "__main__":
    # 테스트
    res = run_once(
        grid_i=12,
        grid_j=4,
        wind_dir_deg=90.0,
        wind_speed_ms=5.0,
        model_idx=0,
        size=15,
        max_steps=50,
    )
    print(res)