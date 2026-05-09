from tile import Tile


# Initializes a rack to contain the player's tiles. Default size is 7 but can be modified for special game modes.
class Rack:
    def __init__(self, size = 7):
        self.size = size
        self.tiles : list[Tile] = []

    def __str__(self):
        display_rack = []
        for tile in self.tiles:
            display_rack.append(f"{tile.letter}{tile.value_small}")
        return f"Vos lettres sont : {" ".join(sorted(display_rack))}"

    def pop(self, index : int = -1):
        return self.tiles.pop(index)

# This method pulls tiles one by one out of the bag by repeatedly
# calling the draw_tile function until the player's rack is full or the bag is empty.
# This method does not make more calls to the draw_tile function than are necessary.
    def fill_rack(self, bag) -> None:
        for _ in range(min(len(bag.content), self.size - len(self.tiles))):
            self.tiles.append(bag.draw_tile())
        if len(bag.content) == 0:
            print(bag)