from collections import defaultdict
import numpy as np
import plotly.graph_objects as go
from random import random
import heapq

from orderbook import OrderBook

from datetime import datetime, timedelta

class tick:
    def __init__(self):
        self.marks = defaultdict(timedelta)
        self.last = datetime.now()

    def pick(self, name: str):
        nw = datetime.now()
        self.marks[name] += nw - self.last
        self.last = nw

tcr = tick()

class OrderBookp:
    def __init__(self):
        self.bids = []
        self.asks = []

    def add_bid(self, price, volume):
        self.bids.append([price, volume])

    def add_ask(self, price, volume):
        self.asks.append([price, volume])

    def trade(self):
        self.bids.sort(reverse=True, key=lambda a : a[0])
        self.asks.sort(key=lambda a : a[0])

        bi, si = 0, 0
        trade_price = 0
        trade_volume = 0

        while bi < len(self.bids) and si < len(self.asks):
            pb, vb = self.bids[bi]
            ps, vs = self.asks[si]

            if pb < ps:
                break

            traded_volume = min(vb, vs)
            trade_price = (pb + ps) / 2

            self.bids[bi][1] -= traded_volume
            self.asks[si][1] -= traded_volume

            trade_volume += traded_volume

            if self.bids[bi][1] == 0:
                bi += 1
            if self.asks[si][1] == 0:
                si += 1

        self.bids = self.bids[bi:]
        self.asks = self.asks[si:]

        return trade_price, trade_volume


obook = OrderBook()
obookp = OrderBookp()
for _ in range(128):
    tcr.pick("step")
    for i in range(2048):
        price, volume = random(), random()
        obook.add_bid(price, volume)
        obookp.add_bid(price, volume)

        price, volume = random(), random()
        obook.add_ask(price, volume)
        obookp.add_ask(price, volume)

    trade_price, trade_volume = obook.trade()
    trade_pricep, trade_volume = obookp.trade()
    print(trade_price == trade_pricep)

for name, delta in tcr.marks.items():
    print(name, delta)

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
