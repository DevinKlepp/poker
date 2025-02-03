"""Player module."""

from typing import List
from poker.card import Card


class Player:
    """A Player represents a poker player.

    They have a name, an amount of chips, and private cards.

    Args:
        name (str): The player's name
        chips (int): The amount of chips the player has
    """

    def __init__(self, name: str, chips: int):
        if not name:
            raise Exception("A players name cannot be empty")
        if not chips:
            raise Exception("A player cannot start with 0 chips")

        self.name: str = name
        self.chips: int = chips
        self.cards: List[Card] = []
        self.current_bet = 0  # Tracks bets for the round
        self.in_hand = True  # Whether player is still active in the hand
        self.all_in = False

    def bet(self, amount: int) -> int:
        """Player bets a specified amount of chips.

        If the player doesn't have enough chips, they go all-in.

        Args:
            amount (int): The amount to bet
        """
        bet_amount = amount
        if amount >= self.chips:
            bet_amount = self.chips  # Go all-in if not enough chips
            self.all_in = True
        self.chips -= bet_amount
        self.current_bet += bet_amount
        return bet_amount

    def __repr__(self):
        return f"Name: {self.name}, Chips: {self.chips}"
