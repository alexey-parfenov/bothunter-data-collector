# BotHunter Data Collector

Asynchronous Python application for collecting and processing real-time market data from multiple cryptocurrency exchanges.

## About the project

BotHunter Data Collector is a personal Python project developed to practice building reliable asynchronous applications that work with external APIs and high-frequency data streams.

The application collects public market data using REST APIs and WebSocket connections, processes incoming events and monitors the quality and stability of data collection.

The project focuses on data engineering, API integrations, asynchronous programming and application reliability.

## Technologies

- Python
- asyncio
- REST API
- WebSocket
- JSON
- pandas
- CSV / Parquet
- Linux / Ubuntu
- Git

## Key features

- asynchronous collection of real-time market data;
- integration with multiple external APIs;
- WebSocket connection management;
- processing of large event streams;
- connection and error monitoring;
- data latency diagnostics;
- data-quality monitoring;
- structured storage in CSV and Parquet;
- configuration-based application setup;
- deployment and testing on Linux/VPS.

## Project architecture

The application is divided into several logical components:

1. Instrument discovery through REST APIs.
2. WebSocket connection management.
3. Asynchronous event processing.
4. Data validation and normalization.
5. Health and latency monitoring.
6. Persistent data storage.

## Reliability

The collector includes mechanisms for:

- automatic WebSocket reconnection;
- connection watchdogs;
- exception handling;
- event timestamp validation;
- latency monitoring;
- detection of abnormal or stale data;
- collection health statistics.

## Repository purpose

This repository contains a simplified portfolio version of the project.

Production configuration, credentials, infrastructure details and proprietary trading logic are intentionally excluded.

The repository demonstrates the architecture, coding approach and technologies used in the project.
