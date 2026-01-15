# poker_bot
<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/5/52/Poker-sm.png" width="120" alt="Poker Logo"/>
</p>

# Poker Algorithm & Opponent Modeling

Tracking my Python poker algorithm project, including:

- Opponent modeling
- Hand evaluation
- Probabilistic decision making
- API deployment

---

## Project Status

- ✅ Core algorithm implemented
- ✅ Opponent modeling integrated
- ⚙️ API deployed via FastAPI

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)


Pre-flop decision bot for No Limit Texas Hold'em

Built and deployed a FastAPI-based poker strategy engine with algorithmic pre-flop logic, opponent modeling, JSON persistence, and a web UI. Designed REST endpoints and deployed on Render.


Currently focuses on preflop decision making to ensure deterministic, testable logic before expanding into postflop, also designed specifically for cash games to avoid tournament-specific dynamics such as ICM and blind escalation (I wanted an explainable preflop engine first, with abstractions I can later build on top off).


Caveats:

Assumes standard rake structure and stack size (does not account for extremes such as <40/>300 BB)

Assumes cash game. Rules/optimal play differs in tournament structure

Only accounts for pre-flop strategy, as EV is gained/lost most often pre-flop

Opponent modeling could likely be over-emphasized, sample size generally too small in most situations

Assumes live 1/3 player tendencies (Poker bot likely suboptimal past 2/5)

Opponent modeling only in backend



(Biggest challenge was ranking hands efficiently)

