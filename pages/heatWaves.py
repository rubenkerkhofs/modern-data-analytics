import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from utils import Header, make_dash_table, loadESG, loadDailyReturns
import pandas as pd


def create_layout(app):
    esg_env, esg_soc, esg_gov = loadESG()
    daily_returns = loadDailyReturns()

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
                        )

                    ],
                        className="row")



                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
