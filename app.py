import dash
import dash_bootstrap_components as dbc
from dash import dcc, Output, Input
from dash import html
from visualization import all
import pandas as pd
import numpy as np
from dash import callback_context


pd.set_option("display.max_colwidth", 1000000)

# call class
v = all()
first_article = v.df.loc[v.df["impact_score_daily_return_ap1"].abs().nlargest(1).index]

# Specify stylesheets
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Define date slider items

selections_list = ['12012', '20402', '20401', '6939', '6916', '20396', '15497', '16233', '15818', '20094', '15427', '15459', '12085', '2578', '6948', '205', '20309', '20104', '3221', '5082', '3224', '6785', '1278', '3564', '532', '8971', '25', '20181', '4576', '15272', '5324', '2766', '14056', '14057', '3781', '4001', '547', '15510', '15512', '8902', '16009', '3024', '16087', '3307', '2671', '270', '1817', '1814', '2699', '13986']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame see https://plotly.com/python/px-arguments/ for more options
app.layout = \
    html.Div(className="web_app", children=[
        dcc.Store(id="selections"),
        # Top row
        dbc.Row(className="header", children=[
            # Title of the web crime_dash_app
            dbc.Col(html.H2("Financial News Analysis", id="main_header"), width=8)
        ],
                align="center"  # Vertically center the elements within this row
                ),
        # Everything else row (main web crime_dash_app content)
        dbc.Row(className="main_content", children=[
            # Display Settings Column
            dbc.Col(className="container", id="display_settings", children=[
                html.H3("Display Settings"),

                # Selecting which dataset will be used to display the data (Always show)
                html.Br(),
                html.P("Select View"),
                dcc.RadioItems(id="view_select",
                               options=["Topic Map", "Article Map", "Company Tab"],
                               value="Topic Map",
                               inline=True,
                               inputStyle={"margin-left": "20px"},
                               style={"font-size": "1vw"}),

                # Dropdown to select which company will be displayed (Show with Company Tab only)
                html.Br(),
                html.P("Select Company", id="company_select_title"),
                dcc.Dropdown(id="company_select",
                             options=["AAPL", "AMZN", "AVGO", "FB", "GOOG", "MA", "MSFT", "NVDA", "TSLA", "V"],
                             value="Select a Company",
                             multi=True
                             ),

                # Radio items to select showing bearish or bullish articles (with Article map and company tab)
                html.Br(),
                html.P("Filter by daily returns", id="bull_bear_filter"),
                dcc.RadioItems(id="bull_bear_button",
                               options=["Bullish", "Bearish", "All"],
                               inline=True,
                               inputStyle={"margin-left": "20px"},
                               style={"font-size": "1vw"},
                               value="All"
                               ),

                # Dropdown multi select to select topics (Article map and company tab)
                html.Br(),
                html.P("Select article map view", id="article_map_selector"),
                dcc.Dropdown(id="article_map_dropdown",
                             options=["Company", "Daily Returns", "Next day Returns",
                                      "Two day Returns", "Sentiment", "Topics"],
                             value="Topics",
                             multi=False, ),

                html.Br(),
                html.P("Select Topic Sentiment Weight Method", id="weight_selection"),
                dcc.RadioItems(id="weight_button",
                             options=["Total topic deviation","Sentiment topic deviation"],
                             value="Total topic deviation",),

                html.Br(),
                html.P("Select sentiment", id="sentiment_selection"),
                dcc.RadioItems(id="sentiment_button",
                             options=["All","Positive","Negative"],
                             value="All",),

                html.Br(),
                html.P("Select return range", id="return_selection"),
                dcc.RadioItems(id="return_range_button",
                             options=["Daily Returns", "Next Day Returns","Next 2 day Returns"],
                             value="Daily Returns",),

            ], width=3, style={"background-color": "#F6F6F6"}),

            # Visualization Columns (only one will show at a time)
            dbc.Col(className="container", id="visual_charts", children=[
                # pyLDAvis graph
                dbc.Row(id="lda_row", children=[
                    html.H3("Latent Dirichlet Allocation Topic Visualization"),
                    html.Iframe(src="assets/lda.html",
                                style={"height": "1067px", "width": "100%"}), ]),

                # Article topics map
                dbc.Row(id="article_map_row", children=[
                    html.H3("Article Topics Map"),
                    dcc.Graph(id="article_map",
                              figure=v.article_map(company=0, sentiment=0, main_topic=1, returns=0,
                                                   filter_company=[], filter_returns=[])),
                    # Mybe some buttons to filter stuff

                ]),
                # Company tab
                dbc.Row(id="company_row", children=[
                    dbc.Row([
                        dbc.Col(html.H3("Recommended Articles")),
                        dbc.Col(dbc.Button("Refresh", color="primary", size="sm", id="ref_bttn"))
                    ]),
                    dbc.Row([
                        dbc.Card([
                            dbc.Row([*[
                                dbc.Row([
                                    dbc.Col(html.Div("Ticker"),
                                            width=1,
                                            style={'fontSize': 18}),
                                    dbc.Col(html.Div("Impact Score"),
                                            width=2,
                                            style={'fontSize': 18}),
                                    dbc.Col(html.Div("Title"),
                                            width=3,
                                            style={'fontSize': 18}),
                                    dbc.Col(html.Div("Topics"),
                                            width=2,
                                            style={'fontSize': 18}),
                                    dbc.Col(html.Div("Positive Sentiment"),
                                            width=2,
                                            style={'fontSize': 18}),
                                    dbc.Col(html.Div("Negative Sentiment"),
                                            width=2,
                                            style={'fontSize': 18}),
                                ])
                            ]], style={"flexWrap": "nowrap"}),
                            html.Hr(),
                            html.Br(),
                            dbc.Row([
                                dbc.Col(
                                    children=[v.article_stats(i) for i in v.recommended_articles(sentiment_filter=0,
                                                                                                 company_filter=[],
                                                                                                 daily_return_filter=1,
                                                                                                 next_day_return_filter=0,
                                                                                                 two_day_return_filter=0,
                                                                                                 ap1=1, average=0)],
                                    id="recommendations_content")
                            ])
                        ], style={'overflowX': 'scroll'})
                    ], style={"display": "flex",
                              "maxHeight": "800px", "overflow": "scroll"})
                ])],),
                    #width=6, ),

            # Statistics Column
            dbc.Col(className="container", id="statistics", children=[
                html.H3("Statistics"),
                html.P(""),
                # LDA statistics
                dbc.Row(id="lda_statistics", children=[
                    html.P("LDA Statistics", style={"font-style": "italic"}),
                    html.P(""),
                    html.Br()
                    # Display list of topics with sentiment weights and names (if possible names already in lda graph)
                ]),
                # Article map statistics
                dbc.Row(id="article_statistics", children=[
                    html.P("Article Statistics", style={"font-style": "italic"}),
                ]),
                # Company Tab statistics
                dbc.Row(id="company_statistics", children=[
                    v.article_statistics(12012)
                ])],
                    width=3)
        ]),
        dbc.Row([
            dbc.Col([
            html.Footer("Intellectual property of Matic Potocnik. Developed and designed for MSIN0032: Management "
                        "Science Dissertation. Not to be distributed.")
        ], align="center")], className="h-50")
    ])


# ])


@app.callback(
    # Setting up callbacks for different parts of the web crime_dash_app
    Output("lda_row", "style"),
    Output("lda_statistics", "style"),

    Output("article_map_row", "style"),
    Output("article_statistics", "style"),
    Output("article_map_selector", "style"),
    Output("article_map_dropdown", "style"),
    Output("bull_bear_filter","style"),
    Output("bull_bear_button","style"),

    Output("company_select_title","style"),
    Output("company_select","style"),
    Output("statistics","style"),

    Output("company_row", "style"),
    Output("company_statistics", "style"),
    Output("weight_selection","style"),
    Output("weight_button","style"),
    Output("sentiment_selection","style"),
    Output("sentiment_button","style"),
    Output("return_selection","style"),
    Output("return_range_button","style"),

    Input("view_select", "value")
)
def hide(view_select):
    # Hides/Shows parts of the web crime_dash_app based off which chart is selected
    if view_select == "Topic Map":
        return {'display': 'block'}, {'display': 'block'}, \
               {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'},{'display': 'none'},{'display': 'none'}, \
               {'display': 'none'},{'display': 'none'},{'display': 'none'},\
               {'display': 'none'}, {'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},
    if view_select == "Article Map":
        return {'display': 'none'}, {'display': 'none'}, \
               {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'block'},{'display': 'block'},{'display': 'block'}, \
               {'display': 'block'},{'display': 'block'},{'display': 'block'},\
               {'display': 'none'}, {'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},{'display': 'none'},

    if view_select == "Company Tab":
        return {'display': 'none'}, {'display': 'none'}, \
               {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'},{'display': 'none'},{'display': 'none'}, \
               {'display': 'block'},{'display': 'block'},{'display': 'block'},\
               {'display': 'block'}, {'display': 'block'},{'display': 'block'},{'display': 'block'},{'display': 'block'},{'display': 'block'},{'display': 'block'},{'display': 'block'},


@app.callback(
    Output("article_map", "figure"),
    Input("company_select", "value"),
    Input("bull_bear_button", "value"),
    Input("article_map_dropdown", "value")
)
def update_data(company_select, bull_bear_button, article_map_dropdown):
    # Updates the data used for the histogram based on the slider date range
    if article_map_dropdown == "Topics":
        fig = v.article_map(company=0, sentiment=0, main_topic=1, returns=0,
                            filter_company=company_select, filter_returns=bull_bear_button)
    elif article_map_dropdown == "Company":
        fig = v.article_map(company=1, sentiment=0, main_topic=0, returns=0,
                            filter_company=company_select, filter_returns=bull_bear_button)
    elif article_map_dropdown == "Daily Returns":
        fig = v.article_map(company=0, sentiment=0, main_topic=0, returns="daily",
                            filter_company=company_select, filter_returns=bull_bear_button)
    elif article_map_dropdown == "Next day Returns":
        fig = v.article_map(company=0, sentiment=0, main_topic=0, returns="next_day",
                            filter_company=company_select, filter_returns=bull_bear_button)
    elif article_map_dropdown == "Two day Returns":
        fig = v.article_map(company=0, sentiment=0, main_topic=0, returns="2_days",
                            filter_company=company_select, filter_returns=bull_bear_button)
    elif article_map_dropdown == "Sentiment":
        fig = v.article_map(company=0, sentiment=1, main_topic=0, returns=0,
                            filter_company=company_select, filter_returns=bull_bear_button)
    return fig

@app.callback(
Output("recommendations_content", "children"),
Input("company_select", "value"),
Input("sentiment_button","value"),
Input("return_range_button","value"),
Input("weight_button","value")
)
def update_recomendations(company_select, sentiment_button,return_range_button,weight_button):
    #print("company select = ", company_select)
    #print("sentiment button = ", sentiment_button)
    #print("return range button = ",return_range_button)
    #print("weight button = ",weight_button)
    #print(" ")
    companies = company_select
    if sentiment_button=="All":
        sentiment_f = 0
    elif sentiment_button=="Positive":
        sentiment_f = "positive"
    elif sentiment_button == "Negative":
        sentiment_f = "negative"
    if weight_button == "Total topic deviation":
        ap_w = 1
        aver_w = 0
    else:
        ap_w = 0
        aver_w = 1
    if return_range_button == "Daily Returns":
        dr = 1
        nr =0
        r2 = 0
    elif return_range_button == "Next Day Returns":
        dr=0
        nr=1
        r2=0
    elif return_range_button == "Next 2 day Returns":
        dr=0
        nr=0
        r2 = 1

    children = [v.article_stats(i) for i in v.recommended_articles(sentiment_filter=sentiment_f,
                                                                   company_filter=companies,
                                                                   daily_return_filter=dr,
                                                                   next_day_return_filter=nr,
                                                                   two_day_return_filter=r2,
                                                                   ap1=ap_w, average=aver_w)]
    return children

@app.callback(
    Output("selections", "data"),
    [Input("company_select", "value")],
    [Input("sentiment_button", "value")],
    [Input("return_range_button", "value")],
    [Input("weight_button", "value")]
)
def get_buttons(company_select, sentiment_button,return_range_button,weight_button):
    companies = company_select
    if sentiment_button == "All":
        sentiment_f = 0
    elif sentiment_button == "Positive":
        sentiment_f = "positive"
    elif sentiment_button == "Negative":
        sentiment_f = "negative"
    if weight_button == "Total topic deviation":
        ap_w = 1
        aver_w = 0
    else:
        ap_w = 0
        aver_w = 1
    if return_range_button == "Daily Returns":
        dr = 1
        nr = 0
        r2 = 0
    elif return_range_button == "Next Day Returns":
        dr = 0
        nr = 1
        r2 = 0
    elif return_range_button == "Next 2 day Returns":
        dr = 0
        nr = 0
        r2 = 1

    button_list= v.recommended_articles(sentiment_filter=sentiment_f,
                                                                   company_filter=companies,
                                                                   daily_return_filter=dr,
                                                                   next_day_return_filter=nr,
                                                                   two_day_return_filter=r2,
                                                                   ap1=ap_w, average=aver_w)
    #print(np.array(button_list)[:,0])
    selections = np.array(button_list)[:,0].tolist()
    global selections_list
    selections_list = selections
    return selections_list

@app.callback(
    Output("company_statistics","children"),
    [Input(f"article_bttn_{i}", 'n_clicks') for i in selections_list],
    Input("ref_bttn","n_clicks")
)
def func(*args):
    #print(selections_list)
    trigger = callback_context.triggered[0]
    print(trigger["prop_id"].split(".")[0][13:])
    if trigger["prop_id"].split(".")[0]!="ref_bttn":
        a = float(trigger["prop_id"].split(".")[0][13:])
        return v.article_statistics(a)


if __name__ == '__main__':
    app.run_server(debug=True)
