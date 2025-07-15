import numpy as np


class OrderBook:
    # Логика оч сложная|медленная, по этому стоит переделать

    def __init__(self, omax):
        self.buy = np.zeros([omax], dtype=np.float32)
        self.sell = np.zeros([omax], dtype=np.float32)

    def crosspoint(self):
        bi = len(self.buy) - 1
        si = 0

        volume_buy = self.buy[bi]
        volume_sell = self.sell[si]

        while bi > si:
            if volume_buy < volume_sell:
                volume_buy += self.buy[bi]
                bi -= 1
            else:
                volume_sell += self.sell[si]
                si += 1

        return bi, min(volume_buy, volume_sell)

    def trade(self, price: int):
        self.buy[price:] = 0.0
        self.sell[: price + 1] = 0.0

        self.buy *= 0.9995
        self.sell *= 0.9995


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
        volumes = np.random.random(len(prb))
        volumes = np.random.exponential(scale=1.0, size=len(prb))
        np.add.at(obook, prb, volumes)

    def step(self):
        heatb = int(np.random.lognormal(mean=0, sigma=1, size=None) * 100)
        heats = abs(heatb + np.random.randint(-5, 6))

        self.addbk(self.obook.buy, self.price - 3, heatb)
        self.addbk(self.obook.sell, self.price + 3, heats)

        self.price, vol = self.obook.crosspoint()
        self.obook.trade(self.price)
        return self.price, vol
