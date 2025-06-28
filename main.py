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
            timestamp Text NOT NULL
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

@app.get("/locations")
async def get_locations():
    print("📥 GET request to /locations")
    try:
        cursor.execute("SELECT * FROM locations")
        results = cursor.fetchall()
        formatted = [
            {
                "Id": row[0],
                "lat": row[1],
                "lng": row[2],
                "time": row[3].strftime("%d %B %Y, %I:%M %p")  # 👈 formats nicely
            }
            for row in results
        ]
        print("📦 Fetched and formatted coordinates:", formatted)
        return formatted
    except Exception as e:
        print("❌ Error fetching coordinates:", e)
        return {"error": str(e)}


@app.post("/location")
async def receive_location(location: Location):
    print("📥 POST request to /location")
    if db:
        try:
            india_tz = pytz.timezone("Asia/Kolkata")
            timestamp = datetime.now(india_tz).strftime("%Y-%m-%d %H:%M:%S")
            print("📦 Incoming location:", location)
            cursor.execute("INSERT INTO locationst (latitude, longitude,accuracy ,timestamp) VALUES (%s, %s,%s,%s)", (location.latitude, location.longitude,location.accuracy,timestamp))
            db.commit()
            print("✅ Location saved to DB")
            cursor.execute("SELECT * FROM locationst")
            results = cursor.fetchone()
            print("📦 Now The Person Is At:", results)
            return {"message": "Location saved ✅"}
        except Exception as e:
            print("❌ DB error on insert:", e)
            return {"error": str(e)}
    print("❌ DB not connected")
    return {"error": "DB not connected"}
