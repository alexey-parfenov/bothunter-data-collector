"""
Storage utilities for normalized market events.

This module demonstrates structured persistence of collected
market data in CSV and Parquet formats.
"""

from pathlib import Path

import pandas as pd

from models import MarketEvent


class EventStorage:
    """Buffer normalized events and persist them to disk."""

    def __init__(
        self,
        output_dir: str = "data",
    ) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._events: list[dict] = []

    def add(self, event: MarketEvent) -> None:
        """Add a normalized market event to the in-memory buffer."""
        self._events.append(
            {
                "exchange": event.exchange,
                "symbol": event.symbol,
                "event_type": event.event_type,
                "price": event.price,
                "quantity": event.quantity,
                "event_timestamp": event.event_timestamp,
                "received_timestamp": event.received_timestamp,
                "latency_ms": round(event.latency_ms, 2),
            }
        )

    def to_dataframe(self) -> pd.DataFrame:
        """Return buffered events as a pandas DataFrame."""
        return pd.DataFrame(self._events)

    def save_csv(
        self,
        filename: str = "events.csv",
    ) -> Path:
        """Persist buffered events as CSV."""
        path = self.output_dir / filename

        self.to_dataframe().to_csv(
            path,
            index=False,
        )

        return path

    def save_parquet(
        self,
        filename: str = "events.parquet",
    ) -> Path:
        """Persist buffered events as Parquet."""
        path = self.output_dir / filename

        self.to_dataframe().to_parquet(
            path,
            index=False,
        )

        return path

    def __len__(self) -> int:
        return len(self._events)
