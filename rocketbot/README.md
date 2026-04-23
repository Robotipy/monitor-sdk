# BotMonitor — RocketBot Module

Module for [RocketBot](https://rocketbot.co/) that integrates with [BotMonitor](https://monitor.robotipy.dev).

Monitor your RPA bots in real time: send logs, track job executions, push data to dashboards, and upload SQLite databases.

## Install

1. Copy the `BotMonitor` folder into your RocketBot `modules/` directory.
2. Install dependencies: open a terminal in `BotMonitor/libs/` and run `pip install requests -t .`
3. The module will appear in the RocketBot command palette.

## Commands

| Command | Description |
|---------|-------------|
| **Connect to BotMonitor** | Initialize connection with API URL, API Key, and Bot ID |
| **Send log** | Send a log entry (INFO, WARNING, ERROR, CRITICAL) with optional payload |
| **Start Job** | Signal the start of a job execution for duration tracking |
| **End Job** | Signal the end of a job with its final status (OK, Error, Timeout) |
| **Send data** | Send a data row to a BotMonitor table |
| **Upload SQLite database** | Upload all tables from a SQLite file in batches |

## Usage

### Basic flow

```
Connect to BotMonitor
    ↓
Start Job (job_id: "invoice-run", job_name: "Process Invoices")
    ↓
  ... your RocketBot commands ...
    ↓
Send log (level: INFO, message: "Processed 42 invoices")
    ↓
End Job (job_id: "invoice-run", status: OK)
```

### Job tracking

Use **Start Job** before your process begins and **End Job** when it finishes. BotMonitor will:

- Calculate execution duration automatically
- Detect stuck processes if a job exceeds the SLA
- Show job history with status in the bot dashboard

Both commands accept an optional **Metadata** field (JSON) for attaching contextual data like record counts or source identifiers.

### Log levels

| Level | When to use |
|-------|-------------|
| `INFO` | Normal operation, heartbeats |
| `WARNING` | Recoverable issues |
| `ERROR` | Failed operations |
| `CRITICAL` | Requires immediate attention |

## Dependencies

- `requests>=2.26.0` (install in the `libs/` folder)
