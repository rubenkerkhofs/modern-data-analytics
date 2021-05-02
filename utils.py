import dash_html_components as html
import dash_core_components as dcc

stocks = {'VZ': 'Verizon Communications Inc.',
          'AAPL': 'Apple Inc.',
          'MSFT': 'Microsoft Corp.',
          'AMZN': 'Amazon.com Inc.',
          'BRK-A': 'Berkshire Hathaway Inc.',
          'JPM': 'JP Morgan Chase & Co.',
          'WMT': 'Walmart Inc.',
          'MA': 'Mastercard Inc.',
          'NVDA': 'Nvidia Corp.',
          'UNH': 'United Health Group Inc.',
          'BAC': 'Bank of America Corp.',
          'DIS': 'The Walt Disney Company',
          'HEIA.AS': 'Heineken N.V.',
          'KO': 'The Coca-Cola Company',
          'ABI.BR': 'Anheuser-Busch InBev SA/NV',
          'PEP': 'PepsiCo Inc.'}

plotly_colors = ['rgb(4,67,123)', 'rgb(84,189,236)', 'rgb(215,224,234)',
    'rgb(52,140,196)', 'rgb(221, 138, 46)', 'rgb(156,196,44)', 'rgb(208,200,64)']
          
def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()])


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
            ),
            dcc.Link(
                "Reddit",
                href="/dash-financial-report/reddit",
                className="tab",
            ),
            dcc.Link(
                "Overview",
                href="/dash-financial-report/overview",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table
