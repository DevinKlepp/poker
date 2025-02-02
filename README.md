# Poker

My attempt at creating a No-Limit Texas Hold'em poker bot using Monte Carlo counterfactual regret minimization, as well as some optimization techniques

## Stages

1. Model the poker game
2. Implement some sort of algorithm
3. Introduce abstraction for bet sizes and hands to optimize

### Algorithm

For the algorithm to efficiently compute the ideal actions, we should use certain techniques at certain stages of the hand.

- Pre-Flop - The game tree is too large to solve in real time. We should rely on pre-computed (Blueprint) strategies, rather than real-time compute.
- Flop - If possible, we should try to use the pre-computed (Blueprint) strategy. Otherwise, use Monte-Carlo Linear CFR (MC-LCFR)
- Turn - If the remaining subgame is large (Lots of players), we should continue to use MC-LCFR. If there are very few players remaining, we could use Vector-based CFR
- River - Same as above. If the subgame is large, use MC-LCFR. Otherwise, we can use Vector-based CFR

```
"Pluribus used one of two different forms of CFR to compute a strategy in the subgame, depending on the size of the subgame and the part of the game. If the subgame is relatively large or it is early in the game, then Monte Carlo Linear CFR is used just as it was for the blueprint strategy computation. Otherwise, Pluribus uses an optimized vector-based form of Linear CFR (38) that samples only chance events (such as board cards) (42)."
```

### Inspiration

https://www.science.org/doi/10.1126/science.aay2400
https://github.com/ozzi7/Poker-MCCFRM/tree/master
