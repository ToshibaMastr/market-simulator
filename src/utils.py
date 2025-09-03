import numpy as np
import pandas as pd


def to_ohlcv(prices, volumes, interval=60):
    cut_len = (len(prices) // interval) * interval

    prices = prices[:cut_len]
    volumes = volumes[:cut_len]

    price_reshaped = prices.reshape(-1, interval)
    volume_reshaped = volumes.reshape(-1, interval)

    ohlcv = np.column_stack(
        (
            price_reshaped[:, 0],
            price_reshaped.max(axis=1),
            price_reshaped.min(axis=1),
            price_reshaped[:, -1],
            volume_reshaped.sum(axis=1),
        )
    )

    return ohlcv


def to_dataframe(prices, volumes, interval=60):
    ohlcv = to_ohlcv(prices, volumes, interval)
    columns = pd.Index(["open", "high", "low", "close", "volume"])
    return pd.DataFrame(ohlcv, columns=columns)
