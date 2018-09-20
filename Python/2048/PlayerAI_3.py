import math
import numpy as np
from BaseAI_3 import BaseAI

count = 0
MAX_COUNT = 1000
A1 = np.array([[16, 15, 14, 13],
               [9, 10, 11, 12],
               [8, 7, 6, 5],
               [1, 2, 3, 4]])
A2 = np.array([[16, 15, 12, 4],
               [14, 13, 11, 3],
               [10, 9, 8, 2],
               [7, 6, 5, 1]])
A3 = np.array([[16, 15, 14, 4],
               [13, 12, 11, 3],
               [10, 9, 8, 2],
               [7, 6, 5, 1]])
mats = [np.rot90(A, i) for A in (A1, A2, A3) for i in range(1, 5)]
mats.extend([A.T for A in mats])

class PlayerAI(BaseAI):

    @staticmethod
    def val(grid):
        global count
        count += 1
        max_tile = grid.getMaxTile()
        num_empty_cells = len(grid.getAvailableCells())
        B = np.array(grid.map)
        conv = max((np.sum(A * B) for A in mats))
        return conv + np.exp(num_empty_cells)

    @staticmethod
    def mini(grid, a, b, depth):
        if depth == 0:
            return None, PlayerAI.val(grid)
        cells = grid.getAvailableCells()
        if not cells:
            return None, PlayerAI.val(grid)

        min_child, min_util = None, math.inf
        for move in cells:
            child_grid = grid.clone()
            child_grid.setCellValue(move, 2)
            _, util = PlayerAI.maxi(child_grid, a, b, depth - 1)
            if util < min_util:
                min_child, min_util = move, util
            if min_util <= a:
                break
            if min_util < b:
                b = min_util
            if count > MAX_COUNT:
                break
        # for num in (2, 4):
        #     for move in cells:
        #         child_grid = grid.clone()
        #         child_grid.setCellValue(move, num)
        #         _, util = PlayerAI.maxi(child_grid, a, b, depth - 1)
        #         if util < min_util:
        #             min_child, min_util = move, util
        #         if min_util <= a:
        #             break
        #         if min_util < b:
        #             b = min_util
        return min_child, min_util

    @staticmethod
    def maxi(grid, a, b, depth):
        if depth == 0:
            return None, PlayerAI.val(grid)
        moves = grid.getAvailableMoves()
        if not moves:
            return None, PlayerAI.val(grid)

        max_child, max_util = None, -math.inf
        for child in moves:
            child_grid = grid.clone()
            child_grid.move(child)
            _, util = PlayerAI.mini(child_grid, a, b, depth - 1)
            if util > max_util:
                max_child, max_util = child, util
            if max_util >= b:
                break
            if max_util > a:
                a = max_util
            if count > MAX_COUNT:
                break
        return max_child, max_util

    @staticmethod
    def getMove(grid):
        global count
        count = 0
        max_depth = 6
        move, _ = PlayerAI.maxi(grid, -math.inf, math.inf, max_depth)
        # print("Count:", count)
        return move
