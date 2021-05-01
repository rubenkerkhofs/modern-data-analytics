# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output, State
from pages import (
    ourApproach,
    portfolio,
    portfolioPerformance,
    heatWaves,
    reddit,
    overview,
)
from utils import Header, make_dash_table, stocks, plotly_colors
import pandas as pd
import numpy as np
import yfinance as yf

# Creating an empty portfolio, diversification and returns dataframe
# TODO: allow uploading a CSV file with tickers and number of shares
df_portfolio = pd.DataFrame(columns=['Ticker', 'Name', 'Number of Shares', 'Price', 'Value (USD)', 'Industry'])
df_portfolio.to_csv('data/df_portfolio.csv', index=False)

df_diversification = pd.DataFrame(columns=['Industry', 'Total Value', 'Relative Value'])
df_diversification.to_csv('data/df_sector_diversification.csv', index=False)

df_returns = pd.DataFrame(columns=['Date', 'Return'])
df_returns.to_csv('data/df_portfolio_returns.csv', index=False)

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Update page when the menu is used to navigate
@app.callback(
    Output("page-content", "children"), 
    Input("url", "pathname"))
def display_page(
    pathname: str):
    if pathname == "/dash-financial-report/portfolio":
        return portfolio.create_layout(app)
    elif pathname == "/dash-financial-report/portfolioPerformance":
        return portfolioPerformance.create_layout(app)
    elif pathname == "/dash-financial-report/heatWaves":
        return heatWaves.create_layout(app)
    elif pathname == "/dash-financial-report/reddit":
        return reddit.create_layout(app)
    elif pathname == "/dash-financial-report/overview":
        return overview.create_layout(app)
    else:
        return ourApproach.create_layout(app)

##########################
# Portfolio page callbacks
##########################
@app.callback(
    Output('table-portfolio-overview', "children"),
    Input('Add-stock-button', 'n_clicks'),
    State('stocks-selection', 'value'),
    State('number-of-shares', 'value')
    )
def update_portfolio(
        n_clicks: int,
        stock_ticker: str,
        number: str):
    # Load the portfolio file because it contains all positions up to now
    df_portfolio = pd.read_csv('data/df_portfolio.csv')
    # If the button has been clicked at least once (needed because dash
    # executes all callbacks during initial load)
    if n_clicks != 0:
        # Get stock information from Yahoo finance
        stock = yf.Ticker(stock_ticker)
        price = (stock.info['bid'] + stock.info['ask'])/2
        if price < 0.001: # When stock market is closed, no bid or ask available
                          # Yahoo then returns 0
            price = stock.info['previousClose']
        # Number input is a string and needs to be converted
        # checkInputs callback provides a warning to the user when the 
        # conversion fails and displays a warning message
        number = float(number)
        value = round(number*price, 2)
        industry = stock.info['industry']

        # Add new information to the portfolio
        df_portfolio = df_portfolio.append(
                {'Ticker': stock_ticker,
                'Name': stocks[stock_ticker],
                'Number of Shares': round(number, 2),
                'Price': round(price, 2),
                'Value (USD)': value,
                'Industry': industry},
            ignore_index=True
            )
        
        # When a person adds a position of a stock that is already in the
        # portfolio, the position should be added to that stock. This piece
        # of code ensures that every ticker is unique in the portfolio.
        df_portfolio_per_comp = df_portfolio.groupby('Ticker', as_index=False).agg('sum')
        df_portfolio = pd.merge(df_portfolio_per_comp.drop('Price', axis=1), 
            df_portfolio[['Ticker', 'Name', "Industry", "Price"]].drop_duplicates("Name"), 
            how='inner', on='Ticker')
        df_portfolio = df_portfolio[[
            'Ticker', 'Name', 'Number of Shares', 'Price', 'Value (USD)', 'Industry'
        ]]
        # Rounding errors because of float can happen e.g. 17.0000000003
        df_portfolio['Number of Shares'] = df_portfolio['Number of Shares'].apply(lambda x: round(x, 2))
        df_portfolio['Value (USD)'] = df_portfolio['Value (USD)'].apply(lambda x: round(x, 2))
        
        # Save portfolio so it can be used in other parts of the application
        df_portfolio.to_csv('data/df_portfolio.csv', index=False)
    
    return dash_table.DataTable(
                id='portfolio',
                columns=[{"name": i, "id": i} for i in df_portfolio.columns],
                data=df_portfolio.to_dict('records'),
                style_cell = {'fontSize': 13, 'font-family':'sans-serif'},
                style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'textAlign': 'center'
                        } for c in ['Date', 'Region']
                    ],

                style_as_list_view=True,
            )


@app.callback(
    Output('portfolio-description', 'children'),
    Input('table-portfolio-overview', 'children')
    )
def update_portfolio_text(
        table # Input not needed but otherwise syntax error
    ):
    # Loading the portfolio and extracting information from it
    df_portfolio = pd.read_csv("data/df_portfolio.csv")
    number_of_companies = df_portfolio.shape[0]
    total_value = sum(df_portfolio['Value (USD)'])
    largest_industry = (df_portfolio
        .groupby('Industry', as_index=False)
        .agg('sum')
        .sort_values('Value (USD)', ascending=False)
        ['Industry'].values[0])
    largest_position = (df_portfolio
        .sort_values('Value (USD)', ascending=False)
        ['Name'].values[0])
    largest_position_ticker = (df_portfolio
        .sort_values('Value (USD)', ascending=False)
        ['Ticker'].values[0])
    largest_position_value = (df_portfolio
        .sort_values('Value (USD)', ascending=False)
        ['Value (USD)'].values[0])
    if number_of_companies == 1:
        st = "stock"
    else:
        st = "stocks"
        # Return a text tailored to the portfolio
    return "The portfolio consists of {n} {st} and has a total value of {usd} US dollars. The majority of the funds is invested in the {ind} industry. The largest position is the one in the {lc} ({lct}) stock which has a value of {lcv} US dollars.".format(
        n = number_of_companies,
        st = st,
        usd = round(total_value, 2),
        ind = largest_industry,
        lc = largest_position,
        lct = largest_position_ticker,
        lcv = largest_position_value
        )


@app.callback(
    Output('table-sector-diversification', "children"),
    Input('table-portfolio-overview', 'children'),
)
def update_sector_diversification(
        table # Input not needed but otherwise syntax error
    ):
    # Load portfolio to calculate diversification
    df_portfolio = pd.read_csv('data/df_portfolio.csv')
    # Diversification based on total value
    sd = df_portfolio.groupby('Industry', as_index=False).agg('sum')[['Industry', 'Value (USD)']]
    sd.loc[:, 'Relative share'] = sd['Value (USD)'].apply(
        lambda x: round(x/sum(sd['Value (USD)']), 4)) # Calculate relative share
    # Give good names to columns
    sd.columns = ['Industry', 'Total Value', 'Relative Value']
    sd['Total Value'] = sd['Total Value'].apply(lambda x: round(x, 2))
    
    # Save results so can be used in other parts e.g. figure
    sd.to_csv('data/df_sector_diversification.csv', index=False)
    return dash_table.DataTable(
                id='sector-diversification',
                columns=[{"name": i, "id": i} for i in sd.columns],
                data=sd.to_dict('records'),
                style_cell = {'fontSize': 13, 'font-family':'sans-serif'},
                style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'textAlign': 'center'
                        } for c in ['Date', 'Region']
                    ],
                style_as_list_view=True,
            )


@app.callback(
    Output('fig-sector-diversification', 'children'),
    Input('table-sector-diversification', "children")
)
def update_sector_figure(
        table
    ):
    sd = pd.read_csv('data/df_sector_diversification.csv')
    sd.loc[:, 'empty'] = "nothing"
    # Creating the figure
    fig = px.bar(sd, x="empty", y="Total Value", color="Industry", 
        title="Industry diversification", hover_data={'empty': False},
        color_discrete_sequence=plotly_colors)
    fig.update_layout(showlegend=False)
    fig.update_yaxes(tickprefix="$", showgrid=True)
    fig.update_layout(xaxis_visible=False, xaxis_showticklabels=False)
    fig.update_layout(
        font_family="sans-serif",
        font_color="black",
        title_x=0.5,
        title_y = 0.82,
        paper_bgcolor='rgba(0,0,0,0)', # No background
        plot_bgcolor='rgba(0,0,0,0)', # No background
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif"
        )
    )
    return dcc.Graph(figure=fig)


@app.callback(
    Output('warning-add-stock', "children"),
    Input('Add-stock-button', 'n_clicks'),
    State('number-of-shares', 'value')
)
def checkInputs(
    n_clicks: int,
    number: str
    ):
    try:
        if n_clicks != 0:
            number = float(number)
        return ''
    except:
        return 'FAILED: Please provide a valid number of shares like by example 1.2345.'

############################
# Performance page callbacks
############################
@app.callback(
    Output('filler', 'children'),
    Input('table-portfolio-overview', "children"),
    )
def getPortfolioReturns(
    table # not needed but otherwise syntax error
    ):
    companies = pd.read_csv('data/df_portfolio.csv')
    portfolio_value = None
    total_portfolio_value = sum(companies['Value (USD)'])
    for index, row in companies.iterrows():
        company = row['Ticker']
        returns = yf.Ticker(company).history(period='10y')['Close']
        if len(returns) > 2517:
            returns = returns[-2517:]
        returns = np.array(returns)*row['Number of Shares']
        if portfolio_value is None:
            portfolio_value = returns
        else:
            portfolio_value = returns + portfolio_value
    dates = yf.Ticker('AAPL').history(period='10y').index
    returns = pd.DataFrame(portfolio_value, columns=['Return'])
    returns.index = dates
    returns.to_csv("data/df_portfolio_returns.csv")
    return ''





if __name__ == "__main__":
    app.run_server(debug=True)
