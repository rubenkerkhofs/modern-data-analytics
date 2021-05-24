import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from model import Model

from utils import Header, loadESG
from utils import loadDailyReturns, loadHeatwaves
import pandas as pd
import numpy as np

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


def GetVaRForecasts(r, ex):
    try:
        df_portfolio = pd.read_csv("data/df_portfolio.csv")
        total_value = sum(df_portfolio['Value (USD)'])
        model = Model(r, exogenous_regressor=ex)
        model.fit()
        mean_0, volatility_0 = model.forecast(exogenous=[0])
        mean_1, volatility_1 = model.forecast(exogenous=[1])
        VaR_0 = "$" + "{:,}".format(round(-(mean_0 - 2.326*volatility_0)*total_value, 2)).replace(',', ' ')
        VaR_1 = "$" + "{:,}".format(round(-(mean_1 - 2.326*volatility_1)*total_value, 2)).replace(',', ' ')
        mean_0, mean_1 = round(mean_0*100, 2), round(mean_1*100, 2)
        volatility_0, volatility_1 = round(volatility_0*100, 2), round(volatility_1*100, 2)
    except:
        VaR_0, VaR_1, mean_0, mean_1, volatility_0, volatility_1 = "-", "-", "-", "-", "-", "-"
    return VaR_0, VaR_1, mean_0, mean_1, volatility_0, volatility_1


def create_layout(app):
    esg_env, esg_soc, esg_gov = loadESG()
    daily_returns = loadDailyReturns().set_index('Date', drop=True)
    # Link heatwave data to the returns
    heatwaves = loadHeatwaves().set_index('Date', drop=True)
    daily_returns = daily_returns.join(heatwaves, how='left')
    daily_returns.loc[daily_returns['heatwave'].isna(), 
        'heatwave'] = 0
    daily_returns = daily_returns.reset_index()
    #  Construct figure and calculate key values
    stationary_figure = getStationaryFigure(daily_returns)
    VaR_0, VaR_1, mean_0, mean_1, volatility_0, volatility_1 = GetVaRForecasts(
        daily_returns.daily_returns, 
        daily_returns.heatwave)

    return html.Div(
        [
            Header(app),
            # page 4
            html.Div(
                [
                    # Row 1
                    html.Div(
                        # Global Heatwave data
                        [html.Div(
                            [html.H6(["Global heatwave data"],
                                     className="subtitle padded")],
                            className="twelve columns",
                        )],
                        className="row ",
                    ),
                    html.P("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."),

                    # Map
                    html.Div(
                        children=[
                            html.Img(src=app.get_asset_url("heat-waves-placeholder.jpg"),
                                     style={'height': '75%', 'width': '75%'})
                        ],
                        className='twelve columns',
                        style={'text-align': 'center'}
                    ),

                    # Country-specific data
                    html.Div(
                        [html.Div(
                            [html.H6(["Country-specific data"],
                                     className="subtitle padded")],
                            className="twelve columns",
                        )],
                        className="row ",
                    ),
                    html.P("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."),

                    # ESG section
                    html.Div(
                        [html.Div(
                            [html.H6(["ESG scores portfolio"],
                                     className="subtitle padded")],
                            className="twelve columns"
                        )],
                        className="row ",
                    ),
                    html.Div(children=[
                        html.P("These ESG Risk Ratings assess the degree to which a company’s enterprise business value is at risk driven by environmental, social and governance issues. A lower score is better. The scores range between 0 and 100."),
                        html.Div(children=[
                            html.Br([]),
                            html.P("Environmental", style={
                                   'font-size': '140%'}),
                            html.Br([]),
                            html.Img(src=app.get_asset_url("environment.png"),
                                     style={'height': '49%', 'width': '49%'}),
                            html.Br([]),
                            html.Br([]),
                            html.P(esg_env, style={'font-size': '250%'}),
                            html.Br([]),
                            html.P(
                                "Environmental factors range from a company’s greenhouse gas emissions to its treatment of animals.")
                        ],
                            className="four columns",
                            style={'text-align': 'center'}
                        ),
                        html.Div(children=[
                            html.Br([]),
                            html.P("Social", style={'font-size': '140%'}),
                            html.Br([]),
                            html.Img(src=app.get_asset_url("social.png"),
                                     style={'height': '45%', 'width': '45%'}),
                            html.Br([]),
                            html.Br([]),
                            html.P(esg_soc, style={'font-size': '250%'}),
                            html.Br([]),
                            html.P(
                                "Social factors examine a company’s business relationships with stakeholders throughout the supply chain.")
                        ],
                            className="four columns",
                            style={'text-align': 'center'}
                        ),
                        html.Div(children=[
                            html.Br([]),
                            html.P("Governance", style={'font-size': '140%'}),
                            html.Br([]),
                            html.Img(src=app.get_asset_url("governance.png"),
                                     style={'height': '45%', 'width': '45%'}),
                            html.Br([]),
                            html.Br([]),
                            html.P(esg_gov, style={'font-size': '250%'}),
                            html.Br([]),
                            html.P(
                                "The governance criteria evaluate legal and compliance issues and board operations.")
                        ],
                            className="four columns",
                            style={'text-align': 'center'}
                        ),

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
                                html.P(VaR_0, style={'font-size': '250%'}),
                                html.P("The expected 1 day return is equal to {ret}% with a volatility of {v}%.".format(ret=mean_0, v = volatility_0))
                                ],
                                className="six columns",
                                style={'text-align': 'center'}),
                            html.Div(children=[
                                html.P("Value at Risk - Heatwave"),
                                html.P(VaR_1, style={'font-size': '250%'}),
                                html.P("The expected 1 day return is equal to {ret}% with a volatility of {v}%.".format(ret=mean_1, v = volatility_1))
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
