import validity_checks
from bag import Bag
from rack import Rack
from board import Board
from square import Bonus
from user import User
from game import Game


if __name__ == "__main__":

    mike = User("Mickaël", 1703)
    print(mike)

    game = Game()
    print(game)

    # The color of the square under the H persists through changing the square's content to a Tile object.
    # This is normal behavior for now, it will be addressed later when the player places a word on the board.
    # That way, the bonus can be calculated for the play before it gets overwritten.
    # game.board.grid[7][3].content = game.bag.content[35]  # H
    # game.board.grid[7][4].content = game.bag.content[20]  # E
    # game.board.grid[7][5].content = game.bag.content[48]  # L
    # game.board.grid[7][6].content = game.bag.content[49]  # L
    # game.board.grid[7][7].content = game.bag.content[65]  # O
    # game.board.grid[7][7].bonus = Bonus.HAS_TILE          # Makes the letter bright white
    #
    # game.board.grid[6][7].content = game.bag.content[96]  # W
    # game.board.grid[8][7].content = game.bag.content[70]  # R
    # game.board.grid[9][7].content = game.bag.content[15]  # D
    # game.board.grid[10][7].content = game.bag.content[80] # S

    # print(type(bag.content[80])) # ok class Tile
    # print(type(board.grid[10][7])) # ok class Square

    # print(board.grid[10][7].content) # ok letter + subscript value
    # print(type(board.grid[10][7].content)) # ok class Tile

    print(game.board)
    game.board.display_detailed_board()

    # game.players[0].rack.tiles.append(game.bag.content[48]) # L
    # game.players[0].rack.tiles.append(game.bag.content[3])  # A
    # game.players[0].rack.tiles.append(game.bag.content[92]) # U
    # game.players[0].rack.tiles.append(game.bag.content[72]) # R
    # game.players[0].rack.tiles.append(game.bag.content[22]) # E
    # game.players[0].rack.tiles.append(game.bag.content[55]) # N
    # game.players[0].rack.tiles.append(game.bag.content[86]) # T
    # print(game.players[0].rack)

    # rack = Rack(15)       # custom rack size ok
    # rack.tiles.append(game.bag.content[48]) # L
    # rack.tiles.append(game.bag.content[3])  # A
    # rack.tiles.append(game.bag.content[92]) # U
    # rack.tiles.append(game.bag.content[72]) # R
    # rack.tiles.append(game.bag.content[22]) # E
    # rack.tiles.append(game.bag.content[55]) # N
    # rack.tiles.append(game.bag.content[86]) # T
    # rack.tiles.append(game.bag.content[49]) # L
    # rack.tiles.append(game.bag.content[21]) # E
    # rack.tiles.append(game.bag.content[69]) # Q
    # rack.tiles.append(game.bag.content[93]) # U
    # rack.tiles.append(game.bag.content[26]) # E
    # rack.tiles.append(game.bag.content[59]) # N
    # rack.tiles.append(game.bag.content[56]) # N
    # rack.tiles.append(game.bag.content[24]) # E
    # print(rack)

    print(game.bag)

    # print(validity_checks.word_is_valid("bonjour")) # valid ok
    # print(validity_checks.square_exists("H8", 15)) # valid ok
    # print(validity_checks.square_exists("8H", 15)) # valid ok
    # print(validity_checks.square_exists("a4", 15)) # valid ok
    # print(validity_checks.square_exists("A15", 15)) # valid ok
    # print(validity_checks.square_exists("1O", 15)) # valid ok (this is a 1 followed by the letter O)
    # print(validity_checks.square_exists("12", 15)) # invalid ok
    # print(validity_checks.square_exists("HI", 15)) # invalid ok
    # print(validity_checks.square_exists("24H", 15)) # invalid ok
    # print(validity_checks.square_exists("H24", 15)) # invalid ok
    # print(validity_checks.square_exists("H!8", 15)) # invalid ok
    # print(validity_checks.square_exists("H 8", 15)) # valid ok
    # print(validity_checks.square_exists(" !8", 15)) # invalid ok
    # # The following checks don't care if the square actually exists on a board of provided board_size length.
    # print(validity_checks.fits_on_board("bonjour", "H8", 15)) # valid ok
    # print(validity_checks.fits_on_board("bonjour", "8H", 15)) # valid ok
    # print(validity_checks.fits_on_board("bonjour", "a4", 15)) # valid ok
    # print(validity_checks.fits_on_board("bonjour", "A15", 15)) # false ok
    # print(validity_checks.fits_on_board("bonjour", "1O", 15)) # false ok (1 + letter O)
    # print(validity_checks.fits_on_board("bonjour", "12", 15)) # false ok
    # print(validity_checks.fits_on_board("bonjour", "HI", 15)) # false ok
    # print(validity_checks.fits_on_board("bonjour", "24H", 15)) # false ok
    # print(validity_checks.fits_on_board("bonjour", "H24", 15)) # false ok
    # print(validity_checks.fits_on_board("bonjour", "H!8", 15)) # false ok
    # print(validity_checks.fits_on_board("bonjour", "H 8", 15)) # valid ok
    # print(validity_checks.fits_on_board("bonjour", " !8", 15)) # false ok

    game.play_game()