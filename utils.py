# Dash packages
import dash_html_components as html
import dash_core_components as dcc

# Other required packages
import pandas as pd
import numpy as np

stocks: dict = {
    'VZ': 'Verizon Communications Inc.',
          'AAPL': 'Apple Inc.',
          'ABI.BR': 'Anheuser-Busch InBev SA/NV',
          'AMZN': 'Amazon.com Inc.',
          'BAC': 'Bank of America Corp.',
          'BRK-A': 'Berkshire Hathaway Inc.',
          'DIS': 'The Walt Disney Company',
          'HEIA.AS': 'Heineken N.V.',
          'JPM': 'JP Morgan Chase & Co.',
          'KO': 'The Coca-Cola Company',
          'MA': 'Mastercard Inc.',
          'MSFT': 'Microsoft Corp.',
          'NVDA': 'Nvidia Corp.',
          'PEP': 'PepsiCo Inc.',
          'UNH': 'United Health Group Inc.',
          'WMT': 'Walmart Inc.'}

months: list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

plotly_colors: list = ['rgb(4,67,123)', 'rgb(84,189,236)', 'rgb(215,224,234)',
                       'rgb(52,140,196)', 'rgb(221, 138, 46)', 'rgb(156,196,44)', 'rgb(208,200,64)']


def createEmptyDatasets():
    # Creating an empty portfolio, diversification and returns dataframe
    # TODO: allow uploading a CSV file with tickers and number of shares
    df_portfolio = pd.DataFrame(
        columns=['Ticker', 'Name', 'Number of Shares', 'Price', 'Value (USD)', 'Industry'])
    df_portfolio.to_csv('data/df_portfolio.csv', index=False)

    df_diversification = pd.DataFrame(
        columns=['Industry', 'Total Value', 'Relative Value'])
    df_diversification.to_csv(
        'data/df_sector_diversification.csv', index=False)

    df_returns = pd.DataFrame(columns=['Date', 'Return'])
    df_returns.to_csv('data/df_portfolio_returns.csv', index=False)


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("ku_leuven_logo.png"),
                        className="logo",
                    )
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Div(
                        [html.H5("Modern Data Analytics - Chad")],
                        className="seven columns main-title",
                    )
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Our approach",
                href="/dash-financial-report/ourApproach",
                className="tab first",
            ),
            dcc.Link(
                "Portfolio",
                href="/dash-financial-report/portfolio",
                className="tab",
            ),
            dcc.Link(
                "Portfolio performance",
                href="/dash-financial-report/portfolioPerformance",
                className="tab",
            ),
            dcc.Link(
                "Heat Waves", href="/dash-financial-report/heatWaves", className="tab"
            )
        ],
        className="row all-tabs",
    )
    return menu


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


def loadColors(return_1y: float, return_5y: float, return_10y: float,
               return_1y_i: float, return_5y_i: float,
               return_10y_i: float) -> tuple:
    color_10, color_5, color_1 = 'black', 'black', 'black'
    if return_1y != "-":  # if stocks in portfolio
        color_10, color_5, color_1 = 'red', 'red', 'red'
        if return_10y > return_10y_i:
            color_10 = 'green'
        if return_5y > return_5y_i:
            color_5 = 'green'
        if return_1y > return_1y_i:
            color_1 = 'green'
    return color_10, color_5, color_1


def loadDailyReturns() -> pd.DataFrame:
    # Get returns
    portfolio_returns = pd.read_csv('data/df_portfolio_returns.csv')
    # Switched to daily returns
    daily_returns = portfolio_returns.Return.pct_change().dropna()
    portfolio_returns = portfolio_returns.iloc[1:]
    portfolio_returns.loc[:, 'daily_returns'] = daily_returns
    return portfolio_returns


def loadHeatwaves() -> pd.Series:
    temperatures = loadTemperatures().dropna().tail(365*11)
    temperatures.DateMax = temperatures.DateMax
    temps = temperatures.DateMax
    heatwave = []
    h = False
    min_temp = 32.2
    for i in range(len(temps) - 2):
        temp_tod = temps[i]
        temp_tom = temps[i+1]
        temp_ove = temps[i+1]
        if h and temp_tod > min_temp:
            heatwave.append(1)
        elif temp_tod > min_temp and temp_tom > min_temp and temp_ove > min_temp:
            heatwave.append(1)
            h = True
        else:
            heatwave.append(0)
            h = False
    heatwave.append(0)
    heatwave.append(0)
    temperatures.loc[:, 'heatwave'] = heatwave
    return temperatures['heatwave']


def loadMetrics() -> tuple:
    # Load the portfolio returns
    portfolio_returns = pd.read_csv('data/df_portfolio_returns.csv')
    df_portfolio = pd.read_csv("data/df_portfolio.csv")
    beta, VaR, standev = "-", "-", "-"
    if portfolio_returns.shape[0] > 0:  # if stocks in portfolio
        # Get the beta
        f = open('data/beta.txt', 'r')
        beta = str(round(float(f.readline()), 4))
        f.close()

        # Get the daily returns and portfolio value
        daily_returns = portfolio_returns.Return.pct_change().dropna()
        total_value = sum(df_portfolio['Value (USD)'])

        # Calculate non-parametric VaR and standard deviation
        VaR = "$" + \
            "{:,}".format(
                round(-np.percentile(daily_returns, 1) * total_value, 2))
        standev = str(round(np.std(daily_returns) * 100, 2)) + "%"
    return beta, VaR, standev


def loadReturns(portfolio_returns: pd.Series, index_returns: pd.Series) -> tuple:
    assert "Return" in portfolio_returns.columns,\
        "Dataframe should have a column named: Return"

    assert "Close" in index_returns.columns,\
        "Dataframe should have a column named: Close"
    # Calculate key metrics
    return_10y, return_10y_i = "-", "-"
    return_5y, return_5y_i = "-", "-"
    return_1y, return_1y_i = "-", "-"
    if portfolio_returns.shape[0] > 0:  # if stocks in portfolio
        # Get start values
        start_investment = portfolio_returns.Return[0]
        index_start = index_returns['Close'][0]
        ratio = start_investment/index_start

        # Modify index returns to match initial investment as portfolio value 10 years ago
        index_returns.Close = index_returns['Close']*ratio

        # Get the number of days
        days = portfolio_returns.shape[0]
        days_i = index_returns.shape[0]

        # Calculate key numbers
        now = portfolio_returns.Return[days-1]
        ago_5y = portfolio_returns.Return[days-5*365-1]
        ago_1y = portfolio_returns.Return[days-366]
        index_5y = index_returns['Close'][days_i-5*365-1]
        index_1y = index_returns['Close'][days_i-365]
        index_now = index_returns['Close'][days_i-1]
        return_10y = round((now - start_investment)*100/start_investment, 2)
        return_5y = round((now - ago_5y)*100/ago_5y, 2)
        return_1y = round((now - ago_1y)*100/ago_1y, 2)
        return_10y_i = round((index_now - start_investment)
                             * 100/start_investment, 2)
        return_5y_i = round((index_now - index_5y)*100/index_5y, 2)
        return_1y_i = round((index_now - index_1y)*100/index_1y, 2)

    return return_1y, return_5y, return_10y, return_1y_i, return_5y_i, return_10y_i


def loadTemperatures() -> pd.DataFrame:
    df = pd.read_pickle("data/dfmaxcel.pkl")
    df.DateMax = df.DateMax - (45-32.2)  # Calibrate temperatures
    return df


def make_dash_table(df: pd.DataFrame):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
