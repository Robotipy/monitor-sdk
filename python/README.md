# BotMonitor — Python SDK

## Install

```bash
pip install botmonitor
```

## Quick Start

```python
from botmonitor import ping, start_job, end_job, log

# Simple ping
ping()

# Track a job
job_id = start_job(job_name="Process Invoices")
try:
    # ... your logic ...
    end_job(status="ok")
except Exception as e:
    log(str(e), level="ERROR")
    end_job(status="error")
```

## Configuration

Set via environment variables or call `configure()`:

| Variable | Description |
|---|---|
| `BOTMONITOR_URL` | BotMonitor server URL |
| `BOTMONITOR_API_KEY` | Your personal API key |
| `BOTMONITOR_BOT_ID` | The bot ID from BotMonitor |

```python
from botmonitor import configure

configure(
    url="https://botmonitor.example.com",
    api_key="bm_xxxx",
    bot_id="uuid-here",
)
```

## Functions

| Function | Description |
|---|---|
| `ping(message, level)` | Send a heartbeat ping |
| `start_job(job_name, job_id)` | Signal job start, returns job_id |
| `end_job(job_id, status)` | Signal job end (ok/error) |
| `log(message, level, meta)` | Send a custom log entry |
| `configure(url, api_key, bot_id)` | Override configuration at runtime |
