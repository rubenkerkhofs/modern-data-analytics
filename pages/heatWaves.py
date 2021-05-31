# Dash packages
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import plotly.express as px

# Models
from model import Model
from temperature_model import Model as Temperature_model
from statsmodels.tsa.seasonal import seasonal_decompose

# Utils functions and variables
from utils import Header, loadTemperatures, months
from utils import loadDailyReturns, loadHeatwaves

# Other required packages
import pandas as pd
import numpy as np
from datetime import date


##################
# HELPER FUNCTIONS
##################
def formatPredictions(predictions: pd.Series, previous_days: np.ndarray) -> tuple:
    assert len(previous_days) == 2, \
        "Previous days array should only have two elements: [yesterday, today]"
    preds = []
    pred_colors = []
    dates = []
    for pred in predictions.values:
        preds.append(str(round(pred, 1)) + "°C")
        if pred >= 32.2:
            pred_colors.append("red")
        else:
            pred_colors.append("green")
    for date in predictions.index:
        # Add the year back (see getTemperaturesPrediction())
        date = (date + pd.to_timedelta(365, unit='d'))
        dates.append(date.strftime("%d %B, %Y"))
    prediction = html.P("Next day is not a heatwave day",
                        style={"font-size": '140%', 'color': 'green'})
    if predictions.values[0] > 32.2 and previous_days[0] > 32.2 and previous_days[1] > 32.2:
        prediction = html.P("Next day is a heatwave day",
                            style={"font-size": '140%', 'color': 'red'})
    elif predictions.values[0] > 32.2 and predictions.values[1] > 32.2 and predictions.values[2] > 32.2:
        prediction = html.P("Next day is a heatwave day",
                            style={"font-size": '140%', 'color': 'red'})
    predictions_format = [
        html.Br([]),
        html.P("Forecasts next five days", style={'font-size': '150%'}),
        html.P(preds[0], style={
            'font-size': '140%', 'color': pred_colors[0]}),
        html.P(preds[1], style={
            'font-size': '140%', 'color': pred_colors[1]}),
        html.P(preds[2], style={
            'font-size': '140%', 'color': pred_colors[2]}),
        html.P(preds[3], style={
            'font-size': '140%', 'color': pred_colors[3]}),
        html.P(preds[4], style={
            'font-size': '140%', 'color': pred_colors[4]}),
        html.P("Today / Yesterday:"),
        html.P(
            "{t}°C / {y}°C".format(t=round(previous_days[1], 1), y=round(previous_days[0], 1)))
    ]
    dates_format = [
        html.Br([]),
        html.P("Dates", style={'font-size': '150%'}),
        html.P(dates[0], style={
            'font-size': '140%'}),
        html.P(dates[1], style={
            'font-size': '140%'}),
        html.P(dates[2], style={
            'font-size': '140%'}),
        html.P(dates[3], style={
            'font-size': '140%'}),
        html.P(dates[4], style={
            'font-size': '140%'}),
        prediction]
    return predictions_format, dates_format


def getCounty(heatwaves: pd.DataFrame) -> tuple:
    assert len(heatwaves.columns) == 5, \
        "Dataframe should have a five columns"
    heatwaves.columns = ['notes', 'county', 'county_code',
                         'avg_max_temp', 'avg_heat_index']
    maximum = max(heatwaves.avg_max_temp)
    county_largest = (heatwaves[heatwaves.avg_max_temp == maximum]
                      .county.values[0])
    return county_largest, maximum


def getHeatwavesPlot(heatwaves: pd.DataFrame) -> plotly.graph_objs.Figure:
    assert "avg_max_temp" in heatwaves.columns, \
        "Dataframe should have a column named: avg_max_temp"
    assert "year" in heatwaves.columns, \
        "Dataframe should have a column named: year"
    avg = np.mean(heatwaves.avg_max_temp)
    left_lim = min(heatwaves.year)
    right_lim = max(heatwaves.year)
    fig = px.bar(heatwaves, x='year', y='avg_max_temp',
                 width=425, height=200,
                 labels=dict(year="Year", avg_max_temp="# Heatwave days"))
    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='y',
                        x0=left_lim, y0=avg, x1=right_lim, y1=avg, line=dict(
                            color="Red")
                        ),
        row=1, col=1
    )
    fig.add_annotation(x=left_lim + 3, y=avg+0.1,
                       text="Average",
                       font=dict(color="red"),
                       arrowcolor="red")
    fig.update_layout(
        font_family="sans-serif",
        font_color="black",
        title_x=0.5,
        title_y=0.82,
        paper_bgcolor='rgba(0,0,0,0)',  # No background
        plot_bgcolor='rgba(0,0,0,0)',  # No background
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif"
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig


def getStationaryFigure(portfolio_returns: pd.DataFrame) -> dcc.Graph:
    assert "Date" in portfolio_returns.columns, \
        "Dataframe should have a column named: Date"
    assert "daily_returns" in portfolio_returns.columns, \
        "Dataframe should have a column named: daily_returns"

    return dcc.Graph(
        id="returns",
        figure={
            "data": [
                go.Scatter(
                    x=portfolio_returns["Date"],
                    y=portfolio_returns["daily_returns"],
                    line={"color": "#04437b"},
                    mode="lines",
                    name="Portfolio",
                )
            ],
            "layout": go.Layout(
                autosize=True,
                width=700,
                height=200,
                font={"family": "Raleway", "size": 10},
                margin={
                    "r": 30,
                    "t": 30,
                    "b": 30,
                    "l": 30,
                },
                showlegend=True,
                titlefont={
                    "family": "Raleway",
                    "size": 10,
                },
                xaxis={
                    "autorange": True,
                    "range": [
                        "2007-12-31",
                        "2018-03-06",
                    ],
                    "rangeselector": {
                        "buttons": [
                            {
                                "count": 1,
                                "label": "1Y",
                                "step": "year",
                                "stepmode": "backward",
                            },
                            {
                                "count": 3,
                                "label": "3Y",
                                "step": "year",
                                "stepmode": "backward",
                            },
                            {
                                "count": 5,
                                "label": "5Y",
                                "step": "year",
                            },
                            {
                                "count": 10,
                                "label": "10Y",
                                "step": "year",
                                "stepmode": "backward",
                            },
                            {
                                "label": "All",
                                "step": "all",
                            },
                        ]
                    },
                    "showline": True,
                    "type": "date",
                    "zeroline": False,
                },
                yaxis={
                    "autorange": True,
                    "range": [
                        18.6880162434,
                        278.431996757,
                    ],
                    "showline": True,
                    "type": "linear",
                    "zeroline": False,
                },
            ),
        },
        config={"displayModeBar": False},
    )


def getSummaryStats(heatwaves: pd.DataFrame) -> tuple:
    assert "avg_max_temp" in heatwaves.columns, \
        "Dataframe should have a column named: avg_max_temp"
    assert "year" in heatwaves.columns, \
        "Dataframe should have a column named: year"
    average = np.mean(heatwaves.avg_max_temp)
    maximum = max(heatwaves.avg_max_temp)
    maximum_year = heatwaves[heatwaves.avg_max_temp == maximum].year.values[0]
    return average, maximum, maximum_year


def getTemperatureAnomaliesPlot() -> plotly.graph_objs.Figure:
    df = pd.read_pickle("data/anomalies.pkl")
    df = df[['time', 'timeMax']]
    df.columns = ['date', 'anomaly_score']
    df.loc[:, "month"] = df.date.apply(lambda x: x.month)
    df_grouped = df.groupby("month", as_index=False).mean()
    fig = px.bar(df_grouped, x=months, y="anomaly_score",
                 width=425, height=250,
                 labels=dict(
                     anomaly_score="Average temperature anomaly", x=""),
                 title='Average temperature anomaly per month')
    fig.update_layout(
        font_family="sans-serif",
        font_color="black",
        title_x=0.5,
        title_y=1,
        yaxis_range=[0, 6],
        paper_bgcolor='rgba(0,0,0,0)',  # No background
        plot_bgcolor='rgba(0,0,0,0)',  # No background
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif"
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig


def getTemperatureAnomaliesTSPlot(start_year: int, end_year: int) -> plotly.graph_objs.Figure:
    df = pd.read_pickle("data/anomalies.pkl")
    df = df[['time', 'timeMax']]
    df.loc[:, "year"] = df.time.apply(lambda x: x.year)
    df = df[df.year <= end_year]
    df = df[df.year >= start_year]
    df = df.set_index("time")
    df = df.drop("year", axis=1)
    fig = px.line(df, title='Temperature anomalies in the {c} from {y1} to {y2}'.format(
                    c = "United States",
                    y1 = str(start_year),
                    y2 = str(end_year)),
                width=650, height=300,
                labels=dict(value="Maximum temperature anomaly", avg_max_temp="Year"))
    fig.update_layout(
        font_family="sans-serif",
        font_color="black",
        title_x=0.5,
        title_y=1,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',  # No background
        plot_bgcolor='rgba(0,0,0,0)',  # No background
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif"
        ),
        margin=dict(l=0, r=0, t=20, b=0)
    )
    return fig


def getTemperaturePredictions(df: pd.DataFrame) -> tuple:
    assert "DateMax" in df.columns, \
        "Dataframe should have a column named: DateMax"
    # Only use last five years to increase speed
    df = df.tail(365*5)
    # Go back one year in time to simulate realtime data
    day_of_year = date.today().timetuple().tm_yday
    df = df.head(len(df) - (365 - day_of_year))
    # Apply temperature model
    model = Temperature_model(df)
    model.fit()
    previous_temperatures = df.tail(2).DateMax.values
    return model.forecast(), previous_temperatures


def getTemperatureTrendPlot(temperatures: pd.DataFrame) -> plotly.graph_objs.Figure:
    assert "DateMax" in temperatures.columns, \
        "Dataframe should have a column named: DateMax"
    temperatures = temperatures.dropna()
    temperatures = temperatures.tail(365*60)
    temp = temperatures.DateMax.rolling(window=90).mean()
    fig = px.line(temp, title='Maximum temperature (90 day window rolling average)',
                  width=650, height=300,
                  labels=dict(value="Maximum temperature", avg_max_temp="Year"))
    fig.update_layout(
        font_family="sans-serif",
        font_color="black",
        title_x=0.5,
        title_y=1,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',  # No background
        plot_bgcolor='rgba(0,0,0,0)',  # No background
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif"
        ),
        margin=dict(l=0, r=0, t=20, b=0)
    )
    temp = seasonal_decompose(
        temperatures.DateMax, model='additive', extrapolate_trend='freq', freq=365*10)
    fig.add_scatter(x=temp.trend.index, y=temp.trend.values,
                    mode='lines', opacity=.7)
    fig.add_annotation(x=1970, y=temp.trend['1970-01-15'],
                       text="Trend line",
                       font=dict(color="red"),
                       arrowcolor="red")
    return fig


def getVaRForecasts(returns: pd.Series, exogenous: pd.Series) -> tuple:
    try:  # If no portfolio defined, this crashes
        # Get the total portfolio value
        df_portfolio = pd.read_csv("data/df_portfolio.csv")
        total_value = sum(df_portfolio['Value (USD)'])

        # Initiate, fit and forecast using the model.py class
        model = Model(returns, exogenous_regressor=exogenous)
        model.fit()
        mean_0, volatility_0 = model.forecast(exogenous=[0])
        mean_1, volatility_1 = model.forecast(exogenous=[1])

        # Formatting the outputs
        VaR_0 = "$" + \
            "{:,}".format(round(-(mean_0 - 2.326*volatility_0)
                          * total_value, 2)).replace(',', ' ')
        VaR_1 = "$" + \
            "{:,}".format(round(-(mean_1 - 2.326*volatility_1)
                          * total_value, 2)).replace(',', ' ')
        mean_0, mean_1 = round(mean_0*100, 2), round(mean_1*100, 2)
        volatility_0, volatility_1 = round(
            volatility_0*100, 2), round(volatility_1*100, 2)
    except:
        VaR_0, VaR_1, mean_0, mean_1, volatility_0, volatility_1 = "-", "-", "-", "-", "-", "-"
    return VaR_0, VaR_1, mean_0, mean_1, volatility_0, volatility_1


#############################
# LAYOUT FUNCTION USED BY APP
#############################
def create_layout(app):
    daily_returns = loadDailyReturns().set_index('Date', drop=True)

    # Link heatwave data to the returns
    heatwaves = loadHeatwaves()
    daily_returns = daily_returns.join(heatwaves, how='left')
    daily_returns.loc[daily_returns['heatwave'].isna(),
                      'heatwave'] = 0
    daily_returns = daily_returns.reset_index()

    #  Construct figure and calculate key values
    error_message_var0, error_message_var1 = "", ""
    stationary_figure = getStationaryFigure(daily_returns)
    VaR_0, VaR_1, mean_0, mean_1, volatility_0, volatility_1 = getVaRForecasts(
        daily_returns.daily_returns,
        daily_returns.heatwave)
    if VaR_0 is np.NaN:
        error_message_var0 = "Solution did not convergence. This can happen during live trading, please restart the app and try again."
    if VaR_1 is np.NaN:
        error_message_var1 = "Solution did not convergence. This can happen during live trading, please restart the app and try again."
    # Download yearly heatwave summary statistics
    hwy = pd.read_table("data/df_heat_waves_yearly.txt")
    hwy.columns = ['notes', 'year', 'avg_max_temp', 'avg_heat_index']
    avg_heatwaves, max_heatwaves, max_heatwaves_year = getSummaryStats(hwy)
    figure = getHeatwavesPlot(hwy)

    # Download county heatwave data 2020 and get insights
    hwc = pd.read_table("data/df_heat_waves_2020.txt")
    county, max_county = getCounty(hwc)

    # Predict heatwaves and construct figures
    temperatures = loadTemperatures()
    figure_temperature_trend = getTemperatureTrendPlot(temperatures)
    predictions, previous_days = getTemperaturePredictions(temperatures)
    predictions, dates = formatPredictions(predictions, previous_days)

    # Discuss temperature anomalies
    anomalies_plot = getTemperatureAnomaliesPlot()

    return html.Div(
        [
            Header(app),
            # page 4
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [html.Div(
                            [html.H6(["Select your country"],
                                     className="subtitle padded")],
                            className="twelve columns",
                        )],
                        className="row ",
                    ),
                    html.Div(
                        [
                            # Information about how to add country
                            html.Div(
                                [
                                    html.P(["Select the country from which you would like to use the heatwave data as well as the date range."], style={
                                           "color": "#7a7a7a"})
                                ],
                                className="three columns",
                            ),
                            # Country
                            html.Div(
                                [
                                    html.P(["Country"], style={
                                           "color": "#7a7a7a"}),
                                    dcc.Dropdown(
                                        id='country-selection',
                                        options=[
                                            {'label': 'United States', 'value': 'US'}
                                        ],
                                        value='US'
                                    )
                                ],
                                className="three columns",
                            ),
                            # Add date
                            html.Div(
                                [
                                    html.P(["At the moment only US. The code has been written in such a way that is supports multiple countries but because the scraping of data takes too long it is not implemented."], style={
                                           "color": "#7a7a7a"})
                                ],
                                className="six columns",
                            )
                        ],
                        className="row ",
                    ),

                    html.Br([]),

                    # Country-specific data
                    html.Div(
                        [html.Div(
                            [html.H6(["Country-specific data"],
                                     className="subtitle padded")],
                            className="twelve columns",
                        )],
                        className="row ",
                    ),
                    html.H5("Summary statistics", style={
                            'font-size': '150%', "text-decoration": "underline"}),
                    html.Br([]),
                    html.Div(
                        [
                            html.Div(children=[
                                     html.P("Average heatwave days per year (averaged over counties)", style={
                                            'font-size': '140%'}),
                                     html.P(round(avg_heatwaves, 2),
                                            style={'font-size': '250%'}),
                                     html.Br([]),
                                     html.P("Maximum number of heatwave days (averaged over counties)", style={
                                            'font-size': '140%'}),
                                     html.P(round(max_heatwaves, 0),
                                            style={'font-size': '250%'}),
                                     html.P("achieved in {}".format(
                                         max_heatwaves_year), style={'font-size': '140%'})

                                     ],
                                     className="four columns",
                                     style={'text-align': 'center'}),
                            html.Div(children=[
                                html.Br([]),
                                dcc.Graph(figure=figure)

                            ],
                                className="eight columns")

                        ],
                        className="row"
                    ),
                    html.Br([]),
                    html.Div(children=[
                        html.Div(children=[
                            html.P("County with largest number of heatwave days in 2020", style={
                                'font-size': '140%'}),
                            html.P(county, style={'font-size': '250%'})
                        ],
                            className="eight columns",
                            style={'text-align': 'center'},
                        ),
                        html.Div(children=[
                            html.P("Heatwave days", style={
                                'font-size': '140%'}),
                            html.P(round(max_county, 2),
                                   style={'font-size': '250%'})
                        ],
                            className="four columns",
                            style={'text-align': 'center'})
                    ],
                        className="row"),
                    html.Br([]),
                    html.Br([]),
                    html.H5("Temperature trend analysis", style={
                            'font-size': '150%', "text-decoration": "underline"}),
                    html.Br([]),
                    html.Br([]),
                    dcc.Graph(figure=figure_temperature_trend),
                    html.Br([]),
                    html.P("The maximum daily temperature has been steadily increasing during the last 60 years. This leads to an increase in the number of heatwaves that occur."),

                    html.H5("Temperature anomalies", style={
                            'font-size': '150%', "text-decoration": "underline"}),
                    html.Br([]),
                    html.Br([]),
                    html.Div(children=[
                        html.Div(dcc.Graph(figure=anomalies_plot),
                                 className="eight columns"),
                        html.Div(html.P("The plot on the left-hand side shows that the average temperature anomaly is greater than one for every month. This indicates that the effects of global warming are noticeable during all parts of the year. The fact that the average temperature anomaly is largest during the winter months indicates that winters are becoming warmer at a faster pace compared to the summers."),
                                 className="four columns")
                    ],
                        className="row"),
                    html.Br([]),
                    html.Br([]),
                    html.Div(
                        [html.Div([
                            html.P(["Explore the evolution of temperature anomalies during a given time period."], style={
                                           "color": "#7a7a7a"})],
                                className="three columns",
                            ),
                            html.Div(
                                [
                                    html.P(
                                        "Start year:"
                                    ),
                                    dcc.Input(
                                        id='start-year',
                                        type='number', min=1947, max=2021,
                                        placeholder=1947, step=1
                                    ),
                                    html.P("", style={"color": "#FF0000"}, id="start-year-error")
                                ],
                                className="two columns",
                                style={"color": "#696969"},
                            ),
                            html.Div(
                                [html.P("")],
                                className="two columns",
                                style={"color": "#696969"},
                            ),
                            html.Div(
                                [
                                    html.P(
                                        "End year:"
                                    ),
                                    dcc.Input(
                                        id='end-year',
                                        type='number', min=1947, max=2021,
                                        placeholder=2021, step=1
                                    ),
                                    html.P("", style={"color": "#FF0000"}, id="end-year-error")
                                ],
                                className="two columns",
                                style={"color": "#696969"},
                            ),
                            html.Div(
                                [html.P("")],
                                className="two columns",
                                style={"color": "#696969"},
                            ),
                            html.Div(
                                [
                                    html.P(
                                        "Apply years"
                                    ),
                                    html.Button('Apply',
                                                id='apply-years',
                                                n_clicks=0
                                                )
                                ],
                                className="two columns",
                                style={"color": "#696969"},
                            ),
                            ],
                            className="row"
                    ),
                    html.Br([]),
                    html.Br([]),
                    dcc.Graph(figure=getTemperatureAnomaliesTSPlot(1947, 2021), id="temperature-anomalies"),
                    html.Br([]),
                    html.Br([]),
                    html.H5("Heat Wave forecasts", style={
                            'font-size': '150%', "text-decoration": "underline"}),
                    html.P("A SARIMAX model is used to forecast the temperature over the next five years. The model is trained using daily temperature data of the last five years. To determine the optimal parameters, the AIC was used."),
                    html.Br([]),
                    html.Div(children=[
                        html.Div(children=predictions,
                                 className="four columns",
                                 style={'text-align': 'center'}),
                        html.Div(children=dates,
                                 className="three columns",
                                 style={'text-align': 'center'}),
                        html.Div(children=html.Br([]),
                                 className="one column",
                                 style={'text-align': 'center'}),
                        html.Div(children=[
                            html.P("Heatwave definition", style={
                                   "text-decoration": "underline"}),
                            html.P(
                                "A heatwave occurs when the temperature exceeds 32.2°C for at least three consecutive days. All days that belong to the heatwave period are considered heatwave days.")
                        ],
                            className="four columns product")

                    ],
                        className="row"),
                    html.Div(children=[
                        # Exposure to heat wave risk
                        html.Div(
                            [html.Div(
                                [html.H6(["Exposure to heat wave risk"],
                                         className="subtitle padded")],
                                className="twelve columns"
                            )],
                            className="row ",
                        ),
                        html.P(
                            "The impact of heatwaves on our portfolio is assessed by exploring the historical volatility and expected return."),

                        # Figure of stationary returns
                        html.Div(
                            children=[stationary_figure],
                            className=" six columns",
                            id='fig-sector-diversification'
                        ),

                        html.Div([
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                        ]),

                        html.P("The effect of a heatwave on the expected return is estimated by using an ARX-GARCH model with a heatwave indicator variable as an external regressor in the mean model. This ARX-GARCH model also provides an estimate for the volatility, however, this estimate is not influenced by the heatwave indicator variable. A separate linear regression model is trained on historic data to allow the heatwave indicator to correct the volatility estimate. Both models are trained specifically for the portfolio chosen by the user."),
                        html.Br([]),

                        html.Div(
                            children=[
                                html.Div(children=[
                                    html.P("Value at Risk - No heatwave"),
                                    html.P(VaR_0, style={'font-size': '250%'}),
                                    html.P("The expected 1 day return is equal to {ret}% with a volatility of {v}%.".format(
                                        ret=mean_0, v=volatility_0)),
                                    html.P(error_message_var0, style={"color": "red"})
                                ],
                                    className="six columns",
                                    style={'text-align': 'center'}),
                                html.Div(children=[
                                    html.P("Value at Risk - Heatwave"),
                                    html.P(VaR_1, style={'font-size': '250%'}),
                                    html.P("The expected 1 day return is equal to {ret}% with a volatility of {v}%.".format(
                                        ret=mean_1, v=volatility_1)),
                                    html.P(error_message_var1, style={"color": "red"})
                                ],
                                    className="six columns",
                                    style={'text-align': 'center'})
                            ],
                            className="row"
                        )

                    ],
                        className="row")



                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
