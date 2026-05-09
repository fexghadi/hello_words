import colorama

import tile

colorama.init(autoreset=True)
import copy
from square import Square


# Creates a new square board of size based on user's input. Default is 15 and will be used for this presentation.
# Typical Scrabble boards should allow words of length 8 to be playable, and because the board has to be symmetrical
# and needs a central tile, the minimum size is 9. The most common "giant scrabble" board format is 21x21.
# Some parts of the code are built around a board of size 15 though, so we will be using that for now, but most parts
# are already built to be usable regardless of size.
class Board:
    def __init__(self, size=15):
        # if 8 < size < 27:
        if size == 15:
            self.size = size
            self.initial_layout = Square.create_squares(self.size)
            self.grid = copy.deepcopy(self.initial_layout)  # Is a 2D list, each inner list represents a row.
        else:
            print("La taille de la grille n'est pas valide. Le minimum est 9, le maximum est 26.")

    # Displays a text-based representation of the board, square by square. That's a lot of lines !
    # Might turn this into a __repr_ ? todo
    def display_detailed_board(self) -> None:
        for row in self.grid:
            for square in row:
                print(square.__str__())

    # Displays a visual representation of the board.
    def __str__(self):
        board_state = "\n"
        board_state = self.label_columns(board_state)
        board_state = self.label_rows(board_state)
        board_state += "\n"
        return board_state

    # First board display builder. Creates column labels over two rows if there are more than then.
    # Color alternates between 1-9, 10-19, 20-26. All spacing is intentional.
    def label_columns(self, board_state: str) -> str:
        columns = [board_state]
        # Creates the top-most row to display double-digit column labels
        if self.size > 9:
            columns.append("   ")
            for i in range(1, self.size + 1):
                if i <= 9:
                    columns.append("    ")
                elif 9 < i <= 19:
                    columns.append(f"\033[92m{str(i)[0]}\033[0m   ")
                else:  # if "i" is between 20 and 26
                    columns.append(f"\033[93m{str(i)[0]}\033[0m   ")
            columns.append("\n")
        # Labels all row with the units' digit.
        for i in range(1, self.size + 1):
            if i == 1:
                columns.append("   ")
            if 9 < i <= 19:
                columns.append(f"\033[92m{i % 10}\033[0m   ")
            else:  # if "i" is single digit or between 20 and 26
                columns.append(f"\033[93m{i % 10}\033[0m   ")
        return "".join(columns)

    # Second board display builder. Takes care of displaying rows with their label + all the squares within.
    def label_rows(self, board_state : str) -> str:
        rows = [board_state]
        for i, row in enumerate(self.grid):
            # chr(65) is "A", 66 is "B", etc.
            row_label = chr(65 + i)
            squares = []
            for square in row:
                if isinstance(square.content, tile.Tile):
                    squares.append(f"{square.bonus.value} {square.content.letter} \033[0m")
                else:
                    squares.append(f"{square.bonus.value}{square.content}\033[0m")
            rows.append(f"\033[93m{row_label}\033[0m {" ".join(squares)} ")
        return "\n".join(rows)


