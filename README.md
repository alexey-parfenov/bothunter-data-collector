# BotHunter Data Collector

[![Python CI](https://github.com/alexey-parfenov/bothunter-data-collector/actions/workflows/python-app.yml/badge.svg)](https://github.com/alexey-parfenov/bothunter-data-collector/actions/workflows/python-app.yml)

Asynchronous Python application for collecting, normalizing and monitoring real-time market data from multiple external data sources.

This repository is a simplified portfolio version of a larger personal project.

Production credentials, infrastructure configuration and proprietary trading logic are intentionally excluded.

## What the project demonstrates

The project demonstrates practical experience with:

- Python
- asyncio
- REST API architecture
- WebSocket-style event processing
- asynchronous data pipelines
- JSON and structured market data
- data validation and normalization
- event latency monitoring
- application health monitoring
- CSV / Parquet storage
- exception handling
- automated testing with pytest
- GitHub Actions CI
- Linux / VPS deployment concepts

## Architecture

The application is divided into several logical components:

```text
External data sources
        |
        v
  Async collectors
        |
        v
 Event normalization
        |
        +------------> Health / latency monitoring
        |
        v
 Event processing
        |
        v
 Persistent storage
```

## Repository structure

```text
bothunter-data-collector/
|
+-- src/
|   +-- __init__.py
|   +-- collector.py
|   +-- models.py
|   +-- health.py
|   +-- storage.py
|
+-- tests/
|   +-- test_health.py
|
+-- examples/
|   +-- sample_events.csv
|
+-- .github/
|   +-- workflows/
|       +-- python-app.yml
|
+-- config.example.yaml
+-- requirements.txt
+-- README.md
```

## Main components

### Collector

`src/collector.py`

Demonstrates:

- concurrent asynchronous collectors;
- lifecycle management with `asyncio`;
- normalized event processing;
- exception handling;
- integration with health monitoring and storage.

### Data model

`src/models.py`

Contains a normalized market-event model with:

- exchange;
- symbol;
- event type;
- price;
- quantity;
- event timestamp;
- receive timestamp;
- calculated delivery latency.

The model also performs basic data validation.

### Health monitoring

`src/health.py`

Tracks runtime statistics for each data source:

- processed events;
- invalid events;
- stale events;
- latency anomalies;
- average latency;
- maximum latency.

This component demonstrates one of the main focuses of the original project: monitoring the quality and reliability of incoming streaming data.

### Storage

`src/storage.py`

Provides a simplified storage layer for normalized events.

The production project uses structured storage for large event streams. The portfolio repository contains only a safe demonstration implementation.

## Automated tests

The repository contains automated tests for the health-monitoring logic.

Examples of tested behaviour:

- valid events are counted correctly;
- latency anomalies are detected;
- stale events are detected.

Tests are located in:

```text
tests/test_health.py
```

## Continuous Integration

GitHub Actions automatically checks the project after every push and pull request to `main`.

The CI pipeline:

1. checks out the repository;
2. installs Python;
3. installs project dependencies;
4. compiles Python modules;
5. runs automated tests with `pytest`.

A successful workflow run confirms that the portfolio version can be installed and tested in a clean Linux environment.

## Example event

Example normalized data:

```csv
timestamp,exchange,symbol,event_type,price,quantity,latency_ms
2026-01-01T12:00:00.100Z,exchange_a,ASSET1USDT,trade,100.25,0.150,42
2026-01-01T12:00:00.220Z,exchange_b,ASSET1USDT,trade,100.27,0.080,55
```

See `examples/sample_events.csv`.

## Reliability

The larger project includes mechanisms for:

- automatic connection recovery;
- connection watchdogs;
- exception handling;
- event timestamp validation;
- latency diagnostics;
- stale-data detection;
- data-quality monitoring;
- runtime health statistics.

The public repository demonstrates these engineering approaches without exposing production infrastructure or proprietary logic.

## Repository purpose

This repository is intended as a technical portfolio project.

It demonstrates how I structure a Python application dealing with asynchronous event streams, data validation, monitoring, storage and automated testing.

The repository contains no API credentials, private endpoints, production infrastructure details or trading execution logic.
