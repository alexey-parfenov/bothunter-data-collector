"""
Simplified asynchronous market-data collector.

This module is a portfolio example inspired by the architecture
of the BotHunter Data Collector project.
"""

import asyncio
import logging
import random
from datetime import datetime, timedelta, timezone

from src.health import HealthMonitor
from src.models import MarketEvent
from src.storage import EventStorage


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


class DataCollector:
    """Simplified asynchronous collector for demonstration purposes."""

    def __init__(self, exchanges: list[str]) -> None:
        self.exchanges = exchanges
        self.running = False
        self.health = HealthMonitor(
            stale_after_ms=5_000.0,
            max_event_latency_ms=3_000.0,
        )
        self.storage = EventStorage()

    async def connect(self, exchange: str) -> None:
        """Simulate connection to an external market-data source."""
        logger.info("Connecting to %s...", exchange)

        await asyncio.sleep(0.5)

        logger.info("Connected to %s", exchange)

    async def receive_event(self, exchange: str) -> MarketEvent:
        """
        Generate a sample normalized market event.

        Production API connections are intentionally excluded
        from this public portfolio repository.
        """
        await asyncio.sleep(random.uniform(0.1, 0.5))

        received_timestamp = datetime.now(timezone.utc)

        simulated_latency_ms = random.uniform(20.0, 250.0)

        event_timestamp = received_timestamp - timedelta(
            milliseconds=simulated_latency_ms
        )

        return MarketEvent(
            exchange=exchange,
            symbol="BTCUSDT",
            event_type="trade",
            price=round(random.uniform(50_000, 70_000), 2),
            quantity=round(random.uniform(0.001, 1.0), 6),
            event_timestamp=event_timestamp,
            received_timestamp=received_timestamp,
        )

    async def process_event(self, event: MarketEvent) -> None:
        """Validate an event and update health statistics."""
        self.health.observe(event)
        self.storage.add(event)

        logger.info(
            "%s | %s | %s | price=%s | quantity=%s | latency=%.2f ms",
            event.exchange,
            event.symbol,
            event.event_type,
            event.price,
            event.quantity,
            event.latency_ms,
        )

    async def collect(self, exchange: str) -> None:
        """Run one simplified collection loop."""
        await self.connect(exchange)

        while self.running:
            try:
                event = await self.receive_event(exchange)
                await self.process_event(event)

            except asyncio.CancelledError:
                raise

            except Exception:
                logger.exception(
                    "Collector error for %s",
                    exchange,
                )

                await asyncio.sleep(1)

    async def run(self, duration: float = 5.0) -> None:
        """Run collectors concurrently for a limited demonstration period."""
        self.running = True

        tasks = [
            asyncio.create_task(
                self.collect(exchange)
            )
            for exchange in self.exchanges
        ]

        try:
            await asyncio.sleep(duration)

        finally:
            self.running = False

            for task in tasks:
                task.cancel()

            await asyncio.gather(
                *tasks,
                return_exceptions=True,
            )

        csv_path = self.storage.save_csv()
        parquet_path = self.storage.save_parquet()

        logger.info(
            "Saved %d events to %s and %s",
            len(self.storage),
            csv_path,
            parquet_path,
        )

        logger.info(
            "Collector stopped. Health snapshot: %s",
            self.health.snapshot(),
        )


async def main() -> None:
    collector = DataCollector(
        exchanges=[
            "exchange_a",
            "exchange_b",
            "exchange_c",
        ]
    )

    await collector.run(duration=5)


if __name__ == "__main__":
    asyncio.run(main())
