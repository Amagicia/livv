from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import mysql.connector
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from datetime import datetime
import pytz

# Get current time in India
india = pytz.timezone("Asia/Kolkata")
timestamp = datetime.now(india)


app = FastAPI()

# CORS for frontend fetch requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount HTML + Static
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # 👈 Replace
    password="root@123",  # 👈 Replace
    database="locationdb"
)
cursor = db.cursor()

# Pydantic schema
class Location(BaseModel):
    latitude: float
    longitude: float
    accuracy: float

@app.get("/", response_class=HTMLResponse)
def serve_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/location")
def store_location(loc: Location):
    india = pytz.timezone("Asia/Kolkata")
    timestamp = datetime.now(india)

    print("📍 Location:", loc.latitude, loc.longitude, "🕒", timestamp,"accuracy",loc.accuracy)

    cursor.execute(
        "INSERT INTO locations (latitude, longitude, timestamp) VALUES (%s, %s, %s)",
        (loc.latitude, loc.longitude, timestamp)
    )
    db.commit()

    return {
        "status": "saved",
        "time": timestamp.strftime("%Y-%m-%d %H:%M:%S")
    }


@app.get("/admin/locations")
def get_all_locations():
    cursor.execute("SELECT * FROM locations")
    rows = cursor.fetchall()
    return [{"id": r[0], "lat": r[1], "lon": r[2], "time": r[3].isoformat()} for r in rows]
