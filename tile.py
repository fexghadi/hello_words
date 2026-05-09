from string import ascii_uppercase


class Tile:
    SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

    def __init__(self, letter, value):
        self.letter = letter
        self.value = value
        self.value_small = str(value).translate(self.SUB)

    def __str__(self):
        return f"{self.letter}{self.value_small}"

    # Fully-functional method to initialize a list of tiles, either by default or with user input.
    # The implementation is a dictionary, with letters as keys (str) and (score, quantity) as values in a tuple.
    # Using the letter as a single key rather than a key+score pair is an easy solution for access.
    @staticmethod
    def create_tile_list() -> list[Tile]:
        tiles_dict = dict()
        custom_tiles = input(
            "Appuyez sur Entrée pour utiliser les lettres standard, "
            "ou appuyez sur une autre touche pour personnaliser la valeur et la quantité de chaque lettre. ")
        if not custom_tiles:
            tiles_dict = {
                        "A": (1, 9), "B": (3, 2), "C": (3, 2), "D": (2, 3), "E": (1, 15), "F": (4, 2), "G": (2, 2),
                        "H": (4, 2), "I": (1, 8), "J": (8, 1), "K": (10, 1), "L": (1, 5), "M": (2, 3), "N": (1, 6),
                        "O": (1, 6), "P": (3, 2), "Q": (8, 1), "R": (1, 6), "S": (1, 6), "T": (1, 6), "U": (1, 6),
                        "V": (4, 2), "W": (10, 1), "X": (10, 1), "Y": (10, 1), "Z": (10, 1), "?": (0, 2)
                        }
        else:
            for char in ascii_uppercase + "?":
                incorrect_input = True
                while incorrect_input:
                    try:
                        val = int(input(f"Entrez la valeur de la lettre {char} : "))
                        qty = int(input(f'Entrez la quantité de "{char}" à ajouter dans le sac : '))
                        tiles_dict[char] = (val, qty)
                        incorrect_input = False
                    except ValueError:
                        print("Valeur invalide, veuillez réessayer.")
        tiles = Tile.create_tiles(tiles_dict)
        return tiles

    @staticmethod
    def create_tiles(tiles_dict : dict) -> list[Tile]:
        tiles = []
        for letter in tiles_dict:
            qty = tiles_dict[letter][1]
            for _ in range(qty):
                tiles.append(Tile(letter, tiles_dict[letter][0]))
        return tiles