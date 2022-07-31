from copy import deepcopy
from multiprocessing.sharedctypes import Value
from typing import List, Tuple
import random

from game.chipcolors import ChipColors
from game.game import Game
from game.playable import Playable

class BennettW_Random(Playable):
    MAX_DEPTH = 5

    def __init__(self, color: ChipColors):
        super().__init__(color)

    def move(self, game_state: List[List[int]], available_moves: List[int], prev_moves: List[Tuple]) -> int:
        return self._minimax_search(game_state, available_moves)

    def _minimax_search(self, game_state: List[List[int]], available_moves: List[int]) -> Tuple:
        util_value, move = self._max_value(game_state, available_moves, self.color, 0)
        return move if move is not None else available_moves[random.randint(0, len(available_moves) - 1)]

    def _max_value(self, game_state: List[List[int]], availables_moves: List[int], color: ChipColors, depth: int) -> Tuple:
        if len(availables_moves) == 0:
            return self._utility(game_state, color), None
        if depth == self.MAX_DEPTH:
            return self._utility(game_state, color), None
        max_util_value = -float('inf')
        max_move = None
        for move in availables_moves:
            chip_row = Game.drop_chip(color, move, game_state)
            new_game_state = self._gen_new_game_state(game_state, chip_row, move, color)
            util_value, _ = self._min_value(new_game_state, Game.open_columns(new_game_state), ChipColors.get_opposite(color), depth + 1)
            if util_value > max_util_value:
                max_util_value = util_value
                max_move = move
        return max_util_value, max_move

    def _min_value(self, game_state: List[List[int]], availables_moves: List[int], color: ChipColors, depth: int) -> Tuple:
        if len(availables_moves) == 0:
            return self._utility(game_state, color), None
        if depth == self.MAX_DEPTH:
            return self._utility(game_state, color), None
        min_util_value = float('inf')
        min_move = None
        for move in availables_moves:
            chip_row = Game.drop_chip(color, move, game_state)
            new_game_state = self._gen_new_game_state(game_state, chip_row, move, color)
            util_value, _ = self._max_value(new_game_state, Game.open_columns(new_game_state), ChipColors.get_opposite(color), depth + 1)
            if util_value < min_util_value:
                min_util_value = util_value
                min_move = move
        return min_util_value, min_move

    def _utility(self, game_state: List[List[int]], color: ChipColors) -> int:
        return self._utility1(game_state, color)

    def _utility1(self, game_state: List[List[int]], color: ChipColors) -> int:
        open_cols = Game.open_columns(game_state)
        for col in open_cols:
            chip_row = Game.drop_chip(color, col, deepcopy(game_state))
            if Game.is_last_move_win(chip_row, col, game_state):
                return 10
            chip_row = Game.drop_chip(ChipColors.get_opposite(color), col, deepcopy(game_state))
            if Game.is_last_move_win(chip_row, col, game_state):
                return -10
        return 0

    def _gen_new_game_state(self, game_state: List[List[int]], row:int, col: int, color: ChipColors) -> List[List[int]]:
        new_game_state = deepcopy(game_state)
        new_game_state[row][col] = color
        return new_game_state

    @classmethod
    def get_name(cls) -> str:
        return "BennettW Minimax"