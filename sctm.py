import json
import psycopg2
from psycopg2.extras import Json

# ----------------------------
# Sample SCTM data (replace with your actual session data)
# ----------------------------
sctm_data = {
    "student": "Alice",
    "emotion": {"curious": 0.8},
    "lesson": "Physics",
    "tip": "Visualize planets pulling each other",
    "confidence": 0.92,
    "additional": {
        "biological": {"cell": "stem", "CRISPR": "P01"},
        "health": {"patient": "John"}
    }
}

# ----------------------------
# 1️⃣ Save to a local JSON file
# ----------------------------
with open("sctm_session.json", "w") as f:
    json.dump(sctm_data, f, indent=4)

print("✅ SCTM data saved locally to sctm_session.json")

# ----------------------------
# 2️⃣ Save to PostgreSQL
# ----------------------------
# Make sure PostgreSQL is installed and a database exists
DB_HOST = "localhost"
DB_NAME = "sctm_db"
DB_USER = "your_user"
DB_PASS = "your_password"

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sctm_sessions (
            id SERIAL PRIMARY KEY,
            data JSONB
        )
    """)
    
    # Insert SCTM session
    cursor.execute("INSERT INTO sctm_sessions (data) VALUES (%s)", (Json(sctm_data),))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("✅ SCTM data saved to PostgreSQL database")
    
except Exception as e:
    print("❌ Error saving to database:", e)
