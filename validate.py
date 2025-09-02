from collections import defaultdict
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from random import random

from orderbook import OrderBook

from datetime import datetime, timedelta


def addbk(price: float, heat: int):
    prb = abs(np.random.normal(0, 10, heat) + price)
    volumes = np.random.exponential(scale=1.0, size=len(prb))
    return np.column_stack([prb, volumes])


price = 100
steps = 3000
interval = 30

prices = np.zeros([steps])
volumes = np.zeros([steps])

nw = datetime.now()

obook = OrderBook()
for i in range(steps):
    heats = int(np.random.lognormal(mean=0, sigma=1, size=None) * 100)
    heatb = abs(heats + np.random.randint(-5, 6))

    for p, v in addbk(price + 3, heats):
        obook.add_ask(p, v)

    for p, v in addbk(price - 3, heatb):
        obook.add_bid(p, v)

    price, volume = obook.trade()

    prices[i] = price
    volumes[i] = volume

    print(i)

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


ohlcv = to_ohlcv(prices, volumes, interval)
columns = pd.Index(["open", "high", "low", "close", "volume"])
df = pd.DataFrame(ohlcv, columns=columns)

fig = make_subplots(
    rows=1,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.02,
)
fig.add_trace(
    go.Candlestick(
        x=df.index, open=df["open"], high=df["high"], low=df["low"], close=df["close"]
    ),
    row=1,
    col=1,
    secondary_y=False,
)
fig.update_layout(
    yaxis_title="Price",
    xaxis_rangeslider_visible=False,
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    template="plotly_dark",
    yaxis=dict(title="Price", anchor="x"),
)
fig.show()

exit()

print(price, datetime.now() - nw)

exit()

buys = np.array(obook.bids)
sels = np.array(obook.asks)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=np.cumsum(sels[:, 1]),
        y=sels[:, 0],
        name="Asks",
        mode="lines",
        line_shape="vh",
        line=dict(color="rgba(200, 0, 0, 0.6)"),
    )
)

fig.add_trace(
    go.Scatter(
        x=np.cumsum(buys[:, 1]),
        y=buys[:, 0],
        name="Bids",
        mode="lines",
        line_shape="vh",
        line=dict(color="rgba(0, 200, 0, 0.6)"),
    )
)

fig.add_hline(y=trade_price, line=dict(color="blue", dash="dash"))
fig.add_vline(x=trade_volume, line=dict(color="blue", dash="dash"))

fig.update_layout(xaxis_title="Volume", yaxis_title="Price", template="plotly_dark")
fig.show()
