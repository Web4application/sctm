# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import psycopg2
from psycopg2.extras import Json

app = FastAPI(title="SCTM Knowledge Universe")

# ----------------------------
# PostgreSQL config
# ----------------------------
DB_CONFIG = {
    "host": "localhost",
    "database": "sctm_db",
    "user": "your_user",
    "password": "your_password"
}

# ----------------------------
# Pydantic Model
# ----------------------------
class SCTMEntityModel(BaseModel):
    name: str
    type: str
    parent: Optional[str] = None
    attributes: Optional[dict] = {}
    emotions: Optional[dict] = {}
    additional: Optional[dict] = {}
    children: Optional[List[dict]] = []

# ----------------------------
# Helper: DB connection
# ----------------------------
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sctm_entities (
            id SERIAL PRIMARY KEY,
            name TEXT,
            type TEXT,
            parent TEXT,
            data JSONB,
            updated_at TIMESTAMP,
            UNIQUE(name, type)
        )
    """)
    conn.commit()
    return conn, cursor

# ----------------------------
# API Endpoints
# ----------------------------
@app.get("/entities")
def get_entities(entity_type: Optional[str] = None):
    conn, cursor = get_db_connection()
    if entity_type:
        cursor.execute("SELECT data FROM sctm_entities WHERE type=%s", (entity_type,))
    else:
        cursor.execute("SELECT data FROM sctm_entities")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in rows]

@app.post("/entities")
def create_entity(entity: SCTMEntityModel):
    conn, cursor = get_db_connection()
    entity_dict = entity.dict()
    entity_dict["timestamp"] = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO sctm_entities (name, type, parent, data, updated_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (name, type) DO UPDATE
        SET data = EXCLUDED.data,
            updated_at = EXCLUDED.updated_at
    """, (entity.name, entity.type, entity.parent, Json(entity_dict), datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Entity created/updated"}

@app.get("/entities/query")
def query_entities(entity_type: Optional[str] = None, attribute_key: Optional[str] = None, emotion: Optional[str] = None):
    conn, cursor = get_db_connection()
    cursor.execute("SELECT data FROM sctm_entities")
    rows = [row[0] for row in cursor.fetchall()]
    results = rows
    if entity_type:
        results = [e for e in results if e["type"] == entity_type]
    if attribute_key:
        results = [e for e in results if attribute_key in e["attributes"]]
    if emotion:
        results = [e for e in results if emotion in e["emotions"]]
    cursor.close()
    conn.close()
    return results
