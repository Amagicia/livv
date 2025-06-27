import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_ROOT_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=int(os.getenv("MYSQL_PORT")),
    )
    print("✅ MySQL connection successful!")
    conn.close()
except mysql.connector.Error as err:
    print(f"❌ MySQL connection failed: {err}")
# ${{ MySQL.MYSQL_URL }}