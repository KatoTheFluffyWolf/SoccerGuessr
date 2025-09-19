from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
import os

# === Supabase Config ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY env vars")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
table = supabase.table("Daily Player")  # assumes today's row exists

# === FastAPI app ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://katothefluffywolf.github.io",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_methods=["GET","POST","OPTIONS"],
    allow_headers=["Content-Type"],
)

class Guess(BaseModel):
    guess: str

# --- Helpers -------------------------------------------------
def get_today_field(field: str):
    """
    Return a single field from the current 'Daily Player' row.
    If you store multiple days, add an order or filter here.
    """
    # Example: if you have a Date column, use:
    # q = table.select(field).order("Date", desc=True).limit(1)
    q = table.select(field).limit(1)
    resp = q.execute()
    rows = getattr(resp, "data", []) or []
    if not rows or field not in rows[0]:
        # Surface a 404 rather than throwing IndexError/KeyError
        raise HTTPException(status_code=404, detail=f"{field} not found")
    return rows[0][field]

# --- Hint endpoints ------------------------------------------
@app.get("/hint/name")
def hint_name():
    return get_today_field("Name")

@app.get("/hint/shirt-number")
def hint_shirt_number():
    return get_today_field("Shirt_number")

@app.get("/hint/profile-image")
def hint_image():
    return get_today_field("Profile_img_url")

@app.get("/hint/birthdate")
def hint_birthdate():
    return get_today_field("DOB")

@app.get("/hint/nationality")
def hint_nationality():
    return get_today_field("Nationality")

@app.get("/hint/market-value")
def hint_market_value():
    return get_today_field("Market_value")

@app.get("/hint/club-logo")
def hint_club_logo():
    return get_today_field("Club_logo")

@app.get("/hint/league")
def hint_league():
    return get_today_field("League")

@app.get("/hint/foot")
def hint_foot():
    return get_today_field("Foot")

@app.get("/hint/appearances")
def hint_appearances():
    return get_today_field("Appearances")

@app.get("/hint/goals")
def hint_goals():
    return get_today_field("Goals")

@app.get("/hint/yellow-cards")
def hint_yellow_cards():
    return get_today_field("Yellow_cards")

@app.get("/hint/red-cards")
def hint_red_cards():
    return get_today_field("Red_cards")

@app.get("/hint/minutes-played")
def hint_minutes_played():
    return get_today_field("Minutes_played")

@app.get("/hint/height")
def hint_height():
    return get_today_field("Height")

@app.get("/hint/position")
def hint_position():
    return get_today_field("Position")

# --- Submit guess --------------------------------------------
@app.post("/submit")
def check_answer(payload: Guess):
    true_answer = str(get_today_field("Name"))  # use helper, not the route
    correct = payload.guess.strip().lower() == true_answer.strip().lower()
    return {"correct": correct}
