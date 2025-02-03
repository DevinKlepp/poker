"""A module for running a game of No-Limit Texas Hold'em poker."""

from enum import Enum

from typing import List, Tuple
from poker.card import Card
from poker.deck import Deck
from poker.player import Player


class Action(Enum):
    """Represents a player's action in a game of poker."""

    FOLD = "fold"
    CALL = "call"
    RAISE = "raise"
    CHECK = "check"
    ALL_IN = "all-in"


class PokerGame:
    """An engine to run a No-Limit Texas Hold'em game

    The engine runs a single hand of poker, handling the betting rounds and showdown
    """

    def __init__(self, players: List[Player], big_blind: int):
        if len(players) < 2:
            raise ValueError("A poker game requires at least two players.")

        # Assign Players
        self.players = players
        self.active_players = players.copy()
        self.all_in_players = []
        self.players_excluded_from_winnings = {}

        # Initialize Deck
        self.deck = Deck()
        self.community_cards: List[Card] = []

        # Initialize Pots
        self.pot = 0
        # Side pots are stored in order of creation, with the
        # players and the amount they contributed
        self.side_pots: List[Tuple[List[Player], int]] = []

        # Initialize Blinds
        self.big_blind = big_blind
        self.small_blind = big_blind // 2
        self.current_bet = 0

        # Assign Blinds and Deal Hole Cards
        self.dealer_index = 0
        self.assign_blinds()
        self.deal_hole_cards()

    def assign_blinds(self):
        """Assigns blinds and posts the initial bets, forcing all-in if necessary."""
        # Assign blinds based on positioning
        small_blind_player = self.players[self.dealer_index % len(self.players)]
        big_blind_player = self.players[(self.dealer_index + 1) % len(self.players)]

        # Post blinds, forcing all-in if necessary
        # small_blind_bet = small_blind_player.bet(self.small_blind)
        # big_blind_bet = big_blind_player.bet(self.big_blind)

        self.handle_bet(small_blind_player, self.small_blind)
        self.handle_bet(big_blind_player, self.big_blind)

        # self.current_bet = max(small_blind_bet, big_blind_bet)

    def deal_hole_cards(self):
        """Deals two private cards to each player."""
        for player in self.players:
            player.cards = [self.deck.deal(), self.deck.deal()]

    def betting_round(self):
        """Handles a single round of betting."""
        # Should change this to: while len(self.active_players) > 1 and
        #
        for player in self.active_players:
            if player.all_in:
                continue  # All-in players don't act

            action = self.get_player_action(player)
            self.handle_action(player, action)

    def get_player_action(self, player: Player) -> Action:
        """Stub function to get player's action (to be replaced with actual decision-making)."""
        return Action.CHECK  # Placeholder

    def handle_action(self, player: Player, action: Action):
        """Handles a player's action."""
        if action == Action.FOLD:
            player.in_hand = False
            self.active_players.remove(player)
        elif action == Action.CALL:
            bet_amount = min(self.current_bet, player.chips)
            self.handle_bet(player, bet_amount)
        elif action == Action.RAISE:
            raise_amount = max(self.big_blind * 2, self.current_bet * 2)
            self.handle_bet(player, raise_amount)
            self.current_bet = raise_amount
        elif action == Action.ALL_IN:
            self.handle_bet(player, player.chips)

    def handle_bet(self, player: Player, amount: int):
        """Handles betting logic and side pot creation."""
        actual_bet = player.bet(amount)
        self.pot += actual_bet

        if player.all_in:
            self.all_in_players.append(player)
            self.active_players.remove(player)

            if actual_bet not in self.side_pots:
                self.side_pots[actual_bet] = 0
            self.side_pots[actual_bet] += actual_bet

    def play_hand(self):
        """Plays through a single hand of Texas Hold'em."""
        # Pre-Flop Betting
        self.betting_round()

        # Flop
        self.deal_community_cards(3)
        self.betting_round()

        # Turn
        self.deal_community_cards(1)
        self.betting_round()

        # River
        self.deal_community_cards(1)
        self.betting_round()

        self.resolve_showdown()

    def deal_community_cards(self, count: int):
        """Deals community cards."""
        for _ in range(count):
            self.community_cards.append(self.deck.deal())

    def compare_hands(self, players: List[Player]) -> List[Player]:
        """Compares the hands of the players and returns the winners.

        Removes players from contention for future side pots or the main
        pot if they lost the current comparison.
        """
        return []  # Placeholder

    def resolve_side_pots(self):
        """Resolves side pots among the winning players for that side pot."""
        while len(self.side_pots) > 0:
            side_pot = self.side_pots.pop()
            # Number of chips in the side pot is the bet amount x number of players in the side pot
            side_pot_chips = side_pot[1] * len(self.side_pots[0])
            winners = self.compare_hands(side_pot[0])

            if len(winners) > 1:
                # Divide the pot among the winners
                split_pot = side_pot_chips // len(winners)
                for winner in winners:
                    winner.chips += split_pot
            else:
                # Winner takes the pot
                winners[0].chips += side_pot_chips

    def resolve_main_pot(self):
        """Resolves the main pot among the winning players."""
        winners = self.compare_hands(self.active_players + self.all_in_players)
        if len(winners) > 1:
            # Divide the pot among the winners
            split_pot = self.pot // len(winners)
            for winner in winners:
                winner.chips += split_pot
        else:
            # Winner takes the pot
            winners[0].chips += self.pot

    def resolve_showdown(self):
        """Determines the winner at showdown, handling side pots."""
        all_contenders = self.active_players + self.all_in_players

        if len(all_contenders) == 1:
            winner = all_contenders[0]
            winner.chips += self.pot
            print(f"{winner.name} wins the entire pot of {self.pot} chips!")
            return

        # Resolve side pots if they are present
        if len(self.side_pots > 0):
            self.resolve_side_pots()

        # Resolve main pot
        self.resolve_main_pot()

    def next_hand(self):
        """Prepares for the next hand."""
        # Reset Player State
        for player in self.players:
            player.cards = []
            player.current_bet = 0
            player.in_hand = True
            player.all_in = False

        self.active_players = self.players.copy()
        self.all_in_players = []
        self.players_excluded_from_winnings = {}

        # Initialize Deck
        self.deck = Deck()
        self.community_cards: List[Card] = []

        # Reset Pots
        self.pot = 0
        self.side_pots = []

        # Reset Bet
        self.current_bet = 0

        # Increment Dealer Index
        self.dealer_index = (self.dealer_index + 1) % len(self.players)

        # Assign Blinds and Deal Hole Cards
        self.assign_blinds()
        self.deal_hole_cards()


# Example usage
starting_players: List[Player] = [
    Player("Alice", 1000),
    Player("Bob", 50),
    Player("Charlie", 200),
]
game = PokerGame(starting_players, big_blind=50)
game.play_hand()
