import numpy as np
import plotly.graph_objects as go

omax = 128

bids = np.zeros([omax], dtype=np.float32)
asks = np.zeros([omax], dtype=np.float32)

bids[50:70] += np.random.random(omax)[50:70]
asks[50:70] += np.random.random(omax)[50:70]

ibids = np.nonzero(bids)[0]
iasks = np.nonzero(asks)[0]

bi = len(bids) - 1
si = 0

volume_bids = bids[bi]
volume_asks = asks[si]

while bi > si:
    if volume_bids < volume_asks:
        volume_bids += bids[bi]
        bi -= 1
    else:
        volume_asks += asks[si]
        si += 1


bids_cumsum = np.cumsum(bids[::-1])[::-1]
asks_cumsum = np.cumsum(asks)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=bids_cumsum,
        name="Bids",
        mode="lines",
        line_shape="hv",
        line=dict(color="rgba(0, 200, 0, 0.6)"),
    )
)

fig.add_trace(
    go.Scatter(
        x=asks_cumsum,
        name="Asks",
        mode="lines",
        line_shape="hv",
        line=dict(color="rgba(200, 0, 0, 0.6)"),
    )
)

fig.add_hline(y=bi, line=dict(color="yellow", dash="dash"))

fig.update_layout(xaxis_title="Volume", yaxis_title="Price", template="plotly_dark")

fig.show()
