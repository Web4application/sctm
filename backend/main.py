# backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

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
