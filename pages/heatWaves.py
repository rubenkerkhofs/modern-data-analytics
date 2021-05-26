from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from model import Model

from utils import Header, loadESG
from utils import loadDailyReturns, loadHeatwaves
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date

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


def getHeatwaveMetrics(heatwaves):
    heatwaves.loc[:, "year"] = heatwaves.Date.apply(
        lambda x: x.year)
    heatwaves.loc[:, "month"] = heatwaves.Date.apply(
        lambda x: x.month)
    perMonth = heatwaves.groupby("month").sum()['heatwave']
    perYear = heatwaves.groupby("year").sum()['heatwave']
    number_of_years = len(perYear)


def getSummaryStats(heatwaves):
    average = np.mean(heatwaves.avg_max_temp)
    maximum = max(heatwaves.avg_max_temp)
    maximum_year = heatwaves[heatwaves.avg_max_temp == maximum].year.values[0]
    return average, maximum, maximum_year

def getCounty(heatwaves):
    heatwaves.columns = ['notes', 'county', 'county_code',
        'avg_max_temp', 'avg_heat_index']
    maximum = max(heatwaves.avg_max_temp)
    county_largest = (heatwaves[heatwaves.avg_max_temp == maximum]
        .county.values[0])
    return county_largest, maximum

def getHeatwavesPlot(heatwaves):
    avg = np.mean(heatwaves.avg_max_temp)
    left_lim = min(heatwaves.year)
    right_lim = max(heatwaves.year)
    fig = px.bar(heatwaves, x='year', y='avg_max_temp',
                 width=425, height=200,
                 labels=dict(year="Year", avg_max_temp="# Heatwave days"))
    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='y',
                        x0=left_lim, y0=avg, x1=right_lim, y1=avg, line=dict(color="Red")
                        ),
        row=1, col=1
    )
    fig.add_annotation(x=left_lim + 3, y=avg+0.1,
            text="Average",
            font=dict( color="red"),
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
    getHeatwaveMetrics(heatwaves.reset_index())

    # Download yearly heatwave data
    hwy = pd.read_table("data/df_heat_waves_yearly.txt")
    hwy.columns = ['notes', 'year', 'avg_max_temp', 'avg_heat_index']
    avg_heatwaves, max_heatwaves, max_heatwaves_year = getSummaryStats(hwy)
    figure = getHeatwavesPlot(hwy)

    # Download county heatwave data 2020
    hwc = pd.read_table("data/df_heat_waves_2020.txt")
    county, max_county = getCounty(hwc)

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
                                    html.P(["Select the country from which you would like to use the heatwave data as well as the date range."], style={"color": "#7a7a7a"})
                                ],
                                className="three columns",
                            ),
                            # Country
                            html.Div(
                                [
                                    html.P(["Country"], style={"color": "#7a7a7a"}),
                                    dcc.Dropdown(
                                        id = 'country-selection',
                                        options=[
                                            {'label': 'United States', 'value': 'US'}
                                        ],
                                        value='US'
                                    )
                                ],
                                className="three columns",
                            ),
                            # Add date
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
                    html.Br([]),
                    html.Div(
                        [
                        html.Div(children=
                            [
                            html.P("Average heatwave days per year (averaged over counties)", style={'font-size': '140%'}),
                            html.P(round(avg_heatwaves, 2), style={'font-size': '250%'}),
                            html.Br([]),
                            html.P("Maximum number of heatwave days (averaged over counties)", style={'font-size': '140%'}),
                            html.P(round(max_heatwaves, 0), style={'font-size': '250%'}),
                            html.P("achieved in {}".format(max_heatwaves_year), style={'font-size': '140%'})

                            ],
                        className="four columns",
                        style={'text-align': 'center'}),
                        html.Div(children=[
                            html.Br([]),
                            dcc.Graph(figure=figure)

                        ],
                        className="eight columns")

                        ],
                        className = "row"
                    ),
                    html.Br([]),
                    html.Div(children=
                        [
                        html.Div(children=
                            [
                                html.P("County with largest number of heatwave days in 2020", style={'font-size': '140%'}),
                                html.P(county, style={'font-size': '250%'})
                            ],
                        className="eight columns",
                        style={'text-align': 'center'},
                        ),
                        html.Div(children=
                            [
                                html.P("Heatwave days", style={'font-size': '140%'}),
                                html.P(round(max_county, 2), style={'font-size': '250%'})
                            ],
                        className="four columns",
                        style={'text-align': 'center'})
                        ],
                        className="row"),
                    html.Br([]),
                    html.Br([]),
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



"""
html.Div(
    [
        html.P(
            "Pick the date range"
        ),
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(1980, 1, 1),
            max_date_allowed=date.today(),
            initial_visible_month=date(1980, 1, 1),
            end_date=date.today(),
            style=dict(border='0px solid #dbdbdb')
        ),
    ],
    className="six columns",
    style={"color": "#696969"},
),
"""
