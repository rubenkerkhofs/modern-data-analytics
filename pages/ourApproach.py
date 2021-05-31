import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from utils import Header, make_dash_table

import pandas as pd

def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [   
                    dcc.Loading(
                        id="loading-1",
                        children=[html.Div([html.Div(id="loading-output-1")])],
                        type="default",
                    ),
                    html.Br([]),
                    html.Br([]),
                    # Row 3
                    # Title box
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Heat wave impact"),
                                    html.Br([]),
                                    html.P(
                                        "In the 1960s, Major cities experienced, on average, about two heat waves per year. In the 2010s, that number rose to more than six heat waves per year. These heat waves are also lasting longer, on average 47 days longer than in 1960. Even under different climate models and emission scenarios, results indicate that extreme heat events worsen. Heatwaves, or heat and hot weather that can last for several days, can have a significant impact on society, including a rise in heat-related deaths. More than 70 000 people died during the 2003 heatwave in Europe. Workers who are exposed to extreme heat or work in hot environments may be at risk of heat stress. Exposure to extreme heat can result in occupational illnesses and injuries. Heat stress can result in heat stroke, heat exhaustion, heat cramps, or heat rashes. Humidity is an important factor in heat index assessment. When the humidity is high, water does not evaporate as easily and so it becomes difficult for the body to cool off through sweating.",
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Our approach subtitle
                    html.Div(
                        [
                            html.Div(
                                [html.H6(["Our approach"],
                                         className="subtitle padded")],
                                className="twelve columns",
                            )
                        ],
                        className="rows",
                    ),
                    html.P("This dashboard was created for investors who want to assess the short-term impact of heat waves on their portfolio. It allows these investors to specify their portfolio, after which the application applies pre-made models to the portfolio data and provides the user with contextual information related to heat waves."),
                    html.Br([]),
                    html.P("Although a company's fundamentals are not affected by heat waves in the short term, we believe that a single heat wave can have an impact on a portfolio in the short term. The reasoning goes like this: heat waves are known to have a negative impact on the mental health of people, including investors, and this negative state of mind could in turn affect the stock market in the short term. "),
                    html.Br([]),
                    html.P("This general idea is illustrated below: "),
                    html.Div(html.Img(src=app.get_asset_url('reddit_results.PNG'),
                                style={"width": "80%"}),
                            style={'textAlign': 'center'}),
                    html.P("During the second heatwave period in 2019, both the invester sentiment and the value of the S&P 500 went down. This effect can of course be random, however, this should be investigated. The dashboard uses a collection of models to determine whether the portfolio specified by the user is exposed to this kind of risk."),
                    html.Br([]),
                    html.Br([]),
                    html.Div(html.A('Click here to move to the next page and pick your portfolio', href="/dash-financial-report/portfolio", id="next-page"),
                        style={"textAlign": "right", 'font-size': '150%', "text-decoration": "underline"})
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
