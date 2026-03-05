# network.py
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from collections import deque
import random
 
# ================================================================
# Dueling DQN 네트워크
# ================================================================
class Dueling_Network(nn.Module):
    """
    Dueling DQN 구조로 구성된 신경망.
    - 방향(action_dir)과 속력(action_speed)을 동시에 예측.
    - ETA, 바람(풍속/방향)을 추가 채널로 입력받음.
    """
    def __init__(self, action_size_dir=8, action_size_speed=26, grid_size=15):
        super().__init__()
        self.in_channels = 10  # [P, G, VSRZ, ECA, Land, Sea, ETA, wind_speed, wind_sin, wind_cos] # KW: Land, Sea 채널 추가

        # CNN 피처 추출부
        self.conv1 = nn.Conv2d(self.in_channels, 32, kernel_size=3, stride=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)

        # Conv 출력 크기 자동 계산
        conv_out_size = self._get_conv_out_size(grid_size)
        self.feature_scaling = FeatureScalingLayer()

        # FC layers
        self.fc1 = nn.Linear(conv_out_size, 512)
        self.fc2 = nn.Linear(512, 256)

        # Dueling 구조
        self.advantage_fc = nn.Linear(256, 256)
        self.value_fc = nn.Linear(256, 256)

        self.advantage_head1 = nn.Linear(256, action_size_dir)
        self.advantage_head2 = nn.Linear(256, action_size_speed)
        self.value_head1 = nn.Linear(256, 1)
        self.value_head2 = nn.Linear(256, 1)

        self.action_size_dir = action_size_dir
        self.action_size_speed = action_size_speed

    def _get_conv_out_size(self, grid_size):
        """입력 grid 크기에 따른 Conv 출력 feature 크기 계산"""
        with torch.no_grad():
            x = torch.zeros(1, self.in_channels, grid_size, grid_size)
            x = self.conv3(self.conv2(self.conv1(x)))
        return int(np.prod(x.size()[1:]))

    def forward(self, state):
        """
        state tensor 구조:
        [0:P, 1:G, 2:VSRZ, 3:ECA, 4:Land, 5:Sea, 6:ETA, 7:wind_speed, 8:wind_sin, 9:wind_cos] # KW: Land, Sea 채널 추가
        """
        ETA_input = state[:, 6, :, :]  # KW: ETA 인덱스 4->6으로 변경
        wind_speed = state[:, 7, :, :]  # KW: wind_speed 인덱스 5->7로 변경
        wind_sin   = state[:, 8, :, :]  # KW: wind_sin 인덱스 6->8로 변경
        wind_cos   = state[:, 9, :, :]  # KW: wind_cos 인덱스 7->9로 변경

        grid = state[:, :6, :, :]  # KW: Player, Goal, VSRZ, ECA, Land, Sea (0-5번 채널)
        ETA_scaled = self.feature_scaling(ETA_input).unsqueeze(1)

        x = torch.cat((grid, ETA_scaled, wind_speed.unsqueeze(1),
                       wind_sin.unsqueeze(1), wind_cos.unsqueeze(1)), dim=1)  # KW: 총 10채널

        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1)

        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        adv = F.relu(self.advantage_fc(x))
        val = F.relu(self.value_fc(x))

        # Dueling heads
        adv_dir = self.advantage_head1(adv)
        adv_spd = self.advantage_head2(adv)

        val_dir = self.value_head1(val).expand(x.size(0), self.action_size_dir)
        val_spd = self.value_head2(val).expand(x.size(0), self.action_size_speed)

        # Q-value 계산
        q_dir = val_dir + (adv_dir - adv_dir.mean(dim=1, keepdim=True))
        q_spd = val_spd + (adv_spd - adv_spd.mean(dim=1, keepdim=True))
        return q_dir, q_spd


# ================================================================
# ETA Feature Scaling
# ================================================================
class FeatureScalingLayer(nn.Module):
    """ETA 값을 [0, 1] 범위로 정규화하는 모듈"""
    def __init__(self, max_value=225, min_value=-200):
        super().__init__()
        self.max_value = max_value
        self.min_value = min_value

    def forward(self, x):
        non_zero_mask = x != 0
        x = x.clone()
        x[non_zero_mask] = (x[non_zero_mask] - self.min_value) / (self.max_value - self.min_value)
        return x.clamp(0, 1)


# ================================================================
# Prioritized Replay Buffer
# ================================================================
class ReplayBuffer:
    """Prioritized Experience Replay Buffer"""
    def __init__(self, capacity, alpha=0.6):
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        self.priorities = np.zeros((capacity,), dtype=np.float32)
        self.pos = 0
        self.alpha = alpha

    def add(self, state1, action_dir, action_speed, reward, state2, done, valid_dirs_next, valid_speeds_next):
        """KW: 새 transition 추가 (valid actions 포함)"""
        transition = (state1, action_dir, action_speed, reward, state2, done, valid_dirs_next, valid_speeds_next)  # KW
        max_prio = self.priorities.max() if self.buffer else 1.0

        if len(self.buffer) < self.buffer.maxlen:
            self.buffer.append(transition)
        else:
            self.buffer[self.pos] = transition

        self.priorities[self.pos] = max_prio
        self.pos = (self.pos + 1) % self.buffer.maxlen

    def sample(self, batch_size, beta=0.4):
        """KW: 우선순위 기반 샘플링 (valid actions 포함)"""
        if len(self.buffer) == 0:
            raise ValueError("Replay buffer is empty.")

        if len(self.buffer) == self.buffer.maxlen:
            prios = self.priorities
        else:
            prios = self.priorities[:self.pos]

        probs = prios ** self.alpha
        probs /= probs.sum()

        indices = np.random.choice(len(self.buffer), batch_size, p=probs)
        samples = [self.buffer[idx] for idx in indices]

        total = len(self.buffer)
        weights = (total * probs[indices]) ** (-beta)
        weights /= weights.max()

        weights = torch.tensor(weights, dtype=torch.float32)
        state1_batch = torch.cat([s1 for (s1, _, _, _, _, _, _, _) in samples])  # KW: 8개 언패킹
        action_dir_batch = torch.tensor([a1 for (_, a1, _, _, _, _, _, _) in samples], dtype=torch.long)
        action_speed_batch = torch.tensor([a2 for (_, _, a2, _, _, _, _, _) in samples], dtype=torch.long)
        reward_batch = torch.tensor([r for (_, _, _, r, _, _, _, _) in samples], dtype=torch.float32)
        state2_batch = torch.cat([s2 for (_, _, _, _, s2, _, _, _) in samples])
        done_batch = torch.tensor([d for (_, _, _, _, _, d, _, _) in samples], dtype=torch.float32)
        valid_dirs_batch = [vd for (_, _, _, _, _, _, vd, _) in samples]  # KW: list of lists
        valid_speeds_batch = [vs for (_, _, _, _, _, _, _, vs) in samples]  # KW: list of lists

        return (state1_batch, action_dir_batch, action_speed_batch,
                reward_batch, state2_batch, done_batch, weights, indices,
                valid_dirs_batch, valid_speeds_batch)  # KW: mask 정보 추가

    def update_priorities(self, batch_indices, batch_priorities):
        """손실 기반 우선순위 갱신"""
        for idx, prio in zip(batch_indices, batch_priorities):
            if idx < len(self.priorities):
                self.priorities[idx] = prio

    def __len__(self):
        return len(self.buffer)
