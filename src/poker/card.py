"""This module contains the Card class, which represents a playing card."""

from typing import List, Set


def get_all_suits() -> Set[str]:
    """Returns a set of all possible suits in a deck of cards."""
    return {"hearts", "diamonds", "clubs", "spades"}


def get_all_ranks() -> List[str]:
    """Returns a list of all possible ranks in a deck of cards."""
    return [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "jack",
        "queen",
        "king",
        "ace",
    ]


class Card:
    """A Card represents a playing card

    A card can have a rank and a suit
    """

    def __init__(self, rank: str, suit: str):
        if rank not in get_all_ranks():
            raise Exception(f"The rank {rank} isn't found in the list of all ranks")
        if not suit in get_all_suits():
            raise Exception(f"The suit {suit} isn't found in the set of all suits")

        self.rank: str = rank
        self.suit: str = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"
