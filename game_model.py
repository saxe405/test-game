from dataclasses import dataclass
from typing import List

import numpy as np

from game_metadata import Move, Player, BoardEntries


@dataclass
class GameBoard:
    board: np.ndarray
    player_turn: Player
    board_dimension: int

    def __init__(self):
        self.board_dimension = 3
        self.board = np.zeros((self.board_dimension, self.board_dimension))
        self.player_turn = Player.player_1

    def all_moves(self) -> List[Move]:
        return [Move(row=x, col=y) for x in range(self.board_dimension) for y in range(self.board_dimension)]

    def is_game_over(self) -> bool:
        if self.is_there_a_winner():
            return True
        elif len(self.valid_moves()) == 0:
            return True
        else:
            return False

    def game_status(self) -> str:
        if self.is_player_winner(player=Player.player_1):
            return 'Player one wins!'
        elif self.is_player_winner(player=Player.player_2):
            return 'Player two wins!'
        elif self.is_game_over():
            return 'Tie!'
        else:
            return f'Turn of Player {self.player_turn.value}'

    def is_player_winner(self, player: Player) -> bool:
        entry_to_test = BoardEntries.X_entry if player == Player.player_1 else BoardEntries.O_entry
        sum_to_test = self.board_dimension * entry_to_test
        if any(self.board.sum(axis=1) == sum_to_test):  # row comparison
            return True
        elif any(self.board.sum(axis=0) == sum_to_test):  # column comparison
            return True
        elif self.board.trace() == sum_to_test or self.board[::-1].trace() == sum_to_test:
            return True
        return False

    def is_there_a_winner(self) -> bool:
        return self.is_player_winner(player=Player.player_1) or self.is_player_winner(player=Player.player_2)

    def is_game_tied(self) -> bool:
        if self.is_there_a_winner():
            return False
        elif self.is_game_over():
            return True

    def is_valid_move(self, move: Move) -> bool:
        if self.board[move.row, move.col] != BoardEntries.Blank:
            return False
        return True

    def valid_moves(self) -> List[Move]:
        return [m for m in self.all_moves() if self.is_valid_move(move=m)]

    def play_move(self, move: Move) -> None:
        if not self.is_valid_move(move=move):
            # add feedback to user to retry
            return
        entry = BoardEntries.X_entry if self.player_turn == Player.player_1 else BoardEntries.O_entry
        self.board[move.row, move.col] = entry
        self.player_turn = Player.player_1 if self.player_turn == Player.player_2 else Player.player_2

    def reset_game(self) -> None:
        self.__init__()

    def print_board_state(self) -> None:
        for row in range(self.board_dimension):
            print(' '.join([board_entry_to_print_form(self.board[row, col]) for col in range(self.board_dimension)]))


def board_entry_to_print_form(entry: int):
    if entry == BoardEntries.X_entry:
        return 'X'
    elif entry == BoardEntries.O_entry:
        return 'O'
    else:
        return '.'
