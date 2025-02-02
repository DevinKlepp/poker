from typing import List

from game.card import Card


class Player:
    """A Player represents a poker player

    They have a name, an amount of chips, and private cards
    """

    def __init__(self, name: str, chips: int):
        self.name: str = name
        self.chips: int = chips
        self.cards: List[Card] = []

    def __repr__(self):
        print(f"Name: {self.name}, Chips: {self.chips}")
