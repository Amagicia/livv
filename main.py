from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
import psycopg2
import os
import pytz


# Set up app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Location model
class Location(BaseModel):
    latitude: float
    longitude: float
    accuracy :float

# PostgreSQL connection
try:
    print("📡 Connecting to PostgreSQL DB...")
    db = psycopg2.connect(
        host="dpg-d1fbfsfgi27c73ckorkg-a",
        user="location_1698_user",
        password="Scmgt1Keu8Y4SgFsoTM0OVG6PKAUg1Hu",
        dbname="location_1698",
        port=5432
    )

    cursor = db.cursor()
    print("🛠️ Creating table if not exists...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS locationst (
            id SERIAL PRIMARY KEY,
            latitude DOUBLE PRECISION NOT NULL,
            longitude DOUBLE PRECISION NOT NULL,
            accuracy  DOUBLE PRECISION NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    print("✅ DB setup complete")
except Exception as e:
    print("❌ DB connection error:", e)
    db = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    print("📥 GET request to /")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/all")
async def get_all():
    print("📥 GET request to /all")
    try:
        cursor.execute("SELECT * FROM locationst")
        results = cursor.fetchall()
        print("📦 Fetched records:", results)
        return results
    except Exception as e:
        print("❌ Error fetching data:", e)
        return {"error": str(e)}

@app.post("/location")
async def receive_location(location: Location):
    print("📥 POST request to /location")
    if db:
        try:
            india_tz = pytz.timezone("Asia/Kolkata")
            timestamp = datetime.now(india_tz).strftime("%Y-%m-%d %H:%M:%S")
            print("📦 Incoming location:", location)
            cursor.execute("INSERT INTO locationst (latitude, longitude,accuracy ) VALUES (%s, %s,%s)", (location.latitude, location.longitude,location.accuracy))
            db.commit()
            print("✅ Location saved to DB")
            return {"message": "Location saved ✅"}
        except Exception as e:
            print("❌ DB error on insert:", e)
            return {"error": str(e)}
    print("❌ DB not connected")
    return {"error": "DB not connected"}
