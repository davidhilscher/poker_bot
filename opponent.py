import json
from pathlib import Path

DATA_FILE = Path("data/opponents.json")

class Opponent:
    def __init__(self, id: str = "", vpip=0.0, pfr=0.0, aggression=0.0, fold_to_cbet=0.0, showdown=0.0):
        self.id = id
        self.vpip = vpip
        self.pfr = pfr
        self.aggression = aggression
        self.fold_to_cbet = fold_to_cbet
        self.showdown = showdown

    def to_dict(self):
        return {
            "id": self.id,
            "vpip": self.vpip,
            "pfr": self.pfr,
            "aggression": self.aggression,
            "fold_to_cbet": self.fold_to_cbet,
            "showdown": self.showdown
        }

class OpponentDB:
    def __init__(self):
        self.opponents = {}
        self.load()

    def load(self):
        if DATA_FILE.exists():
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                for opp_id, stats in data.items():
                    self.opponents[opp_id] = Opponent(**stats)
        else:
            DATA_FILE.parent.mkdir(exist_ok=True)
            DATA_FILE.write_text("{}")

    def save(self):
        data = {opp_id: opp.to_dict() for opp_id, opp in self.opponents.items()}
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def update(self, opponent_id: str, **kwargs):
        opp = self.opponents.get(opponent_id, Opponent(id=opponent_id))
        for k, v in kwargs.items():
            if hasattr(opp, k):
                setattr(opp, k, v)
        self.opponents[opponent_id] = opp
        self.save()

    def get(self, opponent_id: str):
        return self.opponents.get(opponent_id)
