from dataclasses import dataclass, field
from statistics import mean

from models import MarketEvent


@dataclass(slots=True)
class HealthStats:
    """Runtime health statistics for one market-data source."""

    exchange: str
    events: int = 0
    invalid_events: int = 0
    stale_events: int = 0
    latency_anomalies: int = 0
    latencies_ms: list[float] = field(default_factory=list)

    @property
    def average_latency_ms(self) -> float:
        if not self.latencies_ms:
            return 0.0

        return mean(self.latencies_ms)

    @property
    def max_latency_ms(self) -> float:
        if not self.latencies_ms:
            return 0.0

        return max(self.latencies_ms)


class HealthMonitor:
    """Monitor event validity, freshness and delivery latency."""

    def __init__(
        self,
        stale_after_ms: float = 5_000.0,
        max_event_latency_ms: float = 3_000.0,
    ) -> None:
        self.stale_after_ms = stale_after_ms
        self.max_event_latency_ms = max_event_latency_ms
        self._stats: dict[str, HealthStats] = {}

    def _get_stats(self, exchange: str) -> HealthStats:
        if exchange not in self._stats:
            self._stats[exchange] = HealthStats(exchange=exchange)

        return self._stats[exchange]

    def observe(self, event: MarketEvent) -> None:
        """Validate an event and update health statistics."""

        stats = self._get_stats(event.exchange)

        try:
            event.validate()
        except ValueError:
            stats.invalid_events += 1
            raise

        latency_ms = event.latency_ms

        stats.events += 1
        stats.latencies_ms.append(latency_ms)

        if latency_ms > self.stale_after_ms:
            stats.stale_events += 1

        if latency_ms > self.max_event_latency_ms:
            stats.latency_anomalies += 1

    def snapshot(self) -> dict[str, dict[str, float | int]]:
        """Return a serializable snapshot of current health statistics."""

        result: dict[str, dict[str, float | int]] = {}

        for exchange, stats in self._stats.items():
            result[exchange] = {
                "events": stats.events,
                "invalid_events": stats.invalid_events,
                "stale_events": stats.stale_events,
                "latency_anomalies": stats.latency_anomalies,
                "average_latency_ms": round(
                    stats.average_latency_ms,
                    2,
                ),
                "max_latency_ms": round(
                    stats.max_latency_ms,
                    2,
                ),
            }

        return result
