import unittest
from hypothesis.strategies import integers
from hypothesis import given
import numpy as np

from game_metadata import BoardEntries, Player, Move
from game_model import GameBoard


class TestGameModel(unittest.TestCase):
    def setUp(self) -> None:
        self.starting_board = GameBoard()

    def test_game_is_over_when_no_block_is_empty(self):
        player_1_entries = np.random.randint(0, high=2, size=(
            self.starting_board.board_dimension, self.starting_board.board_dimension))
        player_2_entries = -1 * (1 - player_1_entries)
        self.starting_board.board = player_1_entries + player_2_entries
        self.assertTrue(self.starting_board.is_game_over())

    @given(integers(min_value=0, max_value=2))
    def test_player_winner_when_row_is_full(self, row: int):
        self.starting_board.board[row, :] = BoardEntries.X_entry
        self.assertTrue(self.starting_board.is_player_winner(player=Player.player_1))
        self.assertFalse(self.starting_board.is_player_winner(player=Player.player_2))

    @given(integers(min_value=0, max_value=2))
    def test_player_winner_when_column_is_full(self, col: int):
        self.starting_board.board[:, col] = BoardEntries.X_entry
        self.assertTrue(self.starting_board.is_player_winner(player=Player.player_1))
        self.assertFalse(self.starting_board.is_player_winner(player=Player.player_2))

    def test_player_winner_when_diagonal_is_full(self):
        self.starting_board.board = np.diag([BoardEntries.X_entry] * self.starting_board.board_dimension)
        self.assertTrue(self.starting_board.is_player_winner(player=Player.player_1))

    def test_invalid_move_is_rejected(self):
        self.starting_board.board[0, 0] = BoardEntries.X_entry
        starting_board_state = self.starting_board.board.copy()
        player_move = Move(row=0, col=0)
        self.starting_board.play_move(player_move)
        self.assertTrue(np.array_equal(starting_board_state, self.starting_board.board))


if __name__ == '__main__':
    unittest.main()
