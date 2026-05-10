import copy
from random import randint
from enum import Enum
from bag import Bag
from board import Board
from player import Player
import validity_checks
from square import Bonus
from user import User
from tile import Tile


class Challenge(Enum):
    VOID = "Un mot invalide est automatiquement refusé par le programme, sans pénalité pour le joueur."
    # FIVE_POINTS = "Le joueur dont le mot est contesté reçoit 5 points supplémentaires si son coup est valide."
    # DOUBLE = "Le joueur qui conteste perd son tour si le coup de l'adversaire est valide."
    # TRIPLE = "Le joueur qui conteste perd LA PARTIE si le coup de l'adversaire est valide."


class Game:
    def __init__(self, players : list = None, board_size: int = 15, rack_size : int = 7,
                 challenge_type : Challenge = Challenge.VOID) -> None:
        if players is None:
            players = []
        if not players:
            player_to_add = input("Entrez le nom du joueur : ")
            # todo if player_to_add in user_database:
            # todo players.append(player_to_add) <= transform player_to_add into its User counterpart.
            counter = 0
            while True:
                players.append(User(player_to_add, 1500))   # So instead, for now we create new users each game.
                print(f"Le joueur {player_to_add} a été ajouté à cette partie.")
                counter += 1
                if counter == 2:
                # if counter == 4: # todo remove the line above after tests are done and MVP is running.
                    break
                player_to_add = input("Appuyez sur Entrée pour passer à l'étape suivante, "
                                      "ou entrez le nom du joueur suivant : ")
                if player_to_add == "":
                    break
        self.players = [Player(user.name, user.rating, rack_size) for user in players]
        self.board = Board(board_size)
        self.bag = Bag()
        self.turn = 1
        self.challenge_type = challenge_type
        self.acting_index = randint(0, len(self.players) - 1)

    def __str__(self):
        return "\n".join([player.__str__() for player in self.players])

    def enter_word(self, word: str = None) -> tuple:
        # todo need to separate different checks so they don't repeat
        while True:
            if word is None:
                word = input("Entrez le mot que vous souhaitez jouer, ou !! pour revenir en arrière : ")
            if word == "!!":
                return word, None
            word = validity_checks.clean_input(word)
            valid_word = validity_checks.word_is_valid(word)
            if not valid_word:
                print("Le mot entré est invalide.")
                word = None
                continue
            break
        while True:
            alphanum = input("Entrez la référence de la première case du mot joué, ou !! pour revenir en arrière "
                             "(lettre en premier pour un mot horizontal, chiffre en premier pour un mot vertical) : ")
            if alphanum == "!!":
                return word, alphanum
            alphanum = validity_checks.clean_input(alphanum)
            valid_alphanum = validity_checks.square_exists(alphanum, self.board.size)
            if not valid_alphanum:
                print("La référence indiquée n'est pas au bon format ou n'existe pas sur la grille.")
                continue
            fits = validity_checks.fits_on_board(word, alphanum, self.board.size)
            if not fits:
                print("Le mot entré est valide mais sort de la grille.")
                continue
            # todo need to add a step to check lexical validity of eventual words created along the way
            # if not valid_hooks:
            #     if len(invalid_hooks) == 1:
            #         print(f"Le mot {word} formé en raccord est invalide.")
            #     else:
            #         print(f"Mots incorrects formés en raccord : " + ", ".join([word for word in invalid_hooks]))
            break
        return word, alphanum

    def place_word(self, word : str, alphanum : str) -> bool:
        played_word = [letter for letter in word]
        word_length = len(word)
        acting_player = self.players[self.acting_index]
        available_tiles = copy.deepcopy(acting_player.rack.tiles)
        tiles_to_put_on_board = []
        score = 0
        word_multiplier = 1
        unavailable_tiles = []
        if alphanum[0].isalpha():
            alphanum_letter = ord(alphanum[0]) - ord("A")
            alphanum_number = int(alphanum[1:])
            for i in range(word_length):
                checked_square = self.board.grid[alphanum_letter][alphanum_number + i - 1]
                if checked_square.bonus == Bonus.HAS_TILE:
                    score += checked_square.content.value
                else:
                    added_to_tiles_to_put_on_board = False
                    for tile in available_tiles:
                        if tile.letter == played_word[i]:
                            added_to_tiles_to_put_on_board = True
                            match checked_square.bonus:
                                case Bonus.NONE:
                                    score += tile.value
                                case Bonus.DL:
                                    score += tile.value * 2
                                case Bonus.TL:
                                    score += tile.value * 3
                                case Bonus.DW:
                                    score += tile.value
                                    word_multiplier *= 2
                                case Bonus.TW:
                                    score += tile.value
                                    word_multiplier *= 3
                            tiles_to_put_on_board.append(tile)
                            available_tiles.remove(tile)
                            break
                    if not added_to_tiles_to_put_on_board:
                        unavailable_tiles.append(played_word[i])
            if unavailable_tiles:
                letters = (", ".join(letter for letter in unavailable_tiles)).rstrip(", ")
                print(f"Vous ne disposez pas des lettres suivantes : {letters}")
                return False
            skip_counter = 0
            for i in range(word_length):
                checked_square = self.board.grid[alphanum_letter][alphanum_number + i - 1]
                if checked_square.bonus == Bonus.HAS_TILE:
                    skip_counter += 1
                    continue
                else:
                    checked_square.content = tiles_to_put_on_board[i - skip_counter]
                    checked_square.bonus = Bonus.HAS_TILE
        else:
            alphanum_letter = ord(alphanum[-1]) - ord("A")
            alphanum_number = int(alphanum[0]) - 1 if len(alphanum) == 2 else int(alphanum[0:2]) - 1
            for i in range(word_length):
                checked_square = self.board.grid[alphanum_letter + i][alphanum_number]
                if checked_square.bonus == Bonus.HAS_TILE:
                    score += checked_square.content.value
                else:
                    added_to_tiles_to_put_on_board = False
                    for tile in available_tiles:
                        if tile.letter == played_word[i]:
                            added_to_tiles_to_put_on_board = True
                            match checked_square.bonus:
                                case Bonus.NONE:
                                    score += tile.value
                                case Bonus.DL:
                                    score += tile.value * 2
                                case Bonus.TL:
                                    score += tile.value * 3
                                case Bonus.DW:
                                    score += tile.value
                                    word_multiplier *= 2
                                case Bonus.TW:
                                    score += tile.value
                                    word_multiplier *= 3
                            tiles_to_put_on_board.append(tile)
                            available_tiles.remove(tile)
                            break
                    if not added_to_tiles_to_put_on_board:
                        unavailable_tiles.append(played_word[i])
            if unavailable_tiles:
                letters = (", ".join(letter for letter in unavailable_tiles)).rstrip(", ")
                print(f"Vous ne disposez pas des lettres suivantes : {letters}")
                return False
            skip_counter = 0
            for i in range(word_length):
                checked_square = self.board.grid[alphanum_letter + i][alphanum_number]
                if checked_square.bonus == Bonus.HAS_TILE:
                    skip_counter += 1
                    continue
                else:
                    checked_square.content = tiles_to_put_on_board[i - skip_counter]
                    checked_square.bonus = Bonus.HAS_TILE
        acting_player.rack.tiles = copy.deepcopy(available_tiles)
        score *= word_multiplier
        acting_player.score += score
        print(f"{acting_player.name}, vous venez de jouer le mot {word} en {alphanum} pour {score} points. "
              f"Votre score actuel est de {acting_player.score} points.")
        return True

    def take_turn(self) -> bool:
        first_display_of_turn = True
        while True:
            if first_display_of_turn:
                acting_player = self.players[self.acting_index]
                print(f"C'est au tour de {acting_player.name} !")
                first_display_of_turn = False
            print(f"{acting_player.name}, {acting_player.rack}")
            choice = (input(f"Voici vos options :\n"
                            f"1 --- Afficher toutes les lettres restantes.\n"  # todo doesn't work for now, defaults to choice 2 in Bag class method
                            f"2 --- Afficher uniquement les lettres du sac.\n"
                            f"3 --- Afficher la grille.\n"
                            f"4 --- Échanger des lettres.\n"  # todo restrict when len(bag) < 7
                            f"5 --- Passer votre tour.\n"
                            f"Ou entrez un mot pour le jouer.\n"
                            f"Votre choix : "))
            if choice == "1":
                continue  # todo
            elif choice == "2":
                print(self.bag.display_remaining_tiles(""))
            elif choice == "3":
                print(self.board)
            elif choice == "4":
                continue  # todo
            elif choice == "5":
                self.acting_index = (self.acting_index + 1) % len(self.players)
                return True
            elif choice.isalpha():
                word, alphanum = self.enter_word(choice)
                if word == "!!" or alphanum == "!!":
                    continue
                if not self.place_word(word, alphanum):
                    continue
                acting_player.rack.fill_rack(self.bag)
                if not acting_player.rack:
                    return False
                self.acting_index = (self.acting_index + 1) % len(self.players)
                break
            else:
                print("Le choix introduit n'est pas valable")
        return True



    def play_game(self):
        # Initializing game state.
        game_continues = True
        for player in self.players:
            player.rack.fill_rack(self.bag)
        # Main game loop.
        while game_continues:
            game_continues = self.take_turn()