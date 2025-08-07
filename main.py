from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os

# === Supabase Config ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === FastAPI app ===
app = FastAPI()

# === Allow CORS for your frontend ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://katothefluffywolf.github.io/SoccerGuessr/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

headers = {
    "User-Agent": "Mozilla/5.0"
}

table = supabase.table("Daily Player")

@app.get("/hint/name")
def hint_name():
    return table.select("Name").execute().data[0]["Name"]

@app.get("/hint/shirt-number")
def hint_shirt_number():
    return table.select("Shirt_number").execute().data[0]["Shirt_number"]

@app.get("/hint/profile-image")
def hint_image():
    return table.select("Profile_img_url").execute().data[0]["Profile_img_url"]

@app.get("/hint/birthdate")
def hint_birthdate():
    return table.select("DOB").execute().data[0]["DOB"]

@app.get("/hint/nationality")
def hint_nationality():
    return table.select("Nationality").execute().data[0]["Nationality"]

@app.get("/hint/market-value")
def hint_market_value():
    return table.select("Market_value").execute().data[0]["Market_value"]

@app.get("/hint/club_logo")
def hint_club():
    return table.select("Club_logo").execute().data[0]["Club_logo"]

@app.get("/hint/league")
def hint_league():
    return table.select("League").execute().data[0]["League"]

@app.get("/hint/foot")
def hint_foot():
    return table.select("Foot").execute().data[0]["Foot"]

@app.get("/hint/appearances")
def hint_appearances():
    return table.select("Appearances").execute().data[0]["Appearances"]

@app.get("/hint/goals")
def hint_goals():
    return table.select("Goals").execute().data[0]["Goals"]

@app.get("/hint/yellow-cards")
def hint_yellow_cards():
    return table.select("Yellow_cards").execute().data[0]["Yellow_cards"]

@app.get("/hint/red-cards")
def hint_red_cards():
    return table.select("Red_cards").execute().data[0]["Red_cards"]

@app.get("/hint/minutes-played")
def hint_minutes_played():
    return table.select("Minutes_played").execute().data[0]["Minutes_played"]

@app.get("/hint/height")
def hint_height():
    return table.select("Height").execute().data[0]["Height"]

@app.get("/hint/position")
def hint_position():
    return table.select("Position").execute().data[0]["Position"]

