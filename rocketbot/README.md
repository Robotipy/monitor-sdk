# BotMonitor — RocketBot Module

Module for [RocketBot](https://rocketbot.co/) that integrates with BotMonitor.

## Install

1. Copy the `BotMonitor` folder into your RocketBot `modules/` directory.
2. The module will appear in the RocketBot command palette.

## Commands

| Command | Description |
|---|---|
| Connect to BotMonitor | Initialize connection with API URL, API Key, and Bot ID |
| Send log | Send a log entry (INFO, WARNING, ERROR, CRITICAL) |
| Send data | Send a data row to a BotMonitor table |
| Upload SQLite database | Upload all tables from a SQLite file in batches |

## Dependencies

- `requests>=2.26.0` (install in the `libs/` folder)
