# Dash packages
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px

# Utils functions and variables
from utils import Header, loadReturns
from utils import loadColors, loadMetrics, loadDailyReturns

# Other required packages
import pandas as pd
import numpy as np
import yfinance as yf

##################
# HELPER FUNCTIONS
##################


def getHistogram(df: pd.DataFrame) -> dcc.Graph:
    assert "daily_returns" in df.columns,\
        "Dataframe should have a column named: daily_returns"

    fig = px.histogram(df, x="daily_returns",
                       width=300, height=150,
                       labels=dict(daily_returns="Daily return"),
                       color_discrete_sequence=["#04437b"])

    try:  # If no portfolio selected, this fails
        VaR = np.percentile(df['daily_returns'], 1)
    except:
        VaR = 0
    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='y',
                        x0=VaR, y0=0, x1=VaR, y1=150, line=dict(color="Red")
                        ),
        row=1, col=1
    )
    fig.add_annotation(x=VaR, y=140,
                       text="VaR",
                       font=dict(color="red"),
                       arrowcolor="red")
    fig.update_layout(
        font_family="sans-serif",
        font_color="black",
        title_x=0.5,
        title_y=0.82,
        yaxis_visible=False,
        yaxis_showticklabels=False,
        paper_bgcolor='rgba(0,0,0,0)',  # No background
        plot_bgcolor='rgba(0,0,0,0)',  # No background
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif"
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return dcc.Graph(figure=fig)


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
                width=450,
                height=185,
                font={"family": "Raleway", "size": 10},
                margin={
                    "r": 30,
                    "t": 30,
                    "b": 30,
                    "l": 30,
                },
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
                        -1, 1
                    ],
                    "showline": True,
                    "type": "linear",
                    "zeroline": False,
                },
            ),
        },
        config={"displayModeBar": False},
    )


#############################
# LAYOUT FUNCTION USED BY APP
#############################
def create_layout(app):
    # Load all necessary information and calculate metrics
    portfolio_returns = pd.read_csv('data/df_portfolio_returns.csv')
    index = yf.Ticker('XWD.TO')
    index_returns = index.history(period='10y')
    return_1y, return_5y, return_10y, return_1y_i, return_5y_i, return_10y_i = loadReturns(
        portfolio_returns, index_returns)
    color_10, color_5, color_1 = loadColors(return_1y, return_5y, return_10y,
                                            return_1y_i, return_5y_i, return_10y_i)
    beta, VaR, standev = loadMetrics()
    daily_returns = loadDailyReturns()
    stationary_figure = getStationaryFigure(daily_returns)
    histogram = getHistogram(daily_returns)
    return html.Div(
        [
            Header(app),
            # page 2
            html.Div(
                [
                    # Performance and plot
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Performance",
                                            className="subtitle padded"),
                                    html.P("In order to gauge performance we can compare the returns of the portfolio to the MSCI world index,  a market cap weighted stock market index of 1,585 companies throughout the world."),
                                    dcc.Graph(
                                        id="returns",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=portfolio_returns["Date"],
                                                    y=portfolio_returns["Return"],
                                                    line={"color": "#04437b"},
                                                    mode="lines",
                                                    name="Portfolio",
                                                ),
                                                go.Scatter(
                                                    x=index_returns.index,
                                                    y=index_returns['Close'],
                                                    line={"color": "#b5b5b5"},
                                                    mode="lines",
                                                    name="MSCI World Index",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                width=700,
                                                height=200,
                                                font={"family": "Raleway",
                                                      "size": 10},
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
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),

                    # Key numbers
                    html.Div(
                        html.H6("Key numbers", className="subtitle padded"),
                        className="row"
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Br([]),
                                    html.Br([]),
                                    html.P("Return (10y)",
                                           style={'font-size': '140%'}),
                                    html.P(str(return_10y) + "%",
                                           style={'font-size': '250%', 'color': color_10}),
                                    html.P("The return on 10 years of the portfolio is equal to {port_10}% compared to the performance of the MSCI World Index of {in_10}%.".format(
                                        port_10=return_10y,
                                        in_10=return_10y_i
                                    ), style={'font-size': '90%'}
                                    )
                                ],
                                className="four columns",
                                style={'text-align': 'center'}
                            ),
                            html.Div(
                                [
                                    html.Br([]),
                                    html.Br([]),
                                    html.P("Return (5y)",
                                           style={'font-size': '140%'}),
                                    html.P(str(return_5y) + "%",
                                           style={'font-size': '250%', 'color': color_5}),
                                    html.P("The return on 5 years of the portfolio is equal to {port_10}% compared to the performance of the MSCI World Index of {in_10}%.".format(
                                        port_10=return_5y,
                                        in_10=return_5y_i
                                    ), style={'font-size': '90%'}
                                    )
                                ],
                                className="four columns",
                                style={'text-align': 'center'}
                            ),
                            html.Div(
                                [
                                    html.Br([]),
                                    html.Br([]),
                                    html.P("Return (1y)",
                                           style={'font-size': '140%'}),
                                    html.P(str(return_1y) + "%",
                                           style={'font-size': '250%', 'color': color_1}),
                                    html.P("The return on 1 year of the portfolio is equal to {port_10}% compared to the performance of the MSCI World Index of {in_10}%.".format(
                                        port_10=return_1y,
                                        in_10=return_1y_i
                                    ), style={'font-size': '90%'}
                                    )
                                ],
                                className="four columns",
                                style={'text-align': 'center'}
                            )

                        ],
                        className="row"
                    ),

                    # Risk assessment title
                    html.Div(
                        html.H6("Risk assessment",
                                className="subtitle padded"),
                        className="row ",
                    ),
                    # Image, volatility and standev
                    html.Div(
                        children=[
                            html.Br([]),
                            html.Br([]),
                            html.Div(
                                children=[stationary_figure],
                                className='eight columns'
                            ),
                            html.Div(
                                children=[
                                    html.Br([]),
                                    html.Br([]),
                                    html.Br([]),
                                    html.Br([]),
                                    html.P("Standard deviation (1 day)",
                                           style={'font-size': '140%'}),
                                    html.P(standev,  style={
                                           'font-size': '250%'})
                                ],
                                className='four columns',
                                style={'text-align': 'center'}
                            )
                        ],
                        className="row"
                    ),
                    # Value at risk and beta
                    html.Div(children=[
                        html.Br([]),
                        html.Br([]),
                        html.Br([]),
                        html.Br([]),
                        html.Div(children=[
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.P("VaR 1% (non-parametric)",
                                   style={'font-size': '140%'}),
                            html.P(VaR, style={'font-size': '250%'}),
                            html.P("The VaR represents the potential loss in the portfolio given the probability of occurrence for the defined loss.")
                        ],
                            className='four columns',
                            style={'text-align': 'center'}),

                        html.Div(children=[
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),
                            html.P("Portfolio Beta", style={
                                   'font-size': '140%'}),
                            html.P(beta, style={'font-size': '250%'}),
                            html.P("The beta value is given by the change in the value of the portfolio given a change in the market.")
                        ],
                            className='three columns',
                            style={'text-align': 'center'}),

                        html.Div(children=[
                            histogram,
                            ],
                            className='five columns'),
                         ],
                        className="row"),
                        html.Br([]),
                        html.Br([]),
                        html.Div(html.A('Check the impact of heatwaves on your portfolio', href="/dash-financial-report/heatWaves", id="next-page"),
                            style={"textAlign": "right", 'font-size': '150%', "text-decoration": "underline"})
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )


