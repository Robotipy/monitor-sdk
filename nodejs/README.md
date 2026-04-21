# BotMonitor — Node.js SDK

## Install

```bash
npm install @robotipy/botmonitor
```

## Quick Start

```javascript
const { BotMonitor } = require("@robotipy/botmonitor");

const monitor = new BotMonitor({
    url: "https://botmonitor.example.com",
    apiKey: "bm_xxxx",
    botId: "uuid-here",
});

// Simple ping
await monitor.ping();

// Track a job
const jobId = await monitor.startJob("Process Invoices");
try {
    // ... your logic ...
    await monitor.endJob(jobId, "ok");
} catch (err) {
    await monitor.log(err.message, "ERROR");
    await monitor.endJob(jobId, "error");
}
```

## Configuration

Pass config in the constructor or set environment variables:

| Variable | Description |
|---|---|
| `BOTMONITOR_URL` | BotMonitor server URL |
| `BOTMONITOR_API_KEY` | Your personal API key |
| `BOTMONITOR_BOT_ID` | The bot ID from BotMonitor |

## API

| Method | Description |
|---|---|
| `ping(message, level)` | Send a heartbeat ping |
| `startJob(jobName, jobId)` | Signal job start, returns jobId |
| `endJob(jobId, status)` | Signal job end (ok/error) |
| `log(message, level, meta)` | Send a custom log entry |
