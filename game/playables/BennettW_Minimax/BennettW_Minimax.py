from typing import List, Tuple
import random

from game.chipcolors import ChipColors
from game.game import Game
from game.playable import Playable

class BennettW_Random(Playable):
    def __init__(self, color: ChipColors):
        super().__init__(color)

    def move(self, game_state: List[List[int]], available_moves: List[int]) -> int:
        return available_moves[random.randint(0, len(available_moves) - 1)]

    def _minimax_search(self, game_state: List[List[int]], available_moves: List[int]) -> Tuple:
        util_value, move = self._max_value(game_state, available_moves, self.color)
        return move

    def _max_value(self, game_state: List[List[int]], availables_moves: List[int], color: ChipColors) -> Tuple:
        if len(availables_moves) == 0:
            return self._utility(game_state, color), None
        max_util_value = -float('inf')
        max_move = None
        for move in availables_moves:
            chip_row = Game.drop_chip(color, move, game_state)
            new_game_state = list
            util_value, _ = self._min_value(new_game_state, self._get_available_moves(new_game_state), self._get_opponent_color(color))
            if util_value > max_util_value:
                max_util_value = util_value
                max_move = move
        return max_util_value, max_move

    def _min_value(self, game_state: List[List[int]], availables_moves: List[int], color: ChipColors) -> Tuple:
        if len(availables_moves) == 0:
            return self._utility(game_state, color), None
        min_util_value = float('inf')
        min_move = None
        for move in availables_moves:
            new_game_state = Game.drop_chip(color, move, game_state)
            util_value, _ = self._max_value(new_game_state, self._get_available_moves(new_game_state), self._get_opponent_color(color))
            if util_value < min_util_value:
                min_util_value = util_value
                min_move = move
        return min_util_value, min_move

    @classmethod
    def get_name(cls) -> str:
        return "BennettW Minimax"