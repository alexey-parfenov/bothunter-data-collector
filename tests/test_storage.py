from datetime import datetime, timezone

import pandas as pd

from src.models import MarketEvent
from src.storage import EventStorage


def make_event() -> MarketEvent:
    timestamp = datetime.now(timezone.utc)

    return MarketEvent(
        exchange="exchange_a",
        symbol="BTCUSDT",
        event_type="trade",
        price=60_000.0,
        quantity=0.1,
        event_timestamp=timestamp,
        received_timestamp=timestamp,
    )


def test_storage_buffers_event(tmp_path):
    storage = EventStorage(output_dir=tmp_path)

    storage.add(make_event())

    assert len(storage) == 1

    dataframe = storage.to_dataframe()

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["exchange"] == "exchange_a"
    assert dataframe.iloc[0]["symbol"] == "BTCUSDT"


def test_storage_saves_csv(tmp_path):
    storage = EventStorage(output_dir=tmp_path)
    storage.add(make_event())

    path = storage.save_csv()

    assert path.exists()

    dataframe = pd.read_csv(path)

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["exchange"] == "exchange_a"


def test_storage_saves_parquet(tmp_path):
    storage = EventStorage(output_dir=tmp_path)
    storage.add(make_event())

    path = storage.save_parquet()

    assert path.exists()

    dataframe = pd.read_parquet(path)

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["symbol"] == "BTCUSDT"
