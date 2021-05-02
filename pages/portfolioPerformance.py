import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import Header, make_dash_table
import pandas as pd
import yfinance as yf

# Load the portfolio returns
portfolio_returns = pd.read_csv('data/df_portfolio_returns.csv')
# Load the historic index return
index = yf.Ticker('XWD.TO')
index_returns = index.history(period='10y')


def create_layout(app):
    portfolio_returns = pd.read_csv('data/df_portfolio_returns.csv')
    return_10y, return_10y_i  = "-", "-"
    return_5y, return_5y_i = "-", "-"
    return_1y, return_1y_i = "-", "-"
    color_10, color_5, color_1 = 'black', 'black', 'black' 
    if portfolio_returns.shape[0] > 0:
        # Simulate equal start investment in index
        start_investment = portfolio_returns.Return[0]
        index_start = index_returns['Close'][0]
        ratio = start_investment/index_start
        index_returns.Close = index_returns['Close']*ratio
        days = portfolio_returns.shape[0]
        days_i = index_returns.shape[0]
        now = portfolio_returns.Return[days-1]
        ago_5y = portfolio_returns.Return[days-5*365-1]
        ago_1y = portfolio_returns.Return[days-366]
        index_5y = index_returns['Close'][days_i-5*365-1]
        index_1y = index_returns['Close'][days_i-365]
        index_now = index_returns['Close'][days_i-1]
        return_10y = round((now - start_investment)*100/start_investment,2)
        return_5y = round((now - ago_5y)*100/ago_5y,2)
        return_1y = round((now - ago_1y)*100/ago_1y,2)
        return_10y_i = round((index_now - start_investment)*100/start_investment,2)
        return_5y_i = round((index_now - index_5y)*100/index_5y,2)
        return_1y_i = round((index_now - index_1y)*100/index_1y,2)
        color_10, color_5, color_1 = 'red', 'red', 'red' 
        if return_10y > return_10y_i:
            color_10 = 'green'
        if return_5y > return_5y_i:
            color_5 = 'green'
        if return_1y > return_1y_i:
            color_1 = 'green'
        
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
                                html.H6("Performance", className="subtitle padded"),
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
                                style={'font-size':'140%'}),
                            html.P(str(return_10y) + "%",
                            style={'font-size':'250%', 'color': color_10}),
                            html.P("The return on 10 years of the portfolio is equal to {port_10}% compared to the performance of the MSCI World Index of {in_10}%.".format(
                                port_10 = return_10y,
                                in_10 = return_10y_i
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
                                style={'font-size':'140%'}),
                            html.P(str(return_5y) + "%",
                            style={'font-size':'250%', 'color': color_5}),
                            html.P("The return on 5 years of the portfolio is equal to {port_10}% compared to the performance of the MSCI World Index of {in_10}%.".format(
                                port_10 = return_5y,
                                in_10 = return_5y_i
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
                                style={'font-size':'140%'}),
                            html.P(str(return_1y) + "%",
                            style={'font-size':'250%', 'color': color_1}),
                            html.P("The return on 1 year of the portfolio is equal to {port_10}% compared to the performance of the MSCI World Index of {in_10}%.".format(
                                port_10 = return_1y,
                                in_10 = return_1y_i
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
                    html.H6("Risk assessment", className="subtitle padded"),
                    className="row ",
                    ),
                # Image, volatility and beta
                html.Div(
                    children=[
                        html.Br([]),
                        html.Br([]),
                        html.Div(
                            children=[html.Img(src=app.get_asset_url("stationary_placeholder.jpg"))],
                            className='eight columns'
                        ),
                        html.Div(
                            children=[
                                html.Br([]),
                                html.P("Volatility (GARCH)",  style={'font-size':'140%'}),
                                html.P("-",  style={'font-size':'250%'}),
                                html.Br([]),
                                html.P("Standard deviation",  style={'font-size':'140%'}),
                                html.P("-",  style={'font-size':'250%'})
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
                        html.P("VaR (non-parametric)", style={'font-size':'140%'}),
                        html.P("-", style={'font-size':'250%'})
                        ], 
                        className='four columns',
                        style={'text-align': 'center'}),
                    
                    html.Div(children=[
                        html.Br([]),
                        html.Br([]),
                        html.Br([]),
                        html.P("Portfolio Beta", style={'font-size':'140%'}),
                        html.P("-", style={'font-size':'250%'})
                        ], 
                        className='three columns',
                        style={'text-align': 'center'}),

                    html.Div(children=[
                        html.Img(src=app.get_asset_url("histogram-placeholder.png"),
                            style={'height':'100%', 'width':'100%'})
                        ],
                        className='five columns')

                    ],
                    className="row")
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
