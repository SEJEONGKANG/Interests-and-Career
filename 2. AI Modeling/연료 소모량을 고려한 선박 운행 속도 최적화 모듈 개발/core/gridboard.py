# gridboard.py
import numpy as np
 
# ================================================================
# 유틸리티
# ================================================================
def addTuple(a, b):
    """2D 좌표 튜플 덧셈"""
    if isinstance(a, list):
        a = a[0]
    return tuple(sum(x) for x in zip(a, b))

def zip_positions2d(positions):
    """두 배열을 (x, y) 튜플 리스트로 묶기"""
    x, y = positions
    return list(zip(x, y))

# ================================================================
# 보드 구성요소 클래스
# ================================================================
class BoardPiece:
    """보드의 개별 구성요소(예: Player, Goal 등)"""
    def __init__(self, name, code, pos):
        self.name = name      # 구성요소 이름
        self.code = code      # 보드 표시 문자
        self.pos = pos        # 좌표 (tuple 또는 list of tuples)

# ================================================================
# GridBoard 클래스
# ================================================================
class GridBoard:
    """격자 기반 환경 보드"""
    def __init__(self, size):
        self.size = size
        self.components = {}   # {name: BoardPiece}
        self.masks = {}        # {name: mask_layer}

    # ------------------------------------------------------------
    # ▶ 구성요소 조작
    # ------------------------------------------------------------
    def addPiece(self, name, code, pos=(0, 0)):
        """보드에 새 구성요소 추가"""
        self.components[name] = BoardPiece(name, code, pos)

    def movePiece(self, name, pos):
        """구성요소 이동 (mask 충돌 검사 포함)"""
        if not self.masks:
            self.components[name].pos = pos
            return

        for mask in self.masks.values():
            if pos in zip_positions2d(mask.get_positions()):
                return  # 충돌 → 이동 금지
        self.components[name].pos = pos

    def delPiece(self, name):
        """구성요소 삭제"""
        if name in self.components:
            del self.components[name]

    # ------------------------------------------------------------
    # ▶ 렌더링
    # ------------------------------------------------------------
    def render(self):
        """보드를 문자형 2D 배열로 렌더링"""
        board = np.full((self.size, self.size), ' ', dtype='<U2')

        # 구성요소 표시
        for piece in self.components.values():
            positions = piece.pos if isinstance(piece.pos, list) else [piece.pos]
            for pos in positions:
                if 0 <= pos[0] < self.size and 0 <= pos[1] < self.size:
                    if board[pos] == ' ':
                        board[pos] = piece.code

        # 마스크 표시 (있을 경우)
        for mask in self.masks.values():
            try:
                x, y = mask.get_positions()
                board[x, y] = mask.code
            except Exception:
                continue

        return board

    def render_np(self):
        """보드를 다층 numpy 배열(채널 형태)로 렌더링"""
        num_layers = len(self.components) + len(self.masks)
        board_np = np.zeros((num_layers, self.size, self.size), dtype=np.uint8)
        layer = 0

        # 구성요소 레이어
        for piece in self.components.values():
            positions = piece.pos if isinstance(piece.pos, list) else [piece.pos]
            for pos in positions:
                if 0 <= pos[0] < self.size and 0 <= pos[1] < self.size:
                    board_np[layer, pos[0], pos[1]] = 1
            layer += 1

        # 마스크 레이어
        for mask in self.masks.values():
            try:
                x, y = mask.get_positions()
                z = np.full(len(x), layer)
                board_np[z, x, y] = 1
                layer += 1
            except Exception:
                continue

        return board_np
