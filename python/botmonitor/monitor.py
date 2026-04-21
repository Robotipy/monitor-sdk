"""
BotMonitor — Python SDK.

Send telemetry (pings, job tracking, logs) to your BotMonitor server.

Usage:
    from botmonitor import ping, start_job, end_job, log

    ping()
    job_id = start_job(job_name="Process Invoices")
    end_job(status="ok")
"""

import requests
import uuid
import time
import os

# ── Configuration ─────────────────────────────────────────────
BOTMONITOR_URL = os.getenv("BOTMONITOR_URL", "{{API_URL}}")
BOTMONITOR_API_KEY = os.getenv("BOTMONITOR_API_KEY", "{{API_KEY}}")
BOTMONITOR_BOT_ID = os.getenv("BOTMONITOR_BOT_ID", "{{BOT_ID}}")

_HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": BOTMONITOR_API_KEY,
    "x-bot-id": BOTMONITOR_BOT_ID,
}

_current_job_id = None
_current_job_start = None


def configure(url=None, api_key=None, bot_id=None):
    """Override configuration at runtime."""
    global BOTMONITOR_URL, BOTMONITOR_API_KEY, BOTMONITOR_BOT_ID, _HEADERS
    if url:
        BOTMONITOR_URL = url
    if api_key:
        BOTMONITOR_API_KEY = api_key
    if bot_id:
        BOTMONITOR_BOT_ID = bot_id
    _HEADERS = {
        "Content-Type": "application/json",
        "x-api-key": BOTMONITOR_API_KEY,
        "x-bot-id": BOTMONITOR_BOT_ID,
    }


def ping(message="alive", level="INFO", meta=None):
    """Send a simple ping to confirm the bot is running."""
    body = {"level": level, "message": message, "type": "ping"}
    if meta:
        body["meta"] = meta
    try:
        requests.post(f"{BOTMONITOR_URL}/api/logs", json=body, headers=_HEADERS, timeout=5)
    except Exception as e:
        print(f"[BotMonitor] ping failed: {e}")


def start_job(job_name=None, job_id=None, meta=None):
    """Signal the start of a job. Returns the job_id for later use."""
    global _current_job_id, _current_job_start
    _current_job_id = job_id or str(uuid.uuid4())
    _current_job_start = time.time()

    body = {
        "level": "INFO",
        "message": f"Job started: {job_name or _current_job_id}",
        "type": "start",
        "job_id": _current_job_id,
    }
    if job_name:
        body["job_name"] = job_name
    if meta:
        body["meta"] = meta

    try:
        requests.post(f"{BOTMONITOR_URL}/api/logs", json=body, headers=_HEADERS, timeout=5)
    except Exception as e:
        print(f"[BotMonitor] start_job failed: {e}")

    return _current_job_id


def end_job(job_id=None, status="ok", meta=None):
    """Signal the end of a job."""
    global _current_job_id, _current_job_start
    jid = job_id or _current_job_id
    if not jid:
        print("[BotMonitor] end_job called without a job_id")
        return

    elapsed = ""
    if _current_job_start:
        elapsed = f" ({time.time() - _current_job_start:.1f}s)"

    body = {
        "level": "ERROR" if status == "error" else "INFO",
        "message": f"Job ended: {jid}{elapsed}",
        "type": "end",
        "job_id": jid,
        "status": status,
    }
    if meta:
        body["meta"] = meta

    try:
        requests.post(f"{BOTMONITOR_URL}/api/logs", json=body, headers=_HEADERS, timeout=5)
    except Exception as e:
        print(f"[BotMonitor] end_job failed: {e}")

    if jid == _current_job_id:
        _current_job_id = None
        _current_job_start = None


def log(message, level="INFO", meta=None):
    """Send a custom log entry."""
    body = {"level": level, "message": message}
    if meta:
        body["meta"] = meta
    try:
        requests.post(f"{BOTMONITOR_URL}/api/logs", json=body, headers=_HEADERS, timeout=5)
    except Exception as e:
        print(f"[BotMonitor] log failed: {e}")
