import validity_checks
from rack import Rack
from user import User


# Initializes a player from an already existing User, and adds an empty rack and a score of 0 to start the game.
class Player(User):
    def __init__(self, name, rating, rack_size = 7, timer: int = 1200):
        super().__init__(name, rating)
        self.rack = Rack(rack_size)
        self.score = 0
        self.timer = timer # exists but doesn't tick down yet.

    def __str__(self):
        return (f"{self.name} a marqué {self.score} points "
                f"et il lui reste {(self.timer // 60):02d}:{(self.timer % 60):02d} au chrono.")
