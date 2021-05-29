import dash_html_components as html
import dash_core_components as dcc
from model import Model

import plotly.graph_objs as go
import pandas as pd
from utils import Header, make_dash_table, loadESG, loadDailyReturns


def getStationaryFigure(portfolio_returns):
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


def GetVaRForecasts(r):
    try:
        df_portfolio = pd.read_csv("data/df_portfolio.csv")
        total_value = sum(df_portfolio['Value (USD)'])
        model = Model(r)
        model.fit()
        mean, volatility = model.forecast()
        VaR = "$" + str(round(-(mean - 1.96*volatility)*total_value, 2))
    except:
        VaR = "-"
    return VaR


def create_layout(app):
    daily_returns = loadDailyReturns()
    stationary_figure = getStationaryFigure(daily_returns)
    VaR = GetVaRForecasts(daily_returns.daily_returns)

    return html.Div(
        [
            Header(app),
            # page 4
            html.Div(
                [
                    # Exposure to heat wave risk
                    html.Div(
                        [html.Div(
                            [html.H6(["Exposure to heat wave risk"],
                                     className="subtitle padded")],
                            className="twelve columns"
                        )],
                        className="row ",
                    ),
                    html.P("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."),

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

                    html.P("In order to estimate the exposure to heat waves, we estimate the VaR using an AR-GARCH model with and without heat wave information as an external regressor."),
                    html.Br([]),

                    html.Div(
                        children=[
                            html.Div(children=[
                                html.P("Value at Risk - No heatwave"),
                                html.P(VaR, style={'font-size': '250%'})
                            ],
                                className="six columns",
                                style={'text-align': 'center'}),
                            html.Div(children=[
                                html.P("Value at Risk - Heatwave"),
                                html.P(VaR, style={'font-size': '250%'})
                            ],
                                className="six columns",
                                style={'text-align': 'center'})
                        ],
                        className="row"
                    )
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )