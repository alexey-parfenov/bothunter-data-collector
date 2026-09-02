import pytest

from src.collector import DataCollector
from src.models import MarketEvent


@pytest.mark.asyncio
async def test_process_event_updates_health_and_storage():
    collector = DataCollector(
        exchanges=["exchange_a"]
    )

    event = MarketEvent(
        exchange="exchange_a",
        symbol="BTCUSDT",
        event_type="trade",
        price=60_000.0,
        quantity=0.1,
        event_timestamp=__import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ),
        received_timestamp=__import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ),
    )

    await collector.process_event(event)

    snapshot = collector.health.snapshot()

    assert len(collector.storage) == 1
    assert snapshot["exchange_a"]["events"] == 1
