import numpy as np
import plotly.graph_objects as go

from optim import crosspoint_np

np.random.seed(220)

omax = 128

bids = np.zeros([omax], dtype=np.float32)
asks = np.zeros([omax], dtype=np.float32)

bids[50:70] += np.random.random(omax)[50:70]
asks[50:70] += np.random.random(omax)[50:70]

bi = len(bids) - 1
si = 0


price, volume = crosspoint_np(bids, asks, omax)

bids[price:] = 0.0
asks[:price] = 0.0

bids_cumsum = np.cumsum(bids[::-1])[::-1]
asks_cumsum = np.cumsum(asks)


fig = go.Figure()

shape = "vh"

fig.add_trace(
    go.Scatter(
        x=bids_cumsum,
        name="Bids",
        mode="lines",
        line_shape=shape,
        line=dict(color="rgba(0, 200, 0, 0.6)"),
    )
)

fig.add_trace(
    go.Scatter(
        x=asks_cumsum,
        name="Asks",
        mode="lines",
        line_shape=shape,
        line=dict(color="rgba(200, 0, 0, 0.6)"),
    )
)

fig.add_hline(y=price, line=dict(color="yellow", dash="dash"))

fig.update_layout(xaxis_title="Volume", yaxis_title="Price", template="plotly_dark")

fig.show()
