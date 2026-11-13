import json
import os
import secrets
import sqlite3
import time
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path

import requests
from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parent
DB_PATH = os.getenv("THE_LORD_DB_PATH", str(ROOT / "the_lord.sqlite3"))
app = Flask(__name__, static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

AGENT_CATALOG = [
    {"id": "quantum-ultra", "name": "Quantum KI Ultra Pro", "role": "generalist", "skills": ["reasoning", "chat", "coding", "planning"]},
    {"id": "ionos", "name": "IONOS KI", "role": "knowledge", "skills": ["knowledge", "analysis", "project-memory"]},
    {"id": "galactic", "name": "Galactic AI", "role": "world-builder", "skills": ["worldbuilding", "creative", "image-workflows"]},
    {"id": "quantum-mirror", "name": "Quantum Mirror", "role": "game-dev", "skills": ["game-design", "mods", "quests", "npc"]},
    {"id": "quantenformel", "name": "Quantenformel", "role": "research", "skills": ["research", "prototyping", "knowledge"]},
    {"id": "note-ki", "name": "Note-KI", "role": "documents", "skills": ["documents", "summarization", "project-context"]},
    {"id": "quantumlight", "name": "AI Quantumlight", "role": "assistant", "skills": ["chat", "creative"]},
    {"id": "cat-chat", "name": "Quantum Cat Chat", "role": "companion", "skills": ["chat", "companion"]},
]

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS agent_tasks (
            id TEXT PRIMARY KEY, goal TEXT NOT NULL, status TEXT NOT NULL,
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL, result_json TEXT
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS update_proposals (
            id TEXT PRIMARY KEY, repo TEXT NOT NULL, summary TEXT NOT NULL,
            risk TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL
        )""")

def require_admin_key(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        expected = os.getenv("THE_LORD_ADMIN_API_KEY")
        supplied = request.headers.get("X-The-Lord-Admin-Key", "")
        if not expected or not secrets.compare_digest(expected, supplied):
            return jsonify({"error": "Unauthorized", "hint": "Configure THE_LORD_ADMIN_API_KEY and send it in X-The-Lord-Admin-Key."}), 401
        return fn(*args, **kwargs)
    return wrapped

def provider_config():
    raw = os.getenv("THE_LORD_AI_PROVIDERS", "{}")
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}

def public_agents():
    configured = provider_config()
    result = []
    for item in AGENT_CATALOG:
        cfg = configured.get(item["id"], {})
        result.append({**item, "connected": bool(cfg.get("url")), "status": "configured" if cfg.get("url") else "awaiting_endpoint"})
    return result

def call_provider(agent_id, prompt, context=None):
    cfg = provider_config().get(agent_id)
    if not isinstance(cfg, dict) or not cfg.get("url"):
        return {"agent_id": agent_id, "status": "not_configured", "message": "Für diesen Agenten ist noch kein API-Endpunkt hinterlegt."}
    url = cfg["url"]
    if not url.startswith("https://"):
        return {"agent_id": agent_id, "status": "blocked", "message": "Nur HTTPS-Endpunkte sind erlaubt."}
    headers = {"Content-Type": "application/json"}
    token_env = cfg.get("api_key_env")
    if token_env and os.getenv(token_env):
        headers["Authorization"] = "Bearer " + os.environ[token_env]
    payload = {"message": prompt, "prompt": prompt, "context": context or {}, "agent": agent_id}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=(5, 35))
        response.raise_for_status()
        try:
            body = response.json()
        except ValueError:
            body = {"text": response.text[:12000]}
        return {"agent_id": agent_id, "status": "ok", "response": body}
    except requests.RequestException as exc:
        return {"agent_id": agent_id, "status": "error", "message": str(exc)[:500]}

@app.get("/")
def home():
    return send_from_directory(ROOT, "index.html")

@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "THE LORD AI Agent Network", "time": datetime.now(timezone.utc).isoformat()})

@app.get("/api/v1/agents")
def agents():
    return jsonify({"agents": public_agents(), "note": "A listed agent is only live when its provider endpoint is configured."})

@app.post("/api/v1/agents/run")
def run_agents():
    body = request.get_json(silent=True) or {}
    goal = str(body.get("goal", "")).strip()
    if not goal or len(goal) > 12000:
        return jsonify({"error": "goal is required and must be under 12000 characters"}), 400
    selected = body.get("agents") or ["quantum-ultra"]
    if not isinstance(selected, list) or len(selected) > 8:
        return jsonify({"error": "agents must be a list of at most 8 agent ids"}), 400
    known = {x["id"] for x in AGENT_CATALOG}
    selected = [x for x in selected if x in known]
    task_id = secrets.token_urlsafe(12)
    now = datetime.now(timezone.utc).isoformat()
    with db() as conn:
        conn.execute("INSERT INTO agent_tasks(id,goal,status,created_at,updated_at) VALUES(?,?,?,?,?)",
                     (task_id, goal, "running", now, now))
    outputs = [call_provider(agent_id, goal, body.get("context")) for agent_id in selected]
    success = any(x["status"] == "ok" for x in outputs)
    status = "completed" if success else "waiting_for_provider_configuration"
    with db() as conn:
        conn.execute("UPDATE agent_tasks SET status=?,updated_at=?,result_json=? WHERE id=?",
                     (status, datetime.now(timezone.utc).isoformat(), json.dumps(outputs), task_id))
    return jsonify({"task_id": task_id, "status": status, "results": outputs,
                    "next_step": "Configure provider endpoints for agents marked awaiting_endpoint."}), (200 if success else 503)

@app.get("/api/v1/tasks/<task_id>")
def task_status(task_id):
    with db() as conn:
        row = conn.execute("SELECT * FROM agent_tasks WHERE id=?", (task_id,)).fetchone()
    if not row:
        return jsonify({"error": "task not found"}), 404
    return jsonify({**dict(row), "result": json.loads(row["result_json"]) if row["result_json"] else None})

@app.post("/api/v1/updates/proposals")
@require_admin_key
def create_update_proposal():
    body = request.get_json(silent=True) or {}
    repo = str(body.get("repo", "")).strip()
    summary = str(body.get("summary", "")).strip()
    risk = str(body.get("risk", "medium")).lower()
    if not repo or "/" not in repo or not summary:
        return jsonify({"error": "repo (owner/name) and summary are required"}), 400
    if risk not in {"low", "medium", "high"}:
        return jsonify({"error": "risk must be low, medium or high"}), 400
    proposal_id = secrets.token_urlsafe(10)
    with db() as conn:
        conn.execute("INSERT INTO update_proposals(id,repo,summary,risk,status,created_at) VALUES(?,?,?,?,?,?)",
                     (proposal_id, repo, summary, risk, "awaiting_human_approval", datetime.now(timezone.utc).isoformat()))
    return jsonify({"proposal_id": proposal_id, "status": "awaiting_human_approval",
                    "policy": "No direct production deployment. Changes require review, passing tests and explicit approval."}), 201

@app.get("/api/v1/updates/proposals")
@require_admin_key
def list_update_proposals():
    with db() as conn:
        rows = conn.execute("SELECT * FROM update_proposals ORDER BY created_at DESC LIMIT 100").fetchall()
    return jsonify({"proposals": [dict(row) for row in rows]})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
else:
    init_db()
