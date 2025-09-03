import numpy as np

from optim import crosspoint_np


class OrderBook:
    def __init__(self, omax):
        self.bids = np.zeros([omax], dtype=np.float32)
        self.asks = np.zeros([omax], dtype=np.float32)
        self.omax = omax

    def crosspoint(self):
        return crosspoint_np(self.asks, self.bids, self.omax)

    def trade(self, price: int):
        self.bids[price:] = 0.0
        self.asks[: price + 1] = 0.0

        self.bids *= 0.9995
        self.asks *= 0.9995


class Simulation:
    def __init__(self, omax: int, price: int):
        self.omax = omax
        self.price = price
        self.obook = OrderBook(omax)

    def obookgen(self, heat: int, price: int):
        p = np.random.normal(0, 10, heat).round().astype(np.int32) + price
        return p[(p >= 0) & (p < self.omax)]

    def addbk(self, obook: np.ndarray, price: int, heat: int):
        prb = self.obookgen(heat, price)
        # volumes = np.random.random(len(prb))
        volumes = np.random.exponential(scale=1.0, size=len(prb))
        np.add.at(obook, prb, volumes)

    def step(self):
        heatb = int(np.random.lognormal(0, 1) * 100)
        heats = abs(heatb + np.random.randint(-5, 6))

        self.addbk(self.obook.bids, self.price - 3, heatb)
        self.addbk(self.obook.asks, self.price + 3, heats)

        self.price, vol = self.obook.crosspoint()
        self.obook.trade(self.price)

        return self.price, vol
