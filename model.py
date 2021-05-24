import numpy as np
import pandas as pd

from arch import arch_model
import statsmodels.api as sm
import yfinance as yf

from utils import loadHeatwaves

import warnings
warnings.filterwarnings("ignore")


class Model:
    def __init__(self, r,
                 exogenous_regressor=None,
                 mean_model="ARX",
                 volatility_model="Garch",
                 p=1, q=1):
        # Define initial volatility model
        self.r = r
        self.arch_model = arch_model(self.r,
                                     x=exogenous_regressor,
                                     mean=mean_model,
                                     vol=volatility_model,
                                     p=p, q=q
                                     )
        self.ex = exogenous_regressor
        np.random.seed(123456)

    def __getGarchPredictions(self):
        # !!!!linear model optimized separately from GARCH model!!!!
        garch_estimates = []
        true_volatility = []
        for i in range(len(self.r)-100, len(self.r)-1):
            r_filtered = self.r[i-200:i]
            am = arch_model(r_filtered)
            am = am.fit(disp="off")
            forecasts = am.forecast(reindex=False)
            garch_estimates.append(forecasts.mean['h.1'].values[0])

            # Get true volatility
            r_filtered = self.r[i-99:i+1]
            true_volatility.append(np.std(r_filtered)**2)
        result = pd.DataFrame(true_volatility, columns=['true_volatility'])
        result.loc[:, 'garch_volatility_prediction'] = garch_estimates
        return result

    def fit(self):
        ######
        # !! Linear correction model and ARX + GARCH model are
        # Fitted independently -> suboptimal result!!
        ######

        # Fit the ARX + GARCH model
        self.res = self.arch_model.fit(disp="off")

        # Fit the linear correction model
        garch_pred = self.__getGarchPredictions()
        garch_pred.loc[:, 'dummy'] = np.random.uniform(
            0, 1, garch_pred.shape[0])
        garch_pred.dummy = garch_pred.dummy.apply(lambda x: int(x > 0.6))
        X = garch_pred[['garch_volatility_prediction', 'dummy']]
        X = sm.add_constant(X)
        y = garch_pred['true_volatility']
        mod = sm.OLS(y, X)
        mod = mod.fit()
        self.summary_lr = mod.summary() 

        # Save result for forecast
        self.intercept = mod.params['const']
        self.garch_vol = mod.params['garch_volatility_prediction']
        self.dummy_var = mod.params['dummy']

    def forecast(self, exogenous=None):
        if self.ex is None:
            forecasts = self.res.forecast(reindex=False)
            mean = forecasts.mean['h.1'].values[0]
            vol = np.sqrt(forecasts.variance['h.1'].values[0])
        else:
            forecasts = self.res.forecast(x=exogenous, reindex=False)
            mean = forecasts.mean['h.1'].values[0]
            vol = np.sqrt(self.intercept +
                          self.garch_vol*forecasts.variance['h.1'].values[0] +
                          self.dummy_var*exogenous[0])
        return mean, vol

    def summary(self):
        print(self.res.summary())
        print(self.summary_lr)


if __name__ == "__main__":
    index = yf.Ticker('XWD.TO')
    index_returns = index.history(period='10y')
    heatwaves = loadHeatwaves()
    index_returns = index_returns.merge(heatwaves, 
        on = "Date", how = "left")
    index_returns.loc[index_returns['heatwave'].isna(), 
        'heatwave'] = 0
    r = index_returns['Open']
    ex = index_returns['heatwave'][1:] 
    r = r.pct_change().dropna()
    model = Model(r, exogenous_regressor=ex)
    model.fit()
    mean, volatility = model.forecast(exogenous=[0])
    print(mean)
    print(volatility)
    mean, volatility = model.forecast(exogenous=[1])
    print(mean)
    print(volatility)