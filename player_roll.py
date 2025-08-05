
!pip install supabase -q
from datetime import datetime
from supabase import create_client, Client
import requests
from bs4 import BeautifulSoup
import random


# === Supabase Config ===
SUPABASE_URL = "https://fvcapchuqxfelruvodyg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ2Y2FwY2h1cXhmZWxydXZvZHlnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0OTUzNjMyNCwiZXhwIjoyMDY1MTEyMzI0fQ.FG_xQYfvj88Wn-kd9hX7sYUkiDFZVl7Dd_PWblP5ECU"  # use service key for backend

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def player_roll():
    today = datetime.now().strftime('%Y-%m-%d')

    response = supabase.table("SoccerPlayerURLs").select("ID, url").eq("used", False).execute()
    player_urls = response.data

    if not player_urls:
        raise Exception("No unused player URLs available.")

    selected = random.choice(player_urls)
    selected_id = selected["ID"]
    random_url = selected["url"]

    supabase.table("Daily Player").upsert({
        "id": 1,
        "Date": today,
        "Player_ID": selected_id,
        "Daily_URL": random_url
    }).execute()

    #supabase.table("SoccerPlayerURLs").update({"used": True}).eq("ID", selected_id).execute()

    print(f"✅ Daily player set: ID={selected_id}, URL={random_url}")

# This line ensures the function runs when testing locally
if __name__ == "__main__":
    player_roll()
