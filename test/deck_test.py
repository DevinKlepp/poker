from poker.card import Card
from poker.deck import Deck


# Test case 1: Ensure the deck is initialized with 52 cards
def test_deck_initialization():
    deck = Deck()
    assert len(deck.cards) == 52, "Deck should contain 52 cards initially"
    assert deck.total_cards == 52, "Total cards should be 52 initially"


# Test case 2: Ensure the shuffle function works (this test checks if the order of cards is shuffled)
def test_deck_shuffle():
    deck = Deck()
    original_deck = deck.cards.copy()
    deck.shuffle()
    assert deck.cards != original_deck, "Shuffling should change the order of the cards"


# Test case 3: Ensure dealing a card reduces the total cards and the deck size
def test_deal_card():
    deck = Deck()
    initial_total = deck.total_cards
    dealt_card = deck.deal()
    assert isinstance(dealt_card, Card), "Dealt card should be an instance of Card"
    assert (
        deck.total_cards == initial_total - 1
    ), "Total cards should decrease by 1 after dealing"
    assert (
        len(deck.cards) == initial_total - 1
    ), "Deck size should decrease by 1 after dealing a card"


# Test case 4: Ensure the deck is properly constructed with 52 unique cards (rank-suit pairs)
def test_deck_unique_cards():
    deck = Deck()
    seen_cards = set()
    for card in deck.cards:
        # Check that the card's rank and suit are unique
        card_repr = (card.rank, card.suit)
        assert card_repr not in seen_cards, f"Duplicate card found: {card_repr}"
        seen_cards.add(card_repr)
