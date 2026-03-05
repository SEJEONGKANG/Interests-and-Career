import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import math
import matplotlib.patches as mpatches

def draw_route_map(
    ax,
    size,
    routes,
    speeds,
    ECAs,
    VSRZs,
    Lands,
    ghost_lines,
    wind_spd_kn,
    wind_dir_deg,
    title=None,
):
    """
    공통: 축(ax)에 항로/배경을 그려주는 함수.
    - ax: matplotlib Axes 객체
    - size: 그리드 사이즈 (정방형 가정)
    - routes: [(row, col), ...]
    - speeds: [속도(kn), ...]
    - ECAs, VSRZs, Lands: [(row, col), ...]
    - ghost_lines: [(x0c, y0c, x1c, y1c), ...] (보드 좌표 기준)
    - wind_spd_kn: 풍속(kn)
    - wind_dir_deg: 풍향(도, 0°=북, FROM 방향)
    """

    H = W = size

    # ==========================
    # 0. 색상 팔레트 (연한 톤)
    # ==========================
    sea_color   = "#e3f2fd"   # 아주 연한 파랑 (바다 기본)
    land_color  = "#dcedc8"   # 연한 초록 (육지)
    eca_color   = "#80deea"   # 밝은 시안 (ECA)
    vsrz_color  = "#ce93d8"   # 연한 보라 (VSRZ)

    # ==========================
    # 1. 축 기본 설정 + 그리드
    # ==========================
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.invert_yaxis()
    ax.set_aspect("equal")

    # 배경을 바다색으로
    ax.set_facecolor(sea_color)

    # 테두리 연한 그레이
    for spine in ax.spines.values():
        spine.set_color("#b0bec5")
        spine.set_linewidth(0.8)

    # 격자 (연한 회색)
    ax.set_xticks(np.arange(0, W + 1, 1), minor=True)
    ax.set_yticks(np.arange(0, H + 1, 1), minor=True)
    ax.set_xticks([])  # major tick 제거
    ax.set_yticks([])

    ax.grid(
        which="minor",
        color="#90a4ae",
        linestyle="-",
        linewidth=0.4,
        alpha=0.25,
    )

    # ==========================
    # 2. Land / ECA / VSRZ 타일
    #    - 바탕은 전부 바다색 (facecolor)
    #    - Land는 그 위에 연두색
    #    - ECA / VSRZ는 반투명으로 덮어쓰기
    #      → 둘 다 있는 칸은 색이 섞여서 다르게 보임
    # ==========================
    # Land
    for (r_, c_) in Lands:
        ax.add_patch(
            plt.Rectangle(
                (c_, r_),
                1,
                1,
                facecolor=land_color,
                edgecolor="#a5d6a7",
                linewidth=0.4,
                alpha=0.95,
                zorder=2,
            )
        )

    # ECA (반투명 시안)
    for (r_, c_) in ECAs:
        ax.add_patch(
            plt.Rectangle(
                (c_, r_),
                1,
                1,
                facecolor=eca_color,
                edgecolor=eca_color,
                linewidth=0.5,
                alpha=0.45,
                zorder=3,
            )
        )

    # VSRZ (반투명 연보라)
    for (r_, c_) in VSRZs:
        ax.add_patch(
            plt.Rectangle(
                (c_, r_),
                1,
                1,
                facecolor=vsrz_color,
                edgecolor=vsrz_color,
                linewidth=0.5,
                alpha=0.45,
                zorder=4,
            )
        )

    # ==========================
    # 3. 출발 / 도착점
    # ==========================
    if routes:
        # Start
        ax.scatter(
            routes[0][1] + 0.5,
            routes[0][0] + 0.5,
            s=80,
            color="#ef5350",
            edgecolor="#37474f",
            linewidth=0.8,
            label="Start",
            zorder=7,
        )
        # Goal
        ax.scatter(
            routes[-1][1] + 0.5,
            routes[-1][0] + 0.5,
            s=80,
            color="#42a5f5",
            edgecolor="#37474f",
            linewidth=0.8,
            label="Goal",
            zorder=7,
        )

    # ==========================
    # 4. 속도 기반 컬러 경로
    # ==========================
    if speeds and len(routes) >= 2:
        speed_vals = list(speeds)  # 원본 보호
        if len(speed_vals) > 1:
            speed_vals[-1] = speed_vals[-2]

        colors = [(1, 0.9, 0.3), (1, 0.7, 0.0), (0.96, 0.26, 0.21)]  # 밝은 노→주→빨
        cmap = LinearSegmentedColormap.from_list("speed_cmap", colors)
        norm = mcolors.Normalize(vmin=min(speed_vals), vmax=max(speed_vals))

        path_r, path_c = zip(*routes)
        xs = [c + 0.5 for c in path_c]
        ys = [r + 0.5 for r in path_r]

        for j in range(len(xs) - 1):
            ax.plot(
                [xs[j], xs[j + 1]],
                [ys[j], ys[j + 1]],
                color=cmap(norm(speed_vals[j])),
                lw=2.2,
                alpha=0.95,
                zorder=6,
            )
    else:
        if len(routes) >= 2:
            path_r, path_c = zip(*routes)
            xs = [c + 0.5 for c in path_c]
            ys = [r + 0.5 for r in path_r]
            ax.plot(xs, ys, lw=2.0, color="#1e88e5", zorder=6)

    # ==========================
    # 5. 드리프트 의도 방향 점선 화살표
    # ==========================
    ARROW_SCALE = 1.5
    for (x0c, y0c, x1c, y1c) in ghost_lines:
        vx, vy = (y1c - y0c), (x1c - x0c)
        ax.arrow(
            y0c,
            x0c,
            vx * ARROW_SCALE,
            vy * ARROW_SCALE,
            head_width=0.18,
            head_length=0.24,
            fc="none",
            ec="#455a64",
            alpha=0.7,
            lw=1.4,
            linestyle="--",
            zorder=8,
        )
        
    # ==========================
    # 6. 바람 정보 (화살표 + 텍스트)
    # ==========================
    # wind_dir_deg: FROM 각도 (어디서 불어오는지)
    # 화살표는 바람이 "불어가는 방향"을 보여주고 싶다면 +180
    rad = math.radians((wind_dir_deg + 180) % 360)

    # 화살표 중심: (0,0)~(1,1) 네 칸을 포함하는 2x2 블록의 정중앙 → (1, 1)
    center_x = 1.0
    center_y = 1.0

    # 길이는 블록 안에만 들어오도록 작게
    wlen = 1

    ax.arrow(
        center_x,
        center_y,
        math.sin(rad) * wlen,
        -math.cos(rad) * wlen,
        head_width=0.25,
        length_includes_head=True,
        fc="black",
        ec="black",
        lw=1.2,
        zorder=9,
    )

    # 바람 텍스트: (0,2) 셀 안에서 왼쪽 정렬
    # y=2.0 ~ 3.0 사이에 적당히 중앙에 두기 위해 2.5 근처에 배치
    ax.text(
        0.0 + 0.1,        # 살짝 안쪽으로
        2.0 + 0.5,
        f"Wind {wind_dir_deg:.0f}°, {wind_spd_kn:.1f} kn",
        fontsize=8,
        color="black",
        ha="left",
        va="center",
        zorder=9,
    )
    
    # ==========================
    # 7. 범례 & 타이틀
    # ==========================
    sea_patch = mpatches.Patch(
        facecolor=sea_color,
        edgecolor="#b0bec5",
        label="Sea",
    )
    land_patch = mpatches.Patch(
        facecolor=land_color,
        edgecolor="#a5d6a7",
        label="Land",
    )
    eca_patch = mpatches.Patch(
        facecolor=eca_color,
        edgecolor=eca_color,
        alpha=0.7,
        label="ECA",
    )
    vsrz_patch = mpatches.Patch(
        facecolor=vsrz_color,
        edgecolor=vsrz_color,
        alpha=0.7,
        label="VSRZ",
    )

    ax.legend(
        handles=[sea_patch, land_patch, eca_patch, vsrz_patch],
        loc="lower left",
        fontsize=7,
        framealpha=0.9,
    )

    if title:
        ax.set_title(title, fontsize=10, color="#37474f")

def plot_training_analysis(reward_list,
                           losses_dir, losses_speed,
                           SOx_emissions, CO2_emissions,
                           ETAs, num_of_timestep,
                           file_path="./results/", idx=0):
    """
    학습 epoch(episode)별 주요 지표 시각화
    - 보상 / 손실 / 배출량 / ETA / timestep 변화 추이
    """
    plt.figure(figsize=(14, 10))

    # ------------------------
    # (1) Reward
    # ------------------------
    plt.subplot(3, 2, 1)
    plt.plot(reward_list, label="Total reward")
    plt.xlabel("Epoch")
    plt.ylabel("Reward")
    plt.title("Reward per Epoch")
    plt.legend()
    plt.grid(True)

    # ------------------------
    # (2) Loss
    # ------------------------
    plt.subplot(3, 2, 2)
    plt.plot(losses_dir, label="Direction loss")
    plt.plot(losses_speed, label="Speed loss", alpha=0.7)
    plt.xlabel("Epoch")
    plt.ylabel("Loss (MSE)")
    plt.title("Training Loss")
    plt.legend()
    plt.grid(True)

    # ------------------------
    # (3) Emissions
    # ------------------------
    plt.subplot(3, 2, 3)
    plt.plot(SOx_emissions, label="SOx")
    plt.plot(CO2_emissions, label="CO2", alpha=0.7)
    plt.xlabel("Epoch")
    plt.ylabel("kg")
    plt.title("Emission per Episode")
    plt.legend()
    plt.grid(True)

    # ------------------------
    # (4) ETA 변화
    # ------------------------
    plt.subplot(3, 2, 4)
    plt.plot(ETAs)
    plt.xlabel("Epoch")
    plt.ylabel("ETA (min)")
    plt.title("ETA over Episodes")
    plt.grid(True)

    # ------------------------
    # (5) Timestep 변화
    # ------------------------
    plt.subplot(3, 2, 5)
    plt.plot(num_of_timestep)
    plt.xlabel("Epoch")
    plt.ylabel("Steps")
    plt.title("Number of Timesteps per Episode")
    plt.grid(True)

    plt.tight_layout()
    figname = f"{file_path}{idx}_training_analysis.png"
    plt.savefig(figname, dpi=200)
    plt.show()
    print(f"[saved] {figname}")
