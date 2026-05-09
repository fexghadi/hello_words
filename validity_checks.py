from string import ascii_uppercase
from pylexique import Lexique383
from pprint import pprint
import unicodedata


# Removes all diacritics for a provided word. Used for checking against the similarly-trimmed set of valid words.
def remove_accents(word: str) -> str:
    nfkd = unicodedata.normalize('NFKD', word)
    return "".join([char for char in nfkd if not unicodedata.combining(char)])


# Creates a set containing all the valid words for a provided lexicon.
# Diacritics are fully removed; only base Unicode characters are retained. For example, "ö" becomes "o".
def create_clean_lexicon(lexicon) -> set:
    full_lexicon = lexicon
    clean_set = {remove_accents(unicodedata.normalize('NFKD', word)) for word in full_lexicon.lexique if word.isalpha()}
    del full_lexicon
    return clean_set


VALID_WORDS = create_clean_lexicon(Lexique383())


# Checks that the word exists in the provided lexicon.
# The official reference is the French dictionary called ODS, for Officiel Du Scrabble, by Larousse.
# However, we are using a different lexicon in this program, obtained from the "Pylexique" library.
# No exception is raised here; the treatment of the returned value happens in the Player.enter_word method.
def word_is_valid(word: str) -> bool:
    user_word = remove_accents(word.lower())
    return user_word in VALID_WORDS


# This function checks that the input coordinates exist on the board. Nothing more.
# It is used in a larger function below that validates a player's attempt to play a word on the board.
def square_exists(coordinates: str, board_size: int) -> bool:
    alphanum = coordinates.replace(" ", "").upper()
    if len(alphanum) == 2:
        if alphanum[0] in ascii_uppercase[:board_size] \
                and alphanum[1].isdigit() and 1 <= int(alphanum[1]) <= board_size:
            return True
        elif alphanum[1] in ascii_uppercase[:board_size] \
                and alphanum[0].isdigit() and 1 <= int(alphanum[0]) <= board_size:
            return True
    elif len(alphanum) == 3:
        if alphanum[0] in ascii_uppercase[:board_size] \
                and alphanum[1].isdigit() and alphanum[2].isdigit() and 1 <= int(alphanum[1:3]) <= board_size:
            return True
        if alphanum[2] in ascii_uppercase[:board_size] \
                and alphanum[0].isdigit() and alphanum[1].isdigit() and 1 <= int(alphanum[0:2]) <= board_size:
            return True
    return False


# This function checks whether the played word fits entirely on the board or not.
# The board_size variable should be provided by the (game.)board.size attribute.
# Works for sizes 1-99 but limited to 26 by design of using ascii_uppercase at board creation.
def fits_on_board(word: str, coordinates: str, board_size: int) -> bool:
    if square_exists(coordinates, board_size):
        word_length = len(word)
        alphanum = coordinates.replace(" ", "").upper()
        alphanum_length = len(alphanum)
        if alphanum[0].isalpha() and ord(alphanum[0]) - ord("A") <= board_size:
            if alphanum_length == 2 and alphanum[1].isdigit() and int(alphanum[1]) <= board_size:
                return int(alphanum[1]) + word_length <= board_size + 1
            elif alphanum_length == 3 and alphanum[1:3].isdigit() and int(alphanum[1:3]) <= board_size:
                return int(alphanum[1:3]) + word_length <= board_size + 1
        elif alphanum[-1].isalpha() and ord(alphanum[-1]) - ord("A") <= board_size:
            if alphanum_length == 2 and alphanum[0].isdigit() and int(alphanum[0]) <= board_size:
                return ord(alphanum[-1].upper()) - ord("A") + word_length <= board_size + 1
            elif alphanum_length == 3 and alphanum[0:2].isdigit() and int(alphanum[0:2]) <= board_size:
                return ord(alphanum[-1].upper()) - ord("A") + word_length <= board_size + 1
    return False


# ========== AI VERSION ==========
# def validate_move(word: str, coordinates: str, board_size: int) -> bool:
#     # 1. Clean and split the input
#     s = coordinates.replace(" ", "").upper()
#     word_len = len(word)
#
#     try:
#         if s[0].isalpha():  # Case: H1 (Horizontal)
#             col_start = ord(s[0]) - 64
#             row_fixed = int(s[1:])
#             # Boundary checks
#             if not (1 <= col_start <= board_size and 1 <= row_fixed <= board_size):
#                 return False
#             return (col_start + word_len - 1) <= board_size
#
#         else:  # Case: 1H (Vertical)
#             row_start = int(s[:-1])
#             col_fixed = ord(s[-1]) - 64
#             # Boundary checks
#             if not (1 <= row_start <= board_size and 1 <= col_fixed <= board_size):
#                 return False
#             return (row_start + word_len - 1) <= board_size
#
#     except (ValueError, IndexError):
#         return False
# ========== AI VERSION ==========