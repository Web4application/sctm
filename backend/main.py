from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json

app = FastAPI(title="SCTM Live API")

# Load existing SCTM universe
JSON_FILE = "sctm_universe.json"
try:
    with open(JSON_FILE, "r") as f:
        sctm_entities = json.load(f)
except FileNotFoundError:
    sctm_entities = []

# ----------------------------
# Pydantic Models
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
# Helper functions
# ----------------------------
def save_json():
    with open(JSON_FILE, "w") as f:
        json.dump(sctm_entities, f, indent=4)

# ----------------------------
# API Endpoints
# ----------------------------
@app.get("/entities")
def get_entities(entity_type: Optional[str] = None):
    if entity_type:
        return [e for e in sctm_entities if e["type"] == entity_type]
    return sctm_entities

@app.post("/entities")
def create_entity(entity: SCTMEntityModel):
    # Check if entity exists
    for i, e in enumerate(sctm_entities):
        if e["name"] == entity.name and e["type"] == entity.type:
            sctm_entities[i] = entity.dict()
            save_json()
            return {"message": "Entity updated"}
    # New entity
    new_entity = entity.dict()
    new_entity["timestamp"] = datetime.now().isoformat()
    sctm_entities.append(new_entity)
    save_json()
    return {"message": "Entity created"}

@app.get("/entities/query")
def query_entities(entity_type: Optional[str] = None, attribute_key: Optional[str] = None, emotion: Optional[str] = None):
    results = sctm_entities
    if entity_type:
        results = [e for e in results if e["type"] == entity_type]
    if attribute_key:
        results = [e for e in results if attribute_key in e["attributes"]]
    if emotion:
        results = [e for e in results if emotion in e["emotions"]]
    return resultsp

# Allow frontend localhost access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/parse")
async def parse_sctm(request: Request):
    data = await request.json()
    sctm_text = data.get("input", "")

    # Simple parser example
    response = {
        "entities": [],
        "emotion": {},
        "formulas": []
    }

    lines = sctm_text.splitlines()
    for line in lines:
        if line.startswith("@user:"):
            response["entities"].append({"id": line[6:], "type": "user"})
        if line.startswith("@emotion:"):
            em, intensity = line[9:].split("~")
            response["emotion"] = {"type": em, "intensity": float(intensity)}
        if line.startswith("⧉F"):
            # Extract formula id and expression
            parts = line.split("=")
            fid = parts[0].strip()[1:]
            expr = parts[1].strip()
            response["formulas"].append({"id": fid, "expr": expr, "range":[0,10]})

    return response
