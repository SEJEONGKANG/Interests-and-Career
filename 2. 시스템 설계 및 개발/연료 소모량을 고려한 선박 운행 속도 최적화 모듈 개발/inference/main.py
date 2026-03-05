# main.py
# python -m inference.main

import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
from datetime import datetime
import copy

from core.environment import *
from core.network import *
from rl.model_test import run_model_simulation
from rl.benchmark import benchmark_main
from core.visualize_results import draw_route_map

# ================================================================
# 설정
# ================================================================
idx = 0
file_path = 'results/'
os.makedirs(file_path, exist_ok=True)

size = 15
max_games = 30
start_time = time.time()
model_path = f'{file_path}{idx}_final.pt' # _best.pt / _final.pt

# ================================================================
# 모델 로드
# ================================================================
print(f"Loading trained model from {model_path}")
checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)

action_size_dir = 8
action_size_speed = 26
model = Dueling_Network(action_size_dir, action_size_speed)
model.load_state_dict(checkpoint['model_state'])
model.eval()
print("Model loaded successfully\n")

# ================================================================
# 통계용 변수 초기화
# ================================================================
test_results = []
test_results_raw = []

# 모델 결과
reward_list = []
SOx_emissions = []
CO2_emissions = []
ETAs = []
num_of_timestep = []

# 휴리스틱 결과
heu_reward_list = []
heu_oper_cost_list = []
heu_timestep_list = []
heu_ETA_list = []
heu_sox_list = []
heu_co2_list = []

# 행동 카운트
cnt_direction = [0] * action_size_dir
cnt_speed = [0] * action_size_speed

# ================================================================
# 모델 테스트 + 휴리스틱 baseline 30회 수행
# ================================================================
for i in range(max_games):
    print(f"\n=== Test {i+1}/{max_games} ===")

    # 1) 새 환경 생성
    base_env = Environment(size=size, mode='static')
    ETA = base_env.ETA

    # 2) 휴리스틱 baseline (같은 환경에서)
    env_heu = copy.deepcopy(base_env)
    heu_total_reward, heu_oper_cost, heu_timestep, heu_ETA, heu_sox, heu_co2, *_ = benchmark_main(env_heu, ETA)

    # 3) 모델 시뮬레이션 (역시 같은 환경 복사본에서)
    env_rl = copy.deepcopy(base_env)
    # run_model_simulation이 env를 인자로 받는다고 가정
    result = run_model_simulation(model, env=env_rl, display=False, size=size, max_steps=50, initial_ETA=ETA)

    # 전체 결과 unpack
    (r, oper_cost, t_ETA, timestep, routes, speeds, ECAs, VSRZs,
     sox, co2, in_ECAs, headings, actual_headings, ghost_lines,
     wind_spd, wind_dir_deg, Lands, ETA_history) = result

    # 4) 모델 통계 저장
    reward_list.append(r)
    SOx_emissions.append(sox)
    CO2_emissions.append(co2)
    ETAs.append(t_ETA)
    num_of_timestep.append(timestep)

    for d in headings:
        cnt_direction[d] += 1
    for s in speeds:
        if 0 <= s - 5 < len(cnt_speed):
            cnt_speed[s - 5] += 1

    # 5) 휴리스틱 통계 저장
    heu_reward_list.append(heu_total_reward)
    heu_oper_cost_list.append(heu_oper_cost)
    heu_timestep_list.append(heu_timestep)
    heu_ETA_list.append(heu_ETA)
    heu_sox_list.append(heu_sox)
    heu_co2_list.append(heu_co2)

    # 6) CSV용 요약 저장 (모델 + 휴리스틱)
    test_results.append([
        i,
        r, oper_cost, t_ETA, timestep, sox, co2,                 # 모델
        heu_total_reward, heu_oper_cost, heu_ETA, heu_timestep,  # 휴리스틱
        heu_sox, heu_co2,
        [speeds, headings, in_ECAs]                              # raw 액션 정보
    ])

    # 7) 전체 raw 결과 (시각화용)
    test_results_raw.append(result)

    print(f"Heuristic  -> Reward={heu_total_reward:.2f}, Oper cost={heu_oper_cost:.2f}, ETA={heu_ETA:.2f}")
    print(f"Model      -> Reward={r:.2f}, Oper cost={oper_cost:.2f}, ETA={t_ETA:.2f}")

# ================================================================
# 결과 저장 (CSV)
# ================================================================
test_df = pd.DataFrame(test_results, columns=[
    'idx',
    'total reward', 'total oper cost', 'ETA', 'timestep', 'SOx', 'CO2',  # 모델
    'heu reward', 'heu oper cost', 'heu ETA', 'heu timestep', 'heu SOx', 'heu CO2',
    'speed, headings, eca_bins'
])
csv_name = f"{file_path}{idx}_test_results.csv"
test_df.to_csv(csv_name, index=False)
print(f"\nSaved test results -> {csv_name}")

# ================================================================
# 시각화 
# ================================================================
def plot_all_results(
    all_results,
    reward_list,
    heu_reward_list,
    file_path,
    idx,
    size,
):
    """
    all_results: run_model_simulation() 결과 전체 리스트
    나머지 리스트: 통계/시각화용
    """

    # -----------------------------
    # 1) 각 에피소드 경로 시각화
    # -----------------------------
    n = len(all_results)
    if n == 0:
        return

    cols = min(3, n)
    rows = (n + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
    axes = np.array(axes).reshape(-1)  # 1D로 평탄화

    for run_idx, result in enumerate(all_results):
        (r, oper_cost, t_ETA, timestep, routes, speeds, ECAs, VSRZs,
         sox, co2, in_ECAs, headings, actual_headings, ghost_lines,
         wind_spd, wind_dir_deg, Lands, ETA_history) = result

        ax = axes[run_idx]
        draw_route_map(
            ax=ax,
            size=size,
            routes=routes,
            speeds=speeds,
            ECAs=ECAs,
            VSRZs=VSRZs,
            Lands=Lands,
            ghost_lines=ghost_lines,
            wind_spd_kn=wind_spd,
            wind_dir_deg=wind_dir_deg,
            title=f"Run {run_idx + 1}",
        )

    # 남는 subplot은 끄기
    for j in range(n, len(axes)):
        axes[j].axis("off")

    plt.tight_layout()
    route_img_path = os.path.join(file_path, f"{idx}_routes.png")
    plt.savefig(route_img_path, dpi=200)
    plt.close(fig)
    print(f"Saved route map figure -> {route_img_path}")

    # -----------------------------
    # 2) 보상 분포 (모델 vs 휴리스틱)
    # -----------------------------
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.hist(reward_list, bins=10, alpha=0.7, label='Model')
    ax2.hist(heu_reward_list, bins=10, alpha=0.7, label='Heuristic')
    ax2.set_title("Reward distribution (Model vs Heuristic)")
    ax2.set_xlabel("Total reward")
    ax2.set_ylabel("Count")
    ax2.legend()
    plt.tight_layout()
    hist_path = os.path.join(file_path, f"{idx}_reward_hist.png")
    plt.savefig(hist_path, dpi=200)
    plt.close(fig2)
    print(f"Saved reward histogram -> {hist_path}")

    # 필요하다면 여기에서 SOx/CO2, ETA 비교 플롯도 추가 가능


plot_all_results(
    all_results=test_results_raw,         # run_model_simulation() 결과 전체 리스트
    reward_list=reward_list,
    heu_reward_list=heu_reward_list,
    file_path=file_path,
    idx=idx,
    size=size,
)

# ================================================================
# 실행 시간 출력
# ================================================================
elapsed_time = time.time() - start_time
print(f"\nAll tests completed in {elapsed_time/60:.1f} min.")
print(f"Model     -> Mean reward: {np.mean(reward_list):.2f}, Mean ETA: {np.mean(ETAs):.2f}")
print(f"Heuristic -> Mean reward: {np.mean(heu_reward_list):.2f}, Mean ETA: {np.mean(heu_ETA_list):.2f}")
