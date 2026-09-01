"""
Simplified asynchronous market-data collector.

This module is a portfolio example inspired by the architecture
of the BotHunter Data Collector project.
"""

import asyncio
import logging
import random
from dataclasses import dataclass
from datetime import datetime, timezone


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


@dataclass
class MarketEvent:
    exchange: str
    symbol: str
    price: float
    quantity: float
    timestamp: datetime


class DataCollector:
    """Simple asynchronous collector for demonstration purposes."""

    def __init__(self, exchanges: list[str]) -> None:
        self.exchanges = exchanges
        self.running = False
        self.events_processed = 0

    async def connect(self, exchange: str) -> None:
        """Simulate connection to an external market-data source."""

        logger.info("Connecting to %s...", exchange)
        await asyncio.sleep(0.5)
        logger.info("Connected to %s", exchange)

    async def receive_event(self, exchange: str) -> MarketEvent:
        """Generate a sample event instead of using production APIs."""

        await asyncio.sleep(random.uniform(0.1, 0.5))

        return MarketEvent(
            exchange=exchange,
            symbol="BTCUSDT",
            price=round(random.uniform(50_000, 70_000), 2),
            quantity=round(random.uniform(0.001, 1.0), 6),
            timestamp=datetime.now(timezone.utc),
        )

    async def process_event(self, event: MarketEvent) -> None:
        """Validate and process a market event."""

        if event.price <= 0:
            raise ValueError("Price must be positive")

        if event.quantity <= 0:
            raise ValueError("Quantity must be positive")

        self.events_processed += 1

        logger.info(
            "%s | %s | price=%s | quantity=%s",
            event.exchange,
            event.symbol,
            event.price,
            event.quantity,
        )

    async def collect(self, exchange: str) -> None:
        """Run a simplified collection loop."""

        await self.connect(exchange)

        while self.running:
            try:
                event = await self.receive_event(exchange)
                await self.process_event(event)

            except asyncio.CancelledError:
                raise

            except Exception:
                logger.exception("Collector error for %s", exchange)
                await asyncio.sleep(1)

    async def run(self, duration: float = 5.0) -> None:
        """Run collectors concurrently for a limited demonstration period."""

        self.running = True

        tasks = [
            asyncio.create_task(self.collect(exchange))
            for exchange in self.exchanges
        ]

        try:
            await asyncio.sleep(duration)

        finally:
            self.running = False

            for task in tasks:
                task.cancel()

            await asyncio.gather(*tasks, return_exceptions=True)

        logger.info(
            "Collector stopped. Events processed: %d",
            self.events_processed,
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
