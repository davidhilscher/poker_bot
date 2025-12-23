from enum import Enum

class HandTier(Enum):
    PREMIUM = "premium"
    STRONG = "strong"
    PLAYABLE = "playable"
    MARGINAL = "marginal"
    TRASH = "trash"

PREMIUM_HANDS = {"AA", "KK", "QQ", "JJ", "AK", "AQS"}

rank = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10, "9": 9, "8": 8,
        "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}

def hand_tier(hand: str) -> HandTier:
    h = hand.upper().replace("10", "T").strip()
    suited = h.endswith("S")
    r1, r2 = h[0], h[1]
    v1, v2 = rank.get(r1, 0), rank.get(r2, 0)
    gap = abs(v1 - v2)

    # Check premiums first
    if h in PREMIUM_HANDS or (r1+r2 in PREMIUM_HANDS):
        return HandTier.PREMIUM

    # Pairs
    if gap == 0 and v1 >= 7:
        return HandTier.STRONG
    if gap == 0 and v1 <= 6:
        return HandTier.PLAYABLE

    # Suited connectors and one-gappers
    if suited:
        if gap == 1 and v1 >= 7:
            return HandTier.PLAYABLE
        if gap <= 2 and v1 >= 6:
            return HandTier.MARGINAL
        if v1 >= 11 and v2 >= 11:
            return HandTier.STRONG

    if not suited:
        if v1 >= 13 and v2 >= 12: # high cards
            return HandTier.STRONG
        if v1 >= 11 and v2 >= 10:
            return HandTier.PLAYABLE

    return HandTier.TRASH

def preflop_decision(hand, position, action, opp):
    tier = hand_tier(hand)

    if position == "BTN":
        if action == "Folded to you":
            if tier != HandTier.TRASH:
                return "Raise"
            return "Fold"
        if action == "Limp(s)":
            if tier in [HandTier.PREMIUM, HandTier.STRONG]:
                return "Raise (+ 1 BB/limper)"
            if tier in [HandTier.PLAYABLE, HandTier.MARGINAL]:
                return "Open small(2-3x BB)"
            return "Fold"
        if action in ["Raise","Raise + Call"]:
            if tier in [HandTier.PREMIUM, HandTier.STRONG]:
                return "3-bet"
            if tier in [HandTier.PLAYABLE, HandTier.MARGINAL]:
                return "Call"
            return "Fold"
        if action == "Raise + 3-bet":
            if tier == HandTier.PREMIUM:
                return "4-bet"
            return "Fold"

    if position in ["SB","BB"]:
        if action == "Folded to you":
            if tier != HandTier.TRASH:
                return "Raise"
            return "Fold/check from BB"
        if action == "Limp(s)":
            if tier in [HandTier.PREMIUM, HandTier.STRONG, HandTier.PLAYABLE]:
                return "Raise"
            if tier == HandTier.MARGINAL:
                return "Limp/Check"
            return "Fold"
        if action in ["Raise","Raise + Call"]:
            if tier == HandTier.PREMIUM:
                return "3-bet"
            if tier == HandTier.STRONG:
                return "Call"
            return "Fold"
        if action == "Raise + 3-bet":
            if tier == HandTier.PREMIUM:
                return "4-bet"
            return "Fold"

    if position in ["UTG","MP","CO"]:
        if action == "Folded to you":
            if tier in [HandTier.PREMIUM, HandTier.STRONG]:
                return "Raise"
            if tier in [HandTier.PLAYABLE, HandTier.MARGINAL] and position != "UTG":
                return "Open small"
            return "Fold"
        if action == "Limp(s)":
            if tier in [HandTier.PREMIUM, HandTier.STRONG]:
                return "Raise (+ 1 BB/limper)"
            if tier in [HandTier.PLAYABLE, HandTier.MARGINAL] and position != "UTG":
                return "Open small(2-3x BB)"
            return "Fold"
        if action in ["Raise","Raise + Call"]:
            if tier in [HandTier.PREMIUM, HandTier.STRONG]:
                return "3-bet"
            if tier in [HandTier.PLAYABLE, HandTier.MARGINAL] and position != "UTG":
                return "Call"
            return "Fold"
        if action == "Raise + 3-bet":
            if tier == HandTier.PREMIUM:
                return "4-bet"
            return "Fold"

    return "Fold"
