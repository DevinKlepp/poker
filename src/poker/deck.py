from random import shuffle
from typing import List
from poker.card import get_all_suits, get_all_ranks, Card


class Deck:
    """Represents a deck of 52 playing cards

    A deck can be shuffled and have cards dealt from it, reducing the total
    """

    def __init__(self):
        self.total_cards: int = 52
        self.cards: List[Card] = self.get_deck()
        self.shuffle()

    def shuffle(self):
        """Shuffles the deck of cards in-place"""
        shuffle(self.cards)

    def deal(self) -> Card:
        """Returns one card from the deck, reducing the total"""
        self.total_cards -= 1
        return self.cards.pop()

    def get_deck(self) -> List[Card]:
        """Returns a fresh deck of 52 cards"""
        suits = get_all_suits()
        ranks = get_all_ranks()
        deck: List[Card] = []

        for rank in ranks:
            for suit in suits:
                deck.append(Card(rank, suit))

        return deck
