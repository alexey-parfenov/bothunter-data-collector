from datetime import datetime, timedelta, timezone

from src.health import HealthMonitor
from src.models import MarketEvent


def make_event(
    *,
    exchange: str = "exchange_a",
    latency_ms: float = 100.0,
) -> MarketEvent:
    received = datetime.now(timezone.utc)
    event_time = received - timedelta(milliseconds=latency_ms)

    return MarketEvent(
        exchange=exchange,
        symbol="BTCUSDT",
        event_type="trade",
        price=60_000.0,
        quantity=0.1,
        event_timestamp=event_time,
        received_timestamp=received,
    )


def test_valid_event_is_counted():
    monitor = HealthMonitor(
        stale_after_ms=5_000.0,
        max_event_latency_ms=3_000.0,
    )

    event = make_event(latency_ms=100.0)
    monitor.observe(event)

    snapshot = monitor.snapshot()

    assert snapshot["exchange_a"]["events"] == 1
    assert snapshot["exchange_a"]["invalid_events"] == 0
    assert snapshot["exchange_a"]["stale_events"] == 0
    assert snapshot["exchange_a"]["latency_anomalies"] == 0


def test_latency_anomaly_is_detected():
    monitor = HealthMonitor(
        stale_after_ms=5_000.0,
        max_event_latency_ms=3_000.0,
    )

    event = make_event(latency_ms=3_500.0)
    monitor.observe(event)

    snapshot = monitor.snapshot()

    assert snapshot["exchange_a"]["events"] == 1
    assert snapshot["exchange_a"]["latency_anomalies"] == 1


def test_stale_event_is_detected():
    monitor = HealthMonitor(
        stale_after_ms=5_000.0,
        max_event_latency_ms=3_000.0,
    )

    event = make_event(latency_ms=6_000.0)
    monitor.observe(event)

    snapshot = monitor.snapshot()

    assert snapshot["exchange_a"]["events"] == 1
    assert snapshot["exchange_a"]["stale_events"] == 1

def test_latency_statistics_are_calculated():
    monitor = HealthMonitor(
        stale_after_ms=5_000.0,
        max_event_latency_ms=3_000.0,
    )

    monitor.observe(make_event(latency_ms=100.0))
    monitor.observe(make_event(latency_ms=300.0))

    snapshot = monitor.snapshot()

    assert snapshot["exchange_a"]["events"] == 2
    assert snapshot["exchange_a"]["average_latency_ms"] == 200.0
    assert snapshot["exchange_a"]["max_latency_ms"] == 300.0
