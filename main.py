from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from preflop import preflop_decision, HandTier
from opponent import OpponentDB
from pathlib import Path
import json, uvicorn

app = FastAPI(title="Poker Strategy Bot")
db = OpponentDB()

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

class AnalyzeRequest(BaseModel):
    hand: str
    position: str
    action: str
    opponent_id: str = "default"

class AnalyzeResponse(BaseModel):
    hand: str
    position: str
    action: str
    advice: str

class UpdateOpponentRequest(BaseModel):
    opponent_id: str
    vpip: float = 0.0
    pfr: float = 0.0 # preflop raise
    aggression: float = 0.0
    fold_to_cbet: float = 0.0 # higher should == + c-bet rate
    showdown: float = 0.0

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    path = BASE_DIR / "data" / "opponents.json"
    if path.exists():
        opponent_ids = list(json.load(open(path)).keys())
    else:
        opponent_ids = []
    if not opponent_ids:
        opponent_ids = ["opponent1"]
    return templates.TemplateResponse("index.html", {"request": request, "opponent_ids": opponent_ids})

# API enpoints below
@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    opp = db.get(req.opponent_id)
    advice = preflop_decision(req.hand, req.position, req.action, opp)

    if opp:
        if opp.fold_to_cbet > 0.65 and "Raise" in advice:
            advice += " (exploit: size up)"
        if opp.aggression > 0.75 and "Call" in advice:
            advice += " (expect pressure post)"

    return AnalyzeResponse(
        hand=req.hand,
        position=req.position,
        action=req.action,
        advice=advice
    )

@app.post("/update_opponent")
def update_opponent(req: UpdateOpponentRequest):
    db.update(req.opponent_id, vpip=req.vpip, pfr=req.pfr,
              aggression=req.aggression, fold_to_cbet=req.fold_to_cbet,
              showdown=req.showdown)
    return {"status": "ok", "opponent": req.opponent_id}

@app.get("/get_opponent/{opponent_id}")
def get_opponent(opponent_id: str):
    opp = db.get(opponent_id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opponent not found")
    return opp.to_dict()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, reload=True)


# Ignore
# uvicorn main:app --reload --host 127.0.0.1 --port 5000
# link:
# http://127.0.0.1:5000