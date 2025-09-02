use pyo3::prelude::*;

#[pyclass]
struct OrderBook {
    bids: Vec<(f64, f64)>,
    asks: Vec<(f64, f64)>,
}

#[pymethods]
impl OrderBook {
    #[new]
    fn new() -> Self {
        OrderBook {
            bids: Vec::new(),
            asks: Vec::new(),
        }
    }

    fn add_bid(&mut self, price: f64, volume: f64) {
        self.bids.push((price, volume));
    }

    fn add_ask(&mut self, price: f64, volume: f64) {
        self.asks.push((price, volume));
    }

    fn trade(&mut self) -> (f64, f64) {
        self.bids.sort_by(|a, b| b.0.partial_cmp(&a.0).unwrap());
        self.asks.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

        let mut bi = 0;
        let mut si = 0;
        let mut trade_price = 0.0;
        let mut trade_volume = 0.0;

        while bi < self.bids.len() && si < self.asks.len() {
            let (pb, vb) = self.bids[bi];
            let (ps, vs) = self.asks[si];

            if pb < ps {
                break;
            }

            let traded_volume = vb.min(vs);
            trade_price = (pb + ps) / 2.0;
            self.bids[bi].1 -= traded_volume;
            self.asks[si].1 -= traded_volume;
            trade_volume += traded_volume;

            if self.bids[bi].1 == 0.0 {
                bi += 1;
            }
            if self.asks[si].1 == 0.0 {
                si += 1;
            }
        }

        self.bids.drain(0..bi);
        self.asks.drain(0..si);

        (trade_price, trade_volume)
    }

    fn get_bids(&self) -> Vec<(f64, f64)> {
        self.bids.clone()
    }

    fn get_asks(&self) -> Vec<(f64, f64)> {
        self.asks.clone()
    }
}

#[pymodule]
fn orderbook(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<OrderBook>()?;
    Ok(())
}
