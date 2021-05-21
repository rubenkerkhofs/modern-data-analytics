import numpy as np
import pandas as pd

from arch import arch_model
import yfinance as yf

import warnings
warnings.filterwarnings("ignore")


class Model:
    def __init__(self, r,
                 exogenous_regressor=None,
                 mean_model="AR",
                 volatility_model="Garch",
                 p=1, q=1):
        # Define initial volatility model
        self.arch_model = arch_model(r,
                                     x=exogenous_regressor,
                                     mean=mean_model,
                                     vol=volatility_model,
                                     p=p, q=q
                                     )

    def fit(self):
        self.res = self.arch_model.fit(disp="off")

    def forecast(self):
        forecasts = self.res.forecast(reindex=False)
        return forecasts.mean['h.1'].values[0], np.sqrt(forecasts.variance['h.1'].values[0])

    def summary(self):
        print(self.res.summary())


if __name__ == "__main__":
    index = yf.Ticker('XWD.TO')
    index_returns = index.history(period='10y')
    r = index_returns['Open']
    r = r.pct_change().dropna()
    model = Model(r)
    model.fit()
    mean, volatility = model.forecast()
