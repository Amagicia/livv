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
# Shirt model
class Shirt(BaseModel):
    id: int
    name: str
    price: str
    image: str
    link: str

# Sample shirt data (could be DB in future)
# shirts = [
#     {"id": 1, "name": "Men Slim Fit Checkered Shirt", "price": "₹279", "image": "redhoodie.jpg", "link": "/product/1"},
#     {"id": 2, "name": "Men Solid Brown Shirt", "price": "₹380", "image": "img2.jpg", "link": "/product/2"},
#     {"id": 3, "name": "Red Hoodie", "price": "₹435", "image": "img3.jpg", "link": "/product/3"},
# ]

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

from fastapi.responses import HTMLResponse
from fastapi import Request

@app.get("/", response_class=HTMLResponse)
async def fpage(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "og_title": "🔥 Latest Men’s Shirts Online | Fashion Deals",
        "og_description": "Get stylish, budget-friendly shirts starting at ₹279. Limited stock!",
        "og_image": "https://livv-2.onrender.com/static/redhoodie.jpg",
        "og_url": "https://livv-2.onrender.com/"
    })


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    print("📥 GET request to /")
    shir = [
        {"name": "Men Slim Fit Checkered Spread Collar Casual Shirt", "price": "₹279", "image": "redhoodie.jpg", "link": "https://dl.flipkart.com/dl/tanip-men-checkered-casual-green-shirt/p/itm9ffb5171a3552?pid=SHTGE85EWWDUN2S4&marketplace=FLIPKART&cmpid=product.share.pp&_refId=PP.1d47ca18-b09e-4892-a6fc-5f1507bf6809.SHTGE85EWWDUN2S4&_appId=WA"},
        {"name": "Peter England Men's Slim Fit T-Shirt", "price": "₹719", "image": "img12.jpg", "link": "https://www.amazon.in/Peter-England-Striped-Regular-PEKWWRGFR06538_Beige/dp/B0DX78DZ31/ref=sr_1_17?rps=1&s=apparel&sr=1-17&psc=1"},
        {"name": "Men Regular Fit Solid Spread Collar Casual Shirt", "price": "₹380", "image": "img2.jpg", "link": "https://dl.flipkart.com/dl/qlonz-store-men-solid-casual-brown-shirt/p/itm676874aeabdbf?pid=SHTHYZYHCGP8PAPN&marketplace=FLIPKART&cmpid=product.share.pp&_refId=PP.75bdb34d-fc27-4863-bde9-b4838b726009.SHTHYZYHCGP8PAPN&_appId=WA"},
        {"name": "Men Regular Fit Checkered Cut Away Collar Casual Shirt", "price": "₹435", "image": "img3.jpg", "link": "https://dl.flipkart.com/dl/allwin-paul-men-checkered-casual-brown-shirt/p/itma5a3ebca3aec8?pid=SHTGFU69ZTVHFFNC&marketplace=FLIPKART&cmpid=product.share.pp&_refId=PP.f1bf3a7e-a6a7-4bfc-a0d2-23cf76d3d069.SHTGFU69ZTVHFFNC&_appId=WA"},
        {"name": "Men Regular Fit Solid, Checkered Spread Collar Casual Shirt", "price": "₹399", "image": "img4.jpg", "link": "https://dl.flipkart.com/s/pyrdKouuuN"},
        {"name": "Men Slim Mid Rise Black Jeans", "price": "₹499", "image": "img6.jpg", "link": "https://dl.flipkart.com/dl/brexx-slim-men-black-jeans/p/itm0bce96d328c7e?pid=JEAHYCVUYMC9QQRT&marketplace=FLIPKART&cmpid=product.share.pp&_refId=PP.bda918e4-c13f-4ddc-977a-88a0ef6e7f4f.JEAHYCVUYMC9QQRT&_appId=WA"},
        {"name": "Men Regular Fit Striped Spread Collar Casual Shirt", "price": "₹930", "image": "img7.jpg", "link": "https://dl.flipkart.com/dl/house-mahnots-men-striped-casual-blue-shirt/p/itm7f012b430aa69?pid=SHTH8ZFFEMFZGXTV&marketplace=FLIPKART&cmpid=product.share.pp&_refId=PP.d3eb9bac-55c2-443d-ab75-f25c24abd3da.SHTH8ZFFEMFZGXTV&_appId=WA"},
        {"name": "Men Regular Mid Rise Blue Jeans", "price": "₹1039", "image": "img5.jpg", "link": "https://dl.flipkart.com/dl/flying-machine-regular-men-blue-jeans/p/itm5fa92a3147a92?pid=JEAH3XVYEG9TGPYK&marketplace=FLIPKART&cmpid=product.share.pp&_refId=PP.4a293916-7fd5-40a1-8d65-4e8afa3f893a.JEAH3XVYEG9TGPYK&_appId=WA"},
        {"name": "Men Regular Fit Solid Spread Collar Casual Shirt  (Pack of 3)", "price": "₹500", "image": "img10.jpg", "link": "https://www.flipkart.com/youth-first-men-solid-casual-black-white-light-green-shirt/p/itm04da8a637950d?pid=SHTHCZ4ZGRNGHEBY&lid=LSTSHTHCZ4ZGRNGHEBY7ZWRYZ&marketplace=FLIPKART&sattr[]=color&st=color"},
        {"name": "Men Regular Fit Checkered Spread Collar Casual Shirt", "price": "₹369", "image": "img11.jpg", "link": "https://dl.flipkart.com/dl/vellosta-men-checkered-casual-white-shirt/p/itm17501c959696a?pid=SHTH8SC79DM6BXYQ&marketplace=FLIPKART&cmpid=product.share.pp&_refId=PP.e41915fa-267d-459e-9d03-4d3a00aa5d93.SHTH8SC79DM6BXYQ&_appId=WA"},
      ]
    return templates.TemplateResponse("main.html", {
        "request": request,
        "shirts": shir
    })



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

@app.get("/delete-all", response_class=HTMLResponse)  # 👈 changed from delete to get
async def delete_all():
    try:
        cursor.execute("DELETE FROM locationst")
        db.commit()
        return "<p>🧹 All location records deleted successfully.</p>"
    except Exception as e:
        return f"<p>Error: {e}</p>"

@app.get("/show", response_class=HTMLResponse)
async def show_data_table(request: Request):
    try:
        cursor.execute("SELECT * FROM locationst ORDER BY id DESC")
        rows = cursor.fetchall()
        india_tz = pytz.timezone("Asia/Kolkata")
        data = [
            {
                "id": row[0],
                "latitude": row[1],
                "longitude": row[2],
                "accuracy": row[3],
                "time": row[4].astimezone(india_tz).strftime("%d %B %Y, %I:%M %p")
            } for row in rows
        ]
        return templates.TemplateResponse("show.html", {"request": request, "data": data})
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error: {e}</h3>", status_code=500)
@app.get("/map", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        cursor.execute("SELECT * FROM locationst ORDER BY id DESC")
        rows = cursor.fetchall()
        india_tz = pytz.timezone("Asia/Kolkata")
        data = [
            {
                "id": row[0],
                "latitude": row[1],
                "longitude": row[2],
                "accuracy": row[3],
                "time": row[4].astimezone(india_tz).strftime("%d %B %Y, %I:%M %p")
            } for row in rows
        ]
    # Pass the coordinates to the Jinja2 template
        return templates.TemplateResponse("map.html", {"request": request, "coordinates": data})
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error: {e}</h3>", status_code=500)

@app.get("/one", response_class=HTMLResponse)
async def unique_coordinates(request: Request):
    query = """
        SELECT DISTINCT 
            ROUND(latitude::numeric, 4) AS latitude, 
            ROUND(longitude::numeric, 4) AS longitude 
        FROM locationst;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    # Convert to list of dicts
    data = [{"latitude": float(row[0]), "longitude": float(row[1])} for row in rows]

    return templates.TemplateResponse("uniq.html", {"request": request, "data": data})