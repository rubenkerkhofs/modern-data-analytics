import dash_html_components as html
from utils import Header, make_dash_table
import pandas as pd


def create_layout(app):
    return html.Div(
        [
            Header(app),
            # page 5
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Distributions"], className="subtitle padded"
                                    ),
                                    html.P(
                                        [
                                            "Distributions for this fund are scheduled quaterly"
                                        ],
                                        style={"color": "#7a7a7a"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Br([]),
                                    html.H6(
                                        ["Dividend and capital gains distributions"],
                                        className="subtitle tiny-header padded",
                                    ),
                                    html.Div(
                                        [
                                            html.Table(
                                                make_dash_table(df_dividend),
                                                className="tiny-header",
                                            )
                                        ],
                                        style={"overflow-x": "auto"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Realized/unrealized gains as of 01/31/2018"],
                                        className="subtitle tiny-header padded",
                                    )
                                ],
                                className=" twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [html.Table(make_dash_table(df_realized))],
                                className="six columns",
                            ),
                            html.Div(
                                [html.Table(make_dash_table(df_unrealized))],
                                className="six columns",
                            ),
                        ],
                        className="row ",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
