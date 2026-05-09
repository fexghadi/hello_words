# Initializes a new User with a name, and a default rating of 1000 that can be modified.
class User:
    def __init__(self, name, rating = 1000):
        self.name = name
        self.rating = rating


    def __str__(self):
        return f"L'utilisateur {self.name} a un rating de {self.rating}"