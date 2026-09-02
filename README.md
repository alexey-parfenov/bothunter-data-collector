# BotHunter Data Collector

[![Python CI](https://github.com/alexey-parfenov/bothunter-data-collector/actions/workflows/python-app.yml/badge.svg)](https://github.com/alexey-parfenov/bothunter-data-collector/actions/workflows/python-app.yml)

A simplified asynchronous Python application for collecting, normalizing, monitoring and storing streaming market events.

This repository is a public portfolio version inspired by the architecture of my larger **BotHunter** project — a system for collecting and analyzing real-time market data from multiple cryptocurrency exchanges.

Production exchange connections, credentials, infrastructure configuration and proprietary trading logic are intentionally excluded.

## What this project demonstrates

The public project demonstrates practical experience with:

- Python
- `asyncio` and concurrent tasks
- asynchronous event-processing architecture
- structured data models
- event validation and normalization
- latency and stale-data monitoring
- runtime health statistics
- CSV and Parquet persistence
- pandas and PyArrow
- exception and cancellation handling
- automated testing with `pytest`
- asynchronous testing with `pytest-asyncio`
- integration testing
- GitHub Actions CI
- application smoke testing

The larger private BotHunter project also works with real exchange REST APIs, WebSocket streams and Linux/VPS deployment. Those production integrations are not included in this public repository.

## Architecture

The portfolio application follows a simplified streaming-data pipeline:

```text
Simulated data sources
        │
        ▼
 Async collectors
        │
        ▼
 Normalized MarketEvent
        │
        ├──────────────► Validation
        │
        ├──────────────► Health / latency monitoring
        │
        ▼
 Event processing
        │
        ▼
 In-memory buffer
        │
        ├──────────────► CSV
        │
        └──────────────► Parquet
```

Multiple collectors run concurrently using `asyncio`.

The public version generates simulated market events so that the architecture can be demonstrated without exposing production exchange connections or private project logic.

## Repository structure

```text
bothunter-data-collector/
│
├── src/
│   ├── __init__.py
│   ├── collector.py
│   ├── models.py
│   ├── health.py
│   └── storage.py
│
├── tests/
│   ├── test_collector.py
│   ├── test_health.py
│   └── test_storage.py
│
├── examples/
│   └── sample_events.csv
│
├── .github/
│   └── workflows/
│       └── python-app.yml
│
├── config.example.yaml
├── requirements.txt
└── README.md
```

## Main components

### DataCollector

`src/collector.py`

Coordinates the demonstration pipeline.

It:

- starts several asynchronous collectors concurrently;
- simulates connections to independent data sources;
- generates normalized market events;
- processes events through the health monitor;
- sends validated events to storage;
- handles task cancellation and runtime exceptions;
- saves collected data when the demonstration run finishes.

The application can be started as a Python module:

```bash
python -m src.collector
```

### MarketEvent

`src/models.py`

Defines the normalized event model.

Each event contains:

- exchange;
- symbol;
- event type;
- price;
- quantity;
- source event timestamp;
- local receive timestamp.

The model validates incoming data and calculates event delivery latency.

Validation includes checks for:

- required identifiers;
- positive price and quantity;
- timezone-aware timestamps;
- correct timestamp ordering;
- future event timestamps.

### HealthMonitor

`src/health.py`

Maintains runtime health statistics independently for each data source.

It tracks:

- processed events;
- invalid events;
- stale events;
- latency anomalies;
- average event latency;
- maximum event latency.

Latency statistics are calculated incrementally instead of storing the complete latency history, keeping memory usage bounded as the number of processed events grows.

### EventStorage

`src/storage.py`

Buffers normalized events and provides persistence in:

- CSV;
- Parquet.

The storage layer converts events into a structured pandas DataFrame before writing them to disk.

During the demonstration run the collector creates:

```text
data/events.csv
data/events.parquet
```

## Automated tests

The repository contains automated tests covering the main public components.

### Health monitoring tests

`tests/test_health.py`

Tests include:

- valid event counting;
- latency anomaly detection;
- stale-event detection;
- average latency calculation;
- maximum latency calculation.

### Collector integration test

`tests/test_collector.py`

Checks the integration between:

```text
DataCollector
      │
      ├──► HealthMonitor
      │
      └──► EventStorage
```

The test verifies that processing an event updates health statistics and adds the event to storage.

### Storage tests

`tests/test_storage.py`

Tests verify:

- event buffering;
- DataFrame conversion;
- CSV persistence;
- Parquet persistence;
- reading generated files back successfully.

## Continuous Integration

GitHub Actions automatically validates the repository after pushes and pull requests to `main`.

The CI pipeline:

1. checks out the repository;
2. sets up Python;
3. installs dependencies;
4. compiles the Python modules;
5. runs the complete `pytest` test suite;
6. launches the collector as a smoke test;
7. verifies that CSV and Parquet output files were actually created.

This means CI checks not only syntax and unit tests, but also the executable demonstration pipeline.

## Example event

A normalized event stored by the application contains fields such as:

```csv
exchange,symbol,event_type,price,quantity,event_timestamp,received_timestamp,latency_ms
exchange_a,BTCUSDT,trade,60000.0,0.1,2026-01-01T12:00:00+00:00,2026-01-01T12:00:00.100000+00:00,100.0
```

A sample dataset is available in:

```text
examples/sample_events.csv
```

## Example configuration

`config.example.yaml` documents the safe public configuration structure:

```yaml
exchanges:
  - exchange_a
  - exchange_b
  - exchange_c

health:
  stale_after_ms: 5000
  max_event_latency_ms: 3000

storage:
  output_dir: data

logging:
  level: INFO
```

The file contains no credentials or production settings.

## Reliability considerations

The public implementation demonstrates several reliability-oriented practices:

- explicit event validation;
- timezone-aware timestamps;
- detection of stale events;
- latency anomaly monitoring;
- bounded-memory health statistics;
- exception handling in asynchronous collectors;
- graceful task cancellation;
- automated unit and integration tests;
- executable smoke testing in CI;
- verification of generated output files.

The larger BotHunter project extends these principles to real-time exchange connections, connection watchdogs, reconnection logic, data-quality monitoring and production-scale event streams.

## Privacy and scope

This repository is intentionally a **portfolio demonstration**, not the production BotHunter codebase.

It does not contain:

- API keys or credentials;
- private endpoints;
- server addresses;
- production infrastructure configuration;
- exchange-specific production connection code;
- order execution functionality;
- proprietary signal or trading logic.

The purpose of the repository is to demonstrate Python engineering practices used in the larger project while keeping sensitive and proprietary implementation details private.

## Project status

**Portfolio demo — working and automatically tested.**

The current version includes:

- asynchronous event collection;
- normalized event models;
- data validation;
- health and latency monitoring;
- CSV / Parquet persistence;
- automated tests;
- integration tests;
- GitHub Actions CI;
- executable smoke testing.
