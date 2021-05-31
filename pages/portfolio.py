# Dash packages
import dash_core_components as dcc
import dash_html_components as html

# Utils functions and variables
from utils import Header

# Other required packages
import pandas as pd

df_portfolio = pd.read_csv("data/df_portfolio.csv")
df_sector_diversification = pd.read_csv("data/df_sector_diversification.csv")


def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 3
            html.Div(
                [   dcc.Loading(
                        id="loading-1",
                        children=[html.Div([html.Div(id="loading-output-1")])],
                        type="default",
                    ),
                    html.Br([]),
                    html.Br([]),
                    # First title
                    html.Div(
                        [
                            html.Div(
                                [html.H6(["Add stocks to your portfolio"],
                                         className="subtitle padded")],
                                className="twelve columns",
                            )
                        ],
                        className="rows",
                    ),
                    # Adding stocks application
                    html.Div(
                        [
                            # Information about how to add stock
                            html.Div(
                                [
                                    html.P(["To add a stock to your portfolio, please indicate the name of the stock as well as the amount of shares."], style={
                                           "color": "#7a7a7a"})
                                ],
                                className="three columns",
                            ),
                            # Name of the stock
                            html.Div(
                                [
                                    html.P(["Indicate the name of the stock"], style={
                                           "color": "#7a7a7a"}),
                                    dcc.Dropdown(
                                        id='stocks-selection',
                                        options=[
                                            {'label': 'Apple', 'value': 'AAPL'},
                                            {'label': 'AB Inbev', 'value': 'ABI.BR'},
                                            {'label': 'Amazon', 'value': 'AMZN'},
                                            {'label': 'Bank of America', 'value': 'BAC'},
                                            {'label': 'Walt Disney Company','value': 'DIS'},
                                            {'label': 'Heineken', 'value': 'HEIA.AS'},
                                            {'label': 'JP Morgan Chase', 'value': 'JPM'},
                                            {'label': 'Coca Cola', 'value': 'KO'},
                                            {'label': 'Mastercard', 'value': 'MA'},
                                            {'label': 'Microsoft', 'value': 'MSFT'},
                                            {'label': 'Nvidia Corp', 'value': 'NVDA'},
                                            {'label': 'PepsiCo', 'value': 'PEP'},
                                            {'label': 'United Health Group', 'value': 'UNH'},
                                            {'label': 'Verizon', 'value': 'VZ'},
                                            {'label': 'Walmart', 'value': 'WMT'}     
                                        ],
                                        value='AAPL'
                                    )
                                ],
                                className="three columns",
                            ),
                            # The number of shares
                            html.Div(
                                [
                                    html.P(
                                        "Indicate the number of shares"
                                    ),
                                    dcc.Input(
                                        id='number-of-shares',
                                        type='text',
                                        placeholder='1.2345'
                                    )
                                ],
                                className="three columns",
                                style={"color": "#696969"},
                            ),
                            # Empty column
                            html.Div(
                                [html.P("")],
                                className="one column",
                                style={"color": "#696969"},
                            ),
                            # Add button
                            html.Div(
                                [
                                    html.P(
                                        "Add stock to portfolio"
                                    ),
                                    html.Button('Add',
                                                id='Add-stock-button',
                                                n_clicks=0
                                                )
                                ],
                                className="two columns",
                                style={"color": "#696969"},
                            ),
                        ],
                        className="row ",
                    ),
                    # Warning message if done something wrong
                    html.Div(
                        [
                            html.P(
                                '',
                                className="twelve columns",
                                id='warning-add-stock',
                                style={'color': 'red'}
                            )
                        ],
                        className="rows",
                    ),
                    # Portfolio overview
                    html.Br([]),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Your portfolio"],
                                        className="subtitle padded",
                                    ),
                                    html.Table(
                                        '',
                                        className="tiny-header",
                                        id='table-portfolio-overview'
                                    ),
                                ],
                                className=" twelve columns",
                                id='Your-portfolio'
                            )
                        ],
                        className="row ",
                    ),
                    # Text under your portfolio
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P(
                                        "",
                                        id="portfolio-description"
                                    )
                                ],
                                className=" twelve columns",
                                id='Your-portfolio'
                            )
                        ],
                        className="row ",
                    ),

                    # Sector diversification
                    html.Div(
                        [
                            html.Div(
                                [html.Br([]),
                                    html.H6(
                                        ["Industry diversification"],
                                        className="subtitle padded",
                                ),
                                    html.Table(
                                        '',
                                        className="tiny-header",
                                        id='table-sector-diversification'
                                ),
                                ],
                                className=" six columns",
                            ),
                            html.Div(
                                children=[],
                                className=" six columns",
                                id='fig-sector-diversification'
                            )
                        ],
                        className="row ",
                    ),
                    html.Div(
                        [html.P('', id='filler')],  # used to update returns
                        className="row ",
                    ),
                    html.Div(html.A('Once you have your portfolio, explore its performance by clicking here', href="/dash-financial-report/portfolioPerformance", id="next-page"),
                        style={"textAlign": "right", 'font-size': '150%', "text-decoration": "underline"})
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
