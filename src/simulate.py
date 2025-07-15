import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .simulation import Simulation

omax = 4000

steps = 30000

interval = 30

sim = Simulation(omax, omax // 2)

price_matrix = np.full((omax, steps // interval), np.nan)

prices = np.zeros([steps])
volumes = np.zeros([steps])

for i in range(steps):
    price, vol = sim.step()

    prices[i] = price
    volumes[i] = vol

    k = i // interval
    price_matrix[: price + 1, k] = sim.obook.bids[: price + 1]
    price_matrix[price:, k] = -sim.obook.asks[price:]

    print(k, price)


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
fig.add_trace(
    go.Heatmap(
        z=price_matrix,
        colorscale=[[0.0, "red"], [0.5, "black"], [1.0, "green"]],
        colorbar=dict(title="Price"),
        showscale=True,
        zmin=-np.max(price_matrix),
        zmid=0,
        zmax=np.max(price_matrix),
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

buy_depth = np.cumsum(sim.obook.bids[::-1])[::-1]
sell_depth = np.cumsum(sim.obook.asks)

buy_prices = np.arange(len(sim.obook.bids))
sell_prices = np.arange(len(sim.obook.asks))

fig_depth = go.Figure()

fig_depth.add_trace(
    go.Scatter(
        x=buy_prices,
        y=buy_depth,
        mode="lines",
        name="Bid",
        line=dict(color="green"),
        line_shape="hv",
        fill="tozeroy",
    )
)

fig_depth.add_trace(
    go.Scatter(
        x=sell_prices,
        y=sell_depth,
        mode="lines",
        name="Ask",
        line=dict(color="red"),
        line_shape="hv",
        fill="tozeroy",
    )
)

fig_depth.update_layout(
    title="OBook",
    xaxis_title="Price",
    yaxis_title="Cumulative Volume",
    template="plotly_dark",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
)
fig_depth.show()
