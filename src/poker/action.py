from enum import Enum


class Action(Enum):
    """The available actions the player or algorithm has to pick from.

    The BLUEPRINT action is used in the situations where the algorithm can
    check the blueprint to see the recommended course of action given the state of the game.
    If there isn't a recommendation in the blueprint, it must decide on another action.

    The algorithm will decide on a specific action using one of the 2 methods
    described earlier; MC-LCFR or Vector-based CFR, depending on the situation.
    """

    BLUEPRINT = 1
    CALL = 2
    RAISE = 3
    FOLD = 4
