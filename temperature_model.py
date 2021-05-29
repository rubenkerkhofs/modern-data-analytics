from numpy import disp
import statsmodels.api as sm
from datetime import date, timedelta

import pandas as pd


import warnings
warnings.filterwarnings("ignore")

class Model:
    def __init__(self, temperatures):
        self.temperatures = temperatures
        # Parameters of the model have been determined based
        # on the AIC
        self.model = sm.tsa.statespace.SARIMAX(temperatures,
                                order=(0, 0, 3),
                                seasonal_order=(0, 1, 3, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
        self.fitted_model = None
    
    def fit(self):
        self.fitted_model = self.model.fit(disp=False)

    def diagnostics(self):
        assert self.fitted_model is not None, \
            "Fit model first before calling summary method"
        self.fitted_model.plot_diagnostics(figsize=(15, 12))
        

    def forecast(self, n = 5):
        assert self.fitted_model is not None, \
            "Fit model first before calling summary method"
        prediction = self.fitted_model.get_forecast(steps=n)
        return prediction.predicted_mean
    
    def summary(self):
        assert self.fitted_model is not None, \
            "Fit model first before calling summary method"
        print(self.fitted_model.summary().tables[1])

