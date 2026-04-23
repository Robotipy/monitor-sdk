# BotMonitor SDKs

Official SDKs to connect your bots with [BotMonitor](https://monitor.robotipy.dev) — the RPA fleet observability platform by [Robotipy](https://robotipy.dev).

## Available SDKs

| SDK | Language | Install |
|-----|----------|---------|
| [**RocketBot**](./rocketbot) | Python (RocketBot module) | Copy `BotMonitor/` into `modules/` |
| [**Python**](./python) | Python 3.7+ | `pip install botmonitor` |
| [**Node.js**](./nodejs) | Node.js 18+ | `npm install @robotipy/botmonitor` |

## How it works

```
Your Bot  ──  SDK  ──  POST /api/logs  ──  BotMonitor Server
                            │
                  ┌─────────┼─────────┐
                  │         │         │
                ping    start job   end job
```

Every SDK communicates with the BotMonitor API using two headers:

- **`x-api-key`** — Your personal API key (generated in Settings)
- **`x-bot-id`** — The UUID of the bot you're reporting for

## Core concepts

### Ping

A heartbeat signal. Send it periodically so BotMonitor knows your bot is alive.

```
POST /api/logs
{ "level": "INFO", "message": "alive", "type": "ping" }
```

### Job tracking

Wrap your bot's work in `start` / `end` events to track execution time, detect stuck processes, and log outcomes.

```
POST /api/logs
{ "type": "start", "job_id": "inv-001", "job_name": "Process Invoices" }

POST /api/logs
{ "type": "end", "job_id": "inv-001", "status": "ok" }
```

Status values: `ok`, `error`, `timeout`.

### Logs

Send arbitrary log entries at any level.

```
POST /api/logs
{ "level": "ERROR", "message": "File not found", "payload": { "file": "data.csv" } }
```

Log levels: `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

### Data tables

Push structured data rows to named tables for dashboard visualizations.

```
POST /api/data
{ "table": "Invoices", "row": { "id": 42, "amount": 1500, "status": "paid" } }
```

## Quick start

### Python

```python
from botmonitor import ping, start_job, end_job, log

ping()

job_id = start_job(job_name="Process Invoices")
try:
    # ... your bot logic ...
    end_job(status="ok")
except Exception as e:
    log(str(e), level="ERROR")
    end_job(status="error")
```

### Node.js

```javascript
const { BotMonitor } = require("@robotipy/botmonitor");

const monitor = new BotMonitor({
    url: "https://monitor.robotipy.dev",
    apiKey: "bmu_xxxx",
    botId: "uuid-here",
});

await monitor.ping();

const jobId = await monitor.startJob("Process Invoices");
try {
    // ... your bot logic ...
    await monitor.endJob(jobId, "ok");
} catch (err) {
    await monitor.log(err.message, "ERROR");
    await monitor.endJob(jobId, "error");
}
```

### RocketBot

Use the visual commands in the RocketBot command palette:

1. **Connect to BotMonitor** — provide URL, API Key, Bot ID
2. **Start Job** — set a Job ID and optional name
3. *...your RocketBot commands...*
4. **End Job** — same Job ID, select status (OK / Error / Timeout)

### cURL

```bash
curl -X POST https://monitor.robotipy.dev/api/logs -H "Content-Type: application/json" -H "x-api-key: YOUR_KEY" -H "x-bot-id: YOUR_BOT_ID" -d '{"level":"INFO","message":"alive","type":"ping"}'
```

## API reference

### `POST /api/logs`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `level` | string | No | `INFO` (default), `WARNING`, `ERROR`, `CRITICAL` |
| `message` | string | No | Human-readable description |
| `type` | string | No | `ping` (default), `start`, `end` |
| `job_id` | string | If start/end | Unique job identifier |
| `job_name` | string | No | Display name for the job |
| `status` | string | No | Job result: `ok` (default), `error`, `timeout` |
| `payload` | object | No | Arbitrary JSON data attached to the log |
| `meta` | object | No | Metadata attached to the job (start or end) |
| `durationMs` | number | No | Custom duration in milliseconds |

### `POST /api/data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `table` | string | Yes | Target table name |
| `row` | object | Yes | Key-value pairs for the row |
| `columns` | array | First time | Column definitions `[{ name, type, label }]` |

## Bot states

BotMonitor automatically evaluates bot health based on incoming telemetry:

| State | Meaning |
|-------|---------|
| **IDLE** | Waiting — last ping is within the expected window |
| **PROCESSING** | At least one open job running within SLA |
| **STALE** | Silence exceeded the expected frequency |
| **STUCK** | An open job has exceeded the configured SLA |
| **DOWN** | No signals for an extended period |
| **UNKNOWN** | Bot has never sent a ping |

## License

MIT
