from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from bs4 import BeautifulSoup
import requests
import os

# === Supabase Config ===
SUPABASE_URL = "https://fvcapchuqxfelruvodyg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ2Y2FwY2h1cXhmZWxydXZvZHlnIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0OTUzNjMyNCwiZXhwIjoyMDY1MTEyMzI0fQ.FG_xQYfvj88Wn-kd9hX7sYUkiDFZVl7Dd_PWblP5ECU"  # use service key for backend

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

def get_soup():
    random_url = supabase.table("Daily Player").select("*").execute().data[0]["Daily_URL"]
    res = requests.get(random_url, headers=headers)
    return BeautifulSoup(res.text, "html.parser")

def get_name(soup):
    name_header = soup.find("h1", class_="data-header__headline-wrapper")
    shirt_number = name_header.find("span", class_="data-header__shirt-number").get_text(strip=True)
    full_text = name_header.get_text(strip=True)
    last_name = name_header.find("strong").get_text(strip=True)
    first_name = full_text.replace(shirt_number, "").replace(last_name, "").strip()
    return first_name + " " + last_name

def get_shirt_number(soup):
    return soup.find("h1", class_="data-header__headline-wrapper").find("span", class_="data-header__shirt-number").get_text(strip=True)

def get_profile_img_url(soup):
    profile_img_tag = soup.find("img", class_="data-header__profile-image")
    return profile_img_tag["src"] if profile_img_tag else None

def get_dob(soup):
    info_box = soup.find("div", class_="data-header__info-box")
    return info_box.find("span", attrs={"itemprop": "birthDate"}).get_text(strip=True)

def get_nationality_name(soup):
    info_box = soup.find("div", class_="data-header__info-box")
    return info_box.find("img", class_="flaggenrahmen")["alt"]

def get_nationality_flag(soup):
    info_box = soup.find("div", class_="data-header__info-box")
    return info_box.find("img", class_="flaggenrahmen")["src"]

def get_height(soup):
    info_box = soup.find("div", class_="data-header__info-box")
    return info_box.find("span", attrs={"itemprop": "height"}).get_text(strip=True)

def get_caps(soup):
    tags = soup.find_all("a", class_="data-header__content data-header__content--highlight")
    return tags[0].get_text(strip=True) if len(tags) > 0 else "N/A"

def get_goals(soup):
    tags = soup.find_all("a", class_="data-header__content data-header__content--highlight")
    return tags[1].get_text(strip=True) if len(tags) > 1 else "N/A"

def get_market_value(soup):
    tag = soup.find("a", class_="data-header__market-value-wrapper")
    return tag.get_text(strip=False).split()[0] if tag else "N/A"

def get_value_last_updated(soup):
    tag = soup.find("a", class_="data-header__market-value-wrapper")
    return " ".join(tag.get_text(strip=False).split()[1:]) if tag else "N/A"

def get_club_name(soup):
    club_header = soup.find("div", class_="data-header__box--big")
    return club_header.find("img")["alt"]

def get_club_logo(soup):
    club_header = soup.find("div", class_="data-header__box--big")
    return club_header.find("img")["srcset"].strip().split(" ")[0]

def get_league_name(soup):
    league_header = soup.find("div", class_="data-header__box--big").find("span", class_="data-header__league")
    return league_header.find("img")["alt"]

def get_league_logo(soup):
    league_header = soup.find("div", class_="data-header__box--big").find("span", class_="data-header__league")
    return league_header.find("img")["src"]

def get_player_info(soup):
    return {
        "name": get_name(soup),
        "shirt_number": get_shirt_number(soup),
        "profile_img_url": get_profile_img_url(soup),
        "DOB": get_dob(soup),
        "nationality_name": get_nationality_name(soup),
        "nationality_flag": get_nationality_flag(soup),
        "height": get_height(soup),
        "caps": get_caps(soup),
        "goals": get_goals(soup),
        "market_value": get_market_value(soup),
        "value_last_updated": get_value_last_updated(soup),
        "club_name": get_club_name(soup),
        "club_logo": get_club_logo(soup),
        "league_name": get_league_name(soup),
        "league_logo": get_league_logo(soup),
    }

# === API endpoints: ONE per hint ===

@app.get("/hint/name")
def hint_name():
    soup = get_soup()
    return {"hint": get_name(soup)}

@app.get("/hint/shirt-number")
def hint_shirt_number():
    soup = get_soup()
    return {"hint": get_shirt_number(soup)}

@app.get("/hint/profile-image")
def hint_image():
    soup = get_soup()
    return {"hint": get_profile_img_url(soup)}

@app.get("/hint/birthdate")
def hint_birthdate():
    soup = get_soup()
    return {"hint": get_dob(soup)}

@app.get("/hint/nationality")
def hint_nationality():
    soup = get_soup()
    return {"hint": get_nationality_name(soup)}

@app.get("/hint/market-value")
def hint_market_value():
    soup = get_soup()
    return {"hint": get_market_value(soup)}

@app.get("/hint/club")
def hint_club():
    soup = get_soup()
    return {"hint": get_club_name(soup)}

@app.get("/hint/league")
def hint_league():
    soup = get_soup()
    return {"hint": get_league_name(soup)}
