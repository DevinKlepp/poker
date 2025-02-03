# Poker

My attempt at creating a No-Limit Texas Hold'em poker bot using Monte Carlo counterfactual regret minimization, as well as some optimization techniques

## Stages

1. Model the poker game
2. Introduce abstraction for bet sizes and hands to optimize
3. Implement some sort of algorithm

## Game

From [PokerStars](https://www.pokerstars.com/poker/games/texas-holdem/):

<details>
<summary>Rules</summary>

## No-Limit Texas Hold'em Rules (For Python Implementation)

## 1. Rules of the Game

- **Players:** Typically **2-10 players** per table.
- **Deck:** **52-card deck**, no jokers.
- **Objective:** Win chips by either:
  - Having the **best 5-card hand** at showdown.
  - **Forcing all other players to fold** before showdown.
- **Blinds:** Two players post **mandatory bets** (small blind & big blind) before the hand starts.
- **Betting:** **No limit** means any player can bet **any amount of their chips** at any time.
- **Community Cards:** **5 shared cards** are dealt face-up in three stages (**flop, turn, river**).
- **Hole Cards:** Each player gets **two private cards**.

---

## 2. Flow of the Game

1. **Blinds are posted**
   - Small blind (SB) and big blind (BB) are posted.
2. **Pre-Flop (First Betting Round)**
   - **Each player gets 2 hole cards** (private cards).
   - **Action starts from the player to the left of BB** and moves clockwise.
   - Players can call, raise, or fold.
   - Ends when all bets are equal or all but one player folds.
3. **Flop (Second Betting Round)**
   - **3 community cards are dealt face-up**.
   - Another round of betting starts from the **first active player left of the dealer**.
4. **Turn (Third Betting Round)**
   - **1 more community card is dealt**.
   - Another betting round follows, same as the flop.
5. **River (Final Betting Round)**
   - **Final community card is dealt**.
   - Last round of betting.
6. **Showdown (If 2+ Players Remain)**
   - Players reveal hands.
   - **Best 5-card hand wins** (combining hole cards + community cards).
   - If all but one player folds before showdown, the last remaining player wins **without showing their cards**.

---

## 3. Actions a Player Can Take

- **Fold:** Discard hand, forfeit the round.
- **Call:** Match the current bet.
- **Check:** If no bet is made, pass action to next player.
- **Bet:** If no bet has been made, place a bet.
- **Raise:** Increase the current bet amount.
- **All-in:** Bet all remaining chips.

---

## 4. When Rounds End

- **Betting rounds end when:**
  - All players have **matched the highest bet**, OR
  - All but one player **folds**.
- **Hand ends when:**
  - Showdown occurs and the best hand is determined, OR
  - All players but one fold.

---

## 5. How the Game is Resolved

- **If everyone folds except one player →** That player wins the pot.
- **If showdown occurs:**

  - Each player makes the **best 5-card hand** from **hole cards + community cards**.
  - Standard **poker hand rankings** determine the winner.
  - **Ties split the pot**.

---

## 6. How the Game Continues

- **If the game is to continue:**
  - All the roles are shifted to the left, in a clock-wise manner, from the dealer.
  - BB becomes SB, SB becomes dealer, dealer becomes a regular player.
  - **If there are only 2 players:**
    - The SB becomes the dealer, and the first to action is the BB.

## 7. Side Pots

Side pots were pretty tricky to implement, here are the guidelines:

In poker, when multiple side pots are created, they are resolved in the following order:

Last Side Pot First: The side pot created by the latest all-in bet is resolved first.
Work Backwards: After the first side pot is awarded, the process continues with the next-to-last side pot, and so on, until all side pots are resolved.
Main Pot Last: Finally, the main pot is awarded to the player with the best hand among all players who contributed to it.
Example:
Eligibility: Only players who contributed to a particular side pot are eligible to win it.

</details>

## Abstraction Optimizations

## Algorithm

For the algorithm to efficiently compute the ideal actions, we should use certain techniques at certain stages of the hand.

- Pre-Flop - The game tree is too large to solve in real time. We should rely on pre-computed (Blueprint) strategies, rather than real-time compute.
- Flop - If possible, we should try to use the pre-computed (Blueprint) strategy. Otherwise, use Monte-Carlo Linear CFR (MC-LCFR)
- Turn - If the remaining subgame is large (Lots of players), we should continue to use MC-LCFR. If there are very few players remaining, we could use Vector-based CFR
- River - Same as above. If the subgame is large, use MC-LCFR. Otherwise, we can use Vector-based CFR

"Pluribus used one of two different forms of CFR to compute a strategy in the subgame, depending on the size of the subgame and the part of the game. If the subgame is relatively large or it is early in the game, then Monte Carlo Linear CFR is used just as it was for the blueprint strategy computation. Otherwise, Pluribus uses an optimized vector-based form of Linear CFR ([38](https://ojs.aaai.org/index.php/AAAI/article/view/4007)) that samples only chance events (such as board cards) ([42](https://poker.cs.ualberta.ca/publications/AAMAS12-pcs.pdf))."

## Inspiration

Pluribus paper: https://www.science.org/doi/10.1126/science.aay2400

https://github.com/ozzi7/Poker-MCCFRM/tree/master

## Todo

- Add logic to compare hands to decide who wins a hand, account for ties
  - Odd chip remaining normally goes to the button (Person before SB), but we may be able to just let the dealer have it (Forget about it)
- Correct side-pot distribution logic
- Add early end if all players but one fold
- Treat players as indexes rather than the player object
- Add capability to reset the game to a new hand
- Fix next hand method

## Potential Improvements

- Instead of using a Card class to represent a unique card, I could use an integer instead, similar to what they do [here](https://github.com/worldveil/deuces/blob/master/deuces/card.py)
- I could write this in another language, like C++ or Rust, to improve computation speed
