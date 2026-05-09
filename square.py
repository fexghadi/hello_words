from unittest import case

import colorama

colorama.init(autoreset=True)
import tile
from string import ascii_uppercase
from enum import Enum


# Used to color bonus squares. Colors the foreground.
class Bonus(Enum):
    TW = "\033[91m"  # Red
    DW = "\033[95m"  # Magenta
    TL = "\033[94m"  # Blue
    DL = "\033[96m"  # Cyan
    HAS_TILE = "\033[97m" # White
    NONE = "\033[90m"  # Default (dark)


# Could this be a dataclass? todo
class Square:
    def __init__(self, row: str, col: int, bonus : Bonus = Bonus.NONE, content : tile.Tile | str = "\u2592\u2592\u2592"):
        self.row = row
        self.col = col
        self.bonus = bonus
        self.content = content

    # Conditional, verbose display of the content of a single square.
    # Called iteratively in the display_detailed_board method of the Board class to display every square.
    def __str__(self):
        bonus = f"a un bonus {self.bonus_to_string()} et " if self.bonus not in (Bonus.NONE, Bonus.HAS_TILE) else ""
        content = f"contient la lettre {self.content.letter}" if isinstance(self.content, tile.Tile) else "est vide"
        return f"La case {self.row}{self.col} {bonus}{content}."

    def bonus_to_string(self):
        match self.bonus:
            case Bonus.TW:
                return "mot compte triple"
            case Bonus.DW:
                return "mot compte double"
            case Bonus.TL:
                return "lettre compte triple"
            case Bonus.DL:
                return "lettre compte double"
            case _:
                return "pas de bonus"

    # This method is called by the board initializer.
    # str(row) is needed for the bonus assignments, before converting back into an int.
    # Currently limited to 26 columns by virtue of the call to ascii_uppercase.
    # board_size is already checked to be between 9 and 26 included at time of board initialization.
    @staticmethod
    def create_squares(board_size : int) -> list:
        squares = list(
            ([row, str(col), Bonus.NONE] for row in ascii_uppercase[:board_size:] for col in range(1, board_size + 1)))
        Square.assign_bonus(squares)
        layout = []
        for i in range(board_size):
            built_row = []
            for j in range(board_size):
                item = squares[board_size * i + j]
                item = Square(item[0], int(item[1]), item[2])
                built_row.append(item)
            layout.append(built_row)
        return layout

    # Assigns bonus multipliers to squares. Called by create_squares when the board is initialized.
    # The back-and-forth type conversion is handled by create_squares so that join() can work here.
    @staticmethod
    def assign_bonus(squares : list) -> list:
        for square in squares:
            if "".join(square[0:2]) in ["A1", "H1", "O1", "A8", "O8", "A15", "H15", "O15"]:
                square[2] = Bonus.TW  # Triple Word
            elif "".join(square[0:2]) in ["B2", "N2", "C3", "M3", "D4", "L4", "E5", "K5", "H8", "E11", "K11", "D12",
                                          "L12", "C13", "M13", "B14", "N14"]:
                square[2] = Bonus.DW  # Double Word
            elif "".join(square[0:2]) in ["F2", "J2", "B6", "F6", "J6", "N6", "B10", "F10", "J10", "N10", "F14", "J14"]:
                square[2] = Bonus.TL  # Triple Letter
            elif "".join(square[0:2]) in ["D1", "L1", "G3", "I3", "A4", "H4", "O4", "C7", "G7", "I7", "M7", "D8", "L8",
                                          "C9", "G9", "I9", "M9", "A12", "H12", "O12", "G13", "I13", "D15", "L15"]:
                square[2] = Bonus.DL  # Double Letter
        return squares

    # Placeholder to check whether a square already contains a tile.
    # Potential uses : crossing as well as hooking words.
    # Needs at least one TRUE when playing a word for the play to be valid, except on turn one.
    def has_tile(self):
        if self.bonus == Bonus.HAS_TILE:
            return True
        return False
