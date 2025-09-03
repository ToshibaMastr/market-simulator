from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from rich.console import Console
from rich.progress import BarColumn, Progress, TimeRemainingColumn

from src.simulation import Simulation
from src.utils import to_dataframe

omax = 4000
steps = 30000
forward = 900
interval = 30

console = Console()


sim = Simulation(omax, omax // 2)

prices, volumes = np.zeros([steps]), np.zeros([steps])
price_matrix = np.full((omax, steps // interval), np.nan)


with Progress(
    "[bold blue]Generate[/] {task.completed}/{task.total}",
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    TimeRemainingColumn(),
) as progress:
    ptask = progress.add_task("training", total=steps)
    for i in range(steps):
        price, vol = sim.step()
        prices[i], volumes[i] = price, vol

        k = i // interval
        price_matrix[: price + 1, k] = sim.obook.bids[: price + 1]
        price_matrix[price:, k] = -sim.obook.asks[price:]

        progress.update(ptask, advance=1)


df = to_dataframe(prices, volumes, interval)

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
        colorbar=dict(title="OBook"),
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


exit()

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


def run_simulation():
    rsim = deepcopy(sim)
    heatmap = np.zeros((omax, forward // interval), dtype=int)

    for i in range(forward):
        price, _ = rsim.step()
        heatmap[price, i // interval] += 1

    return heatmap


heatmap = np.zeros((omax, forward // interval), dtype=int)
with ThreadPoolExecutor(max_workers=1) as executor:
    futures = [executor.submit(run_simulation) for _ in range(100)]

    for f in as_completed(futures):
        heatmap += f.result()


fig = make_subplots(
    rows=1,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.02,
)

fig.add_trace(
    go.Heatmap(
        z=heatmap,
        showscale=True,
    ),
    row=1,
    col=1,
    secondary_y=False,
)
fig.show()
