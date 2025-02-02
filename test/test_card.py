import pytest
from poker.card import get_all_suits, get_all_ranks, Card


# Test get_all_suits function
def test_get_all_suits():
    suits = get_all_suits()
    assert isinstance(suits, set), "get_all_suits should return a set"
    assert suits == {
        "hearts",
        "diamonds",
        "clubs",
        "spades",
    }, "get_all_suits should return correct suits"


# Test get_all_ranks function
def test_get_all_ranks():
    ranks = get_all_ranks()
    expected_ranks = [
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
    assert isinstance(ranks, list), "get_all_ranks should return a list"
    assert ranks == expected_ranks, "get_all_ranks should return correct ranks"


# Test Card initialization with valid inputs
def test_card_creation_valid():
    card = Card("ace", "spades")
    assert card.rank == "ace", "Card should have correct rank"
    assert card.suit == "spades", "Card should have correct suit"


# Test Card initialization with an invalid rank
def test_card_invalid_rank():
    with pytest.raises(Exception) as exc_info:
        Card("joker", "spades")
    assert "The rank joker isn't found in the list of all ranks" in str(exc_info.value)


# Test Card initialization with an invalid suit
def test_card_invalid_suit():
    with pytest.raises(Exception) as exc_info:
        Card("ace", "stars")
    assert "The suit stars isn't found in the set of all suits" in str(exc_info.value)


# Test Card __repr__ method
def test_card_repr(capsys):
    card = Card("10", "hearts")
    card.__repr__()
    captured = capsys.readouterr()
    assert (
        captured.out.strip() == "10 of hearts"
    ), "Card __repr__ should print correctly"
