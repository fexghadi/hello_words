import copy
from random import randint
from tile import Tile


class Bag:
    def __init__(self):
        self.initial_tileset : list[Tile] = Tile.create_tile_list()  # Meant to retain bag data at time of creation.
        # Useless so far, but could be useful to determine unseen tiles. List of opponents' racks is cleaner?
        # Create a list of played Tiles to determine "unseen tiles"? Sounds unnecessary. AI says it's better.
        # importing Collections can make it easier.
        self.content : list[Tile] = copy.deepcopy(self.initial_tileset)  # Will get emptied over the course of the game.

    def __str__(self):
        if len(self.content) == 0:
            return "Le sac est vide."
        print(f"Il reste {len(self.content)} lettres dans le sac.")
        choice = (input("Appuyez sur Entrée pour afficher l'ensemble des lettres restantes, "
                        "ou appuyez sur une autre touche pour afficher uniquement le contenu du sac. "))
        # For now, any input will display the full bag.
        return self.display_remaining_tiles(choice)

    # General method to turn a list of Tile objects into a display-ready string.
    @staticmethod
    def bag_list_to_string(remaining_tiles : list[Tile]) -> str:
        formatted_content = []
        for tile in remaining_tiles:
            if len(formatted_content) > 0 and tile.letter != formatted_content[-1]:
                formatted_content.append(" ")
            formatted_content += tile.letter
        return "".join(formatted_content)

    # Branching method based on the choice made in the print(bag) method.
    def display_remaining_tiles(self, choice : str) -> str:
        # if choice == "":                                          # TBA at a later point, not part of the MVP. todo
        #     display = (self.display_bag_and_unseen_tiles(Player.opponents))
        # else:
        display = self.display_tiles_in_bag()
        return display

    # Pretty straightforward..
    def display_tiles_in_bag(self) -> str:
        return self.bag_list_to_string(self.content)

    # TBA at a later point, not part of the MVP. todo, and also move this method into Game (or Player?)
    # For competitive integrity purposes. Allows the player to know all unseen tiles (bag content + opponent(s) rack(s))
    # def display_bag_and_unseen_tiles(self, opponents : list[Player] = None) -> str:
    #     if opponents is None or len(opponents) == 0:
    #         return self.bag_list_to_string(self.content)
    #     unseen_tiles = copy.deepcopy(self.content)      # Temporary variable to preserve the bag's integrity.
    #     for opponent in opponents:
    #         for tile in opponent.rack:
    #             unseen_tiles.append(tile)
    #     return self.bag_list_to_string(unseen_tiles)

    # Removes a Tile object from the bag. Used by the Rack class.
    def draw_tile(self) -> Tile:
        return self.content.pop(randint(0, len(self.content) - 1))