from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(slots=True)
class MarketEvent:
    """Normalized market event used by the portfolio collector."""

    exchange: str
    symbol: str
    event_type: str
    price: float
    quantity: float
    event_timestamp: datetime
    received_timestamp: datetime

    @property
    def latency_ms(self) -> float:
        """Return event delivery latency in milliseconds."""
        delta = self.received_timestamp - self.event_timestamp
        return max(delta.total_seconds() * 1000.0, 0.0)

    def validate(self) -> None:
        """Validate the normalized event."""
        if not self.exchange:
            raise ValueError("Exchange must not be empty")

        if not self.symbol:
            raise ValueError("Symbol must not be empty")

        if not self.event_type:
            raise ValueError("Event type must not be empty")

        if self.price <= 0:
            raise ValueError("Price must be positive")

        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

        if self.event_timestamp.tzinfo is None:
            raise ValueError("Event timestamp must be timezone-aware")

        if self.received_timestamp.tzinfo is None:
            raise ValueError("Received timestamp must be timezone-aware")

        now = datetime.now(timezone.utc)

        if self.event_timestamp > now:
            raise ValueError("Event timestamp must not be in the future")
