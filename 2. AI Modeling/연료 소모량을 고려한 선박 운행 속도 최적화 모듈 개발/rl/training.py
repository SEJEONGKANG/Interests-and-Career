# training.py
import os
import time
import math
import copy
import random
import numpy as np
import torch
import torch.nn as nn
import pandas as pd
from IPython.display import clear_output
from datetime import datetime

from core.environment import *
from core.network import *
from core.visualize_results import plot_training_analysis
 
# ================================================================
# KW: Action Masking 유틸리티
# ================================================================
def apply_action_mask(q_values, valid_actions_batch):
    """
    KW: Batch별 valid actions만 남기고 나머지 -inf로 마스킹

    Args:
        q_values: (batch_size, action_size) Q-values
        valid_actions_batch: list of lists, 각 샘플의 유효한 액션 인덱스

    Returns:
        masked Q-values
    """
    batch_size = q_values.shape[0]
    action_size = q_values.shape[1]

    # KW: -inf 마스크 생성
    mask = torch.full_like(q_values, float('-inf'))

    # KW: 각 샘플의 유효한 액션만 0으로 설정
    for i in range(batch_size):
        valid_actions = valid_actions_batch[i]
        mask[i, valid_actions] = 0.0

    return q_values + mask  # invalid 액션은 -inf가 됨

# ================================================================
# 설정
# ================================================================
EPOCHS = 15000 # 15000 에폭에 하루 정도 소요
IDX = 1
RESULT_DIR = './results/'
os.makedirs(RESULT_DIR, exist_ok=True)

SAVE_EVERY = 3000
BEST_REWARD = -1e18
SYNC_FREQ = 50
EPS_INIT = 0.90
LEARNING_RATE = 1e-5
BATCH_SIZE = 256
CAPACITY = 10000
GAMMA = 0.99
SIZE = 15

# ================================================================
# 환경 및 모델 초기화
# ================================================================
env = Environment(size=SIZE, mode='static')
action_size_dir = 8
action_size_speed = 26

model = Dueling_Network(action_size_dir, action_size_speed)
target_model = copy.deepcopy(model)
target_model.load_state_dict(model.state_dict())

optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
loss_fn = nn.MSELoss()
replay = ReplayBuffer(CAPACITY)

# ================================================================
# 로그 변수
# ================================================================
eps = EPS_INIT
step_counter = 0
best_reward = BEST_REWARD
start_time = time.time()

cnt_direction = [0]*action_size_dir
cnt_speed = [0]*action_size_speed
num_timesteps, reward_list, reward_oper_list = [], [], []
losses_dir, losses_speed, ETAs = [], [], []
SOx_emissions, CO2_emissions, cnt_VSRIP = [], [], []

# ================================================================
# 학습 루프
# ================================================================
for epoch in range(EPOCHS):
    print(f"\n========== Epoch {epoch+1}/{EPOCHS} ==========")
    episode_start = time.time()

    env = Environment(size=SIZE, mode='static')
    ETA = env.ETA
    env.recommended_speed(ETA)

    # --- 상태 구성 (보드 + ETA 채널) ---
    state_np = env.board.render_np()
    state = torch.from_numpy(state_np).unsqueeze(0).float()
    state[0, -1][state[0, -1] == 1] = ETA

    # --------- wind 채널: 에피소드 시작 시 한 번만 계산 ----------
    wind_speed = env.wind_spd_kn
    wind_dir = math.radians(env.wind_dir_deg)
    ws_norm = min(max(wind_speed / 40.0, 0.0), 1.0)
    wind_sin, wind_cos = math.sin(wind_dir), math.cos(wind_dir)

    # state 크기에 맞춰 평면 생성
    ws_plane  = torch.full_like(state[:, 0:1, :, :], ws_norm)
    sin_plane = torch.full_like(state[:, 0:1, :, :], wind_sin)
    cos_plane = torch.full_like(state[:, 0:1, :, :], wind_cos)

    # 앞으로 계속 사용할 고정 wind_planes
    wind_planes = torch.cat([ws_plane, sin_plane, cos_plane], dim=1)

    # 초기 상태에 wind_planes concat
    state = torch.cat([state, wind_planes], dim=1)
    # -------------------------------------------------------------

    # --- 초기화 ---
    done = False
    move_count = 0
    total_reward = 0.0
    total_oper_cost = 0.0

    if (epoch + 1) % 50 == 0:
        eps = env.update_epsilon(eps)

    print(f"ETA={ETA:.1f}, epsilon={eps:.2f}")

    # ============================================================
    # Step Loop
    # ============================================================
    while not done:
        step_counter += 1
        move_count += 1

        # 1) 액션 선택
        action_dir, action_speed = env.select_action(
            model=model,
            state=state,
            action_size_dir=action_size_dir,
            action_size_speed=action_size_speed,
            epsilon=eps
        )
        cnt_direction[action_dir] += 1
        cnt_speed[action_speed] += 1

        # 2) 이동 및 다음 상태 구성
        moved, actual = env.makeMove(action_dir)

        if not moved:
            # 이동 실패 (육지로 가려 했거나 drift가 막힘)
            # 강한 패널티를 주고, ETA는 감소시키지 않는다.
            reward = -5.0
            done = False
            # ETA는 변화 없음
        else:
            reward, done, ETA = env.reward(actual, action_speed, done, move_count, ETA)
            
        total_reward += reward
        
        # 다음 상태(보드 + ETA) 구성
        next_state_np = env.board.render_np()
        next_state = torch.from_numpy(next_state_np).unsqueeze(0).float()
        next_state[0, 6][next_state[0, 6] != 0] = ETA  # KW: ETA 채널 인덱스 -1 -> 6으로 명시

        # --------- wind 업데이트 제거: 고정된 wind_planes 사용 ----------
        next_state = torch.cat([next_state, wind_planes], dim=1)
        # ---------------------------------------------------------------

        if not done:
            total_oper_cost += env.p_operational

        # KW: 다음 상태의 유효한 액션 마스크 계산
        next_valid_dirs, next_valid_speeds = env.get_valid_actions()

        # KW: Replay buffer에 mask 정보와 함께 저장
        replay.add(state, action_dir, action_speed, reward, next_state, done,
                   next_valid_dirs, next_valid_speeds)
        state = next_state

        # ========================================================
        # 학습 (Replay)
        # ========================================================
        if len(replay) > BATCH_SIZE:
            # KW: mask 정보 포함하여 샘플링
            s1, a_dir, a_spd, r_batch, s2, done_b, wts, idxs, valid_dirs_batch, valid_speeds_batch = replay.sample(BATCH_SIZE)
            Q1_dir, Q1_spd = model(s1)
            with torch.no_grad():
                Q2_dir, Q2_spd = target_model(s2)

                # KW: Target Q 계산 시 invalid 액션 마스킹 (-inf)
                Q2_dir_masked = apply_action_mask(Q2_dir, valid_dirs_batch)
                Q2_spd_masked = apply_action_mask(Q2_spd, valid_speeds_batch)

            # 방향 손실 (KW: masked target Q 사용)
            Y_dir = r_batch + GAMMA * ((1 - done_b) * torch.max(Q2_dir_masked, dim=1)[0])
            X_dir = Q1_dir.gather(1, a_dir.long().unsqueeze(1)).squeeze()
            loss_dir = loss_fn(X_dir, Y_dir.detach())

            # 속도 손실 (KW: masked target Q 사용)
            Y_spd = r_batch + GAMMA * ((1 - done_b) * torch.max(Q2_spd_masked, dim=1)[0])
            X_spd = Q1_spd.gather(1, a_spd.long().unsqueeze(1)).squeeze()
            loss_spd = loss_fn(X_spd, Y_spd.detach())

            # backprop
            clear_output(wait=True)
            optimizer.zero_grad()
            loss_dir.backward(retain_graph=True)
            loss_spd.backward(retain_graph=True)
            optimizer.step()

            # priority update
            new_prios = (loss_dir.detach().abs().cpu().numpy() + loss_spd.detach().abs().cpu().numpy()).flatten()
            new_prios = np.maximum(new_prios, 1e-5)
            replay.update_priorities(idxs, new_prios)

            # target sync
            if step_counter % SYNC_FREQ == 0:
                target_model.load_state_dict(model.state_dict())

    # ============================================================
    # 에피소드 종료 후 기록
    # ============================================================
    num_timesteps.append(move_count)
    reward_list.append(total_reward)
    reward_oper_list.append(total_oper_cost)
    losses_dir.append(loss_dir.item() if 'loss_dir' in locals() else np.nan)
    losses_speed.append(loss_spd.item() if 'loss_spd' in locals() else np.nan)
    ETAs.append(ETA)
    SOx_emissions.append(env.SOx)
    CO2_emissions.append(env.CO2)
    cnt_VSRIP.append(env.cnt_VSRIPmet)

    print(f"Total reward: {total_reward:.2f}, Moves: {move_count}")

    # ============================================================
    # 체크포인트 저장
    # ============================================================
    ckpt = {
        'epoch': epoch,
        'model_state': model.state_dict(),
        'target_state': target_model.state_dict(),
        'optimizer_state': optimizer.state_dict(),
        'epsilon': eps,
        'torch_rng': torch.get_rng_state(),
        'numpy_rng': np.random.get_state(),
        'python_rng': random.getstate(),
    }

    # 주기 저장
    if (epoch + 1) % SAVE_EVERY == 0:
        path = f"{RESULT_DIR}{IDX}_ep{epoch+1}_ckpt.pt"
        torch.save(ckpt, path)
        print(f"[CKPT] periodic checkpoint saved -> {path}")

    # 최고 리워드 모델 저장
    if total_reward > best_reward:
        best_reward = total_reward
        best_path = f"{RESULT_DIR}{IDX}_best.pt"
        torch.save(ckpt, best_path)
        print(f"[CKPT] new BEST (reward={total_reward:.2f}) -> {best_path}")

    print(f"Epoch {epoch} finished in {time.time()-episode_start:.1f}s")

# ================================================================
# 최종 모델 저장
# ================================================================
final_ckpt = {
    'epoch': EPOCHS - 1,
    'model_state': model.state_dict(),
    'target_state': target_model.state_dict(),
    'optimizer_state': optimizer.state_dict(),
    'epsilon': eps,
}
final_path = f"{RESULT_DIR}{IDX}_final.pt"
torch.save(final_ckpt, final_path)
print(f"\nTraining complete. Saved FINAL checkpoint -> {final_path}")

elapsed = (time.time() - start_time) / 60
print(f"Total training time: {elapsed:.1f} minutes")

# ==============================
# 학습 종료 후 시각화
# ==============================
plot_training_analysis(
    reward_list=reward_list,
    losses_dir=losses_dir,
    losses_speed=losses_speed,
    SOx_emissions=SOx_emissions,
    CO2_emissions=CO2_emissions,
    ETAs=ETAs,
    num_of_timestep=num_timesteps,
    file_path=RESULT_DIR,
    idx=IDX                                   
)