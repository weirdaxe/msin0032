from pathlib import Path

import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import statistics
import numpy as np
import dash_bootstrap_components as dbc
from dash import html


class all:
    def __init__(self):
        # Core data
        self.df = pd.DataFrame()
        self.return_category = {
            0: "super_bullish",
            1: "bullish",
            2: "weak_bullish",
            3: "neutral",
            4: "weak_bearish",
            5: "bearish",
            6: "super_bearish"
        }
        self.ticker_list = ["AAPL", "AMZN", "AVGO", "FB", "GOOG", "MA", "MSFT", "NVDA", "TSLA", "V"]
        self.return_labels = ["super_bullish", "bullish", "weak_bullish",
                              "neutral", "weak_bearish", "bearish", "super_bearish"]
        self.article_stat_list = ["Ticker", "Impact Score", "Title", "Topics", "Positive Sentiment",
                                  "Negative Sentiment"]
        self.top_list = ['top_0', 'top_1', 'top_10', 'top_11', 'top_12', 'top_13', 'top_14',
                         'top_15', 'top_16', 'top_17', 'top_18', 'top_19', 'top_2', 'top_20',
                         'top_21', 'top_22', 'top_23', 'top_24', 'top_25', 'top_26', 'top_27',
                         'top_28', 'top_29', 'top_3', 'top_4', 'top_5', 'top_6', 'top_7',
                         'top_8', 'top_9']
        self.top_sent_list = ['top_0_average_adjusted',
                              'top_1_average_adjusted',
                              'top_10_average_adjusted',
                              'top_11_average_adjusted',
                              'top_12_average_adjusted',
                              'top_13_average_adjusted',
                              'top_14_average_adjusted',
                              'top_15_average_adjusted',
                              'top_16_average_adjusted',
                              'top_17_average_adjusted',
                              'top_18_average_adjusted',
                              'top_19_average_adjusted',
                              'top_2_average_adjusted',
                              'top_20_average_adjusted',
                              'top_21_average_adjusted',
                              'top_22_average_adjusted',
                              'top_23_average_adjusted',
                              'top_24_average_adjusted',
                              'top_25_average_adjusted',
                              'top_26_average_adjusted',
                              'top_27_average_adjusted',
                              'top_28_average_adjusted',
                              'top_29_average_adjusted',
                              'top_3_average_adjusted',
                              'top_4_average_adjusted',
                              'top_5_average_adjusted',
                              'top_6_average_adjusted',
                              'top_7_average_adjusted',
                              'top_8_average_adjusted',
                              'top_9_average_adjusted']
        # Starting Functions
        self.get_data()

        # Functions
        # self.boroughs()
        # self.crimes()
        # self.dates()

    def get_data(self):
        # Import the main data (crime_data), supporting datasets (population, daytime_population), and geojson
        datafile = Path(__file__).parent.joinpath("data")
        self.df = pd.read_csv(datafile / "df_final.csv")
        # self.df = self.df.drop([["Unnamed: 0", "level_0", "index",
        #                         "Unnamed: 0.1", "date_time", "date_str", "x_coord"]], axis=1)

    def article_map(self, company=0, sentiment=0, main_topic=1, returns=0,
                    filter_company=[], filter_returns=[]):
        if filter_company == "Select a Company" or filter_company == []:
            ticker_list = self.ticker_list
        else:
            ticker_list = filter_company
        if filter_returns == "All" or filter_returns == []:
            return_filter = self.return_labels
        elif filter_returns == "Bullish":
            return_filter = ["super_bullish", "bullish", "weak_bullish"]
        elif filter_returns == "Bearish":
            return_filter = ["weak_bearish", "bearish", "super_bearish"]
        df = self.df
        df = df[df["stock"].isin(ticker_list) &
                df["daily_return_categorical_labeled"].isin(return_filter)]

        if sentiment == 1:
            sentiment_colors = ['#008000', '#00ff00', '#b3ffb3',
                                '#bfbfbf',
                                '#ff9999', '#ff3333', '#990000', ]
            fig = px.scatter(df,
                             y="y_cord",
                             x="x_cord", color="adjusted_sentiment_categorical",
                             opacity=0.6,
                             color_discrete_sequence=sentiment_colors,
                             title="Article topic space with sentiment",
                             labels={"adjusted_sentiment_categorical": "Article Sentiment"},
                             category_orders={"adjusted_sentiment_categorical": [
                                 "super positive", "positive", "weakly positive",
                                 "neutral",
                                 "weakly negative", "negative", "super negative"]},
                             hover_data=["stock", "main_top",
                                         "adjusted_sentiment_categorical",
                                         "daily_return_categorical_labeled",
                                         "next_day_return_categorical_labeled",
                                         "two_day_return_categorical_labeled"]
                             )
            fig.update_yaxes(title='y', visible=False, showticklabels=False)
            fig.update_xaxes(title='Topic Intensity', visible=True, showticklabels=False)

            return fig
        elif company == 1:
            fig = px.scatter(df,
                             y="y_cord",
                             x="x_cord", color="stock",
                             opacity=0.6,
                             title="Article topic space by companies",
                             labels={"stock": "Tickers"},
                             hover_data=["stock", "main_top",
                                         "adjusted_sentiment_categorical",
                                         "daily_return_categorical_labeled",
                                         "next_day_return_categorical_labeled",
                                         "two_day_return_categorical_labeled"]
                             )
            fig.update_yaxes(title='y', visible=False, showticklabels=False)
            fig.update_xaxes(title='Topic Intensity', visible=True, showticklabels=False)
            return fig
        elif main_topic == 1:
            fig = px.scatter(df,
                             y="y_cord",
                             x="x_cord", color="main_top",
                             opacity=0.6,
                             title="Article topic space by topics",
                             labels={"main_top": "Topic"},
                             hover_data=["stock", "main_top",
                                         "adjusted_sentiment_categorical",
                                         "daily_return_categorical_labeled",
                                         "next_day_return_categorical_labeled",
                                         "two_day_return_categorical_labeled"]
                             )
            fig.update_yaxes(title='y', visible=False, showticklabels=False)
            fig.update_xaxes(title='Topic Intensity', visible=True, showticklabels=False)
            return fig
        elif returns == 'daily':
            sentiment_colors = ['#008000', '#00ff00', '#b3ffb3',
                                '#bfbfbf',
                                '#ff9999', '#ff3333', '#990000', ]
            fig = px.scatter(df,
                             y="y_cord",
                             x="x_cord", color="daily_return_categorical_labeled",
                             opacity=0.6,
                             title="Article topic space by daily return",
                             color_discrete_sequence=sentiment_colors,
                             labels={"daily_return_categorical_labeled": "Returns"},
                             category_orders={"daily_return_categorical_labeled": [
                                 "super_bullish", "bullish", "weak_bullish",
                                 "neutral",
                                 "weak_bearish", "bearish", "super_bearish"]},
                             hover_data=["stock", "main_top",
                                         "adjusted_sentiment_categorical",
                                         "daily_return_categorical_labeled",
                                         "next_day_return_categorical_labeled",
                                         "two_day_return_categorical_labeled"]
                             )
            fig.update_yaxes(title='y', visible=False, showticklabels=False)
            fig.update_xaxes(title='Topic Intensity', visible=True, showticklabels=False)
            return fig
        elif returns == 'next_day':
            sentiment_colors = ['#008000', '#00ff00', '#b3ffb3',
                                '#bfbfbf',
                                '#ff9999', '#ff3333', '#990000', ]
            fig = px.scatter(df,
                             y="y_cord",
                             x="x_cord", color="next_day_return_categorical_labeled",
                             opacity=0.6,
                             title="Article topic space by next day return",
                             color_discrete_sequence=sentiment_colors,
                             labels={"next_day_return_categorical_labeled": "Returns"},
                             category_orders={"next_day_return_categorical_labeled": [
                                 "super_bullish", "bullish", "weak_bullish",
                                 "neutral",
                                 "weak_bearish", "bearish", "super_bearish"]},
                             hover_data=["stock", "main_top",
                                         "adjusted_sentiment_categorical",
                                         "daily_return_categorical_labeled",
                                         "next_day_return_categorical_labeled",
                                         "two_day_return_categorical_labeled"]
                             )
            fig.update_yaxes(title='y', visible=False, showticklabels=False)
            fig.update_xaxes(title='Topic Intensity', visible=True, showticklabels=False)
            return fig
        elif returns == "2_days":
            sentiment_colors = ['#008000', '#00ff00', '#b3ffb3',
                                '#bfbfbf',
                                '#ff9999', '#ff3333', '#990000', ]
            fig = px.scatter(df,
                             y="y_cord",
                             x="x_cord", color="two_day_return_categorical_labeled",
                             opacity=0.6,
                             title="Article topic space by next two day return",
                             color_discrete_sequence=sentiment_colors,
                             labels={"two_day_return_categorical_labeled": "Returns"},
                             category_orders={"two_day_return_categorical_labeled": [
                                 "super_bullish", "bullish", "weak_bullish",
                                 "neutral",
                                 "weak_bearish", "bearish", "super_bearish"]},
                             hover_data=["stock", "main_top",
                                         "adjusted_sentiment_categorical",
                                         "daily_return_categorical_labeled",
                                         "next_day_return_categorical_labeled",
                                         "two_day_return_categorical_labeled"]
                             )
            fig.update_yaxes(title='y', visible=False, showticklabels=False)
            fig.update_xaxes(title='Topic Intensity', visible=True, showticklabels=False)
            return fig

    def filter_data(self, sentiment_filter=0, company_filter=0):
        df = self.df
        if sentiment_filter == 'positive':
            df = df[df["adjusted_sentiment_categorical"].isin(["positive", "weakly positive", "super positive"])]
        elif sentiment_filter == "negative":
            df = df[df["adjusted_sentiment_categorical"].isin(["negative", "weakly negative", "super negative"])]

        if company_filter != [] and company_filter != "Select a Company" and company_filter != 0:
            df = df[df["stock"].isin(company_filter)]

        return df

    def recommended_articles(self, sentiment_filter=0, company_filter=0, daily_return_filter=0,
                             next_day_return_filter=0, two_day_return_filter=0, ap1=1, average=0):
        article_list = []
        df = self.df
        if sentiment_filter == 'positive':
            df = df[df["adjusted_sentiment_categorical"].isin(["positive", "weakly positive", "super positive"])]
        elif sentiment_filter == "negative":
            df = df[df["adjusted_sentiment_categorical"].isin(["negative", "weakly negative", "super negative"])]

        if company_filter != [] and company_filter != "Select a Company" and company_filter != 0:
            df = df[df["stock"].isin(company_filter)]

        if daily_return_filter == 1:
            if ap1 == 1:
                article_list = []
                for i in df["impact_score_daily_return_ap1"].abs().nlargest(50).index:
                    ar = df.loc[i]
                    article = [i,
                               ar["stock"],
                               round(abs(ar['impact_score_daily_return_ap1']), 4),
                               ar["title"],
                               str(ar[self.top_list][ar[self.top_list] > 0.0001].index.tolist())[1:-1],
                               str(round(ar["positive"] * 100, 2)) + "%",
                               str(round(ar["negative"] * 100, 2)) + "%",
                               ar["daily_return_categorical_labeled"]]
                    article_list.append(article)
            elif average == 1:
                article_list = []
                for i in df["impact_score_daily_return_average"].abs().nlargest(50).index:
                    ar = df.loc[i]
                    article = [i,
                               ar["stock"],
                               round(abs(ar['impact_score_daily_return_average']), 4),
                               ar["title"],
                               str(ar[self.top_list][ar[self.top_list] > 0.0001].index.tolist())[1:-1],
                               str(round(ar["positive"] * 100, 2)) + "%",
                               str(round(ar["negative"] * 100, 2)) + "%",
                               ar["daily_return_categorical_labeled"]]
                    article_list.append(article)

        elif next_day_return_filter == 1:
            if ap1 == 1:
                article_list = []
                for i in df["impact_score_next_day_return_ap1"].abs().nlargest(50).index:
                    ar = df.loc[i]
                    article = [i,
                               ar["stock"],
                               round(abs(ar['impact_score_next_day_return_ap1']), 4),
                               ar["title"],
                               str(ar[self.top_list][ar[self.top_list] > 0.0001].index.tolist())[1:-1],
                               str(round(ar["positive"] * 100, 2)) + "%",
                               str(round(ar["negative"] * 100, 2)) + "%",
                               ar["next_day_return_categorical_labeled"]]
                    article_list.append(article)
            elif average == 1:
                article_list = []
                for i in df["impact_score_next_day_return_average"].abs().nlargest(50).index:
                    ar = df.loc[i]
                    article = [i,
                               ar["stock"],
                               round(abs(ar['impact_score_next_day_return_average']), 4),
                               ar["title"],
                               str(ar[self.top_list][ar[self.top_list] > 0.0001].index.tolist())[1:-1],
                               str(round(ar["positive"] * 100, 2)) + "%",
                               str(round(ar["negative"] * 100, 2)) + "%",
                               ar["next_day_return_categorical_labeled"]]
                    article_list.append(article)

        elif two_day_return_filter == 1:
            if ap1 == 1:
                article_list = []
                for i in df["impact_score_2_day_return_ap1"].abs().nlargest(50).index:
                    ar = df.loc[i]
                    article = [i,
                               ar["stock"],
                               round(abs(ar['impact_score_2_day_return_ap1']), 4),
                               ar["title"],
                               str(ar[self.top_list][ar[self.top_list] > 0.0001].index.tolist())[1:-1],
                               str(round(ar["positive"] * 100, 2)) + "%",
                               str(round(ar["negative"] * 100, 2)) + "%",
                               ar["two_day_return_categorical_labeled"]]
                    article_list.append(article)
            elif average == 1:
                article_list = []
                for i in df["impact_score_2_day_return_average"].abs().nlargest(50).index:
                    ar = df.loc[i]
                    article = [i,
                               ar["stock"],
                               round(abs(ar['impact_score_2_day_return_average']), 4),
                               ar["title"],
                               str(ar[self.top_list][ar[self.top_list] > 0.0001].index.tolist())[1:-1],
                               str(round(ar["positive"] * 100, 2)) + "%",
                               str(round(ar["negative"] * 100, 2)) + "%",
                               ar["two_day_return_categorical_labeled"]]
                    article_list.append(article)

        return article_list

    def article_stats(self, article):
        element = dbc.Col([
            # dbc.Button("View", color="primary", size="sm", id=f"article_bttn_{article[0]}"),
            dbc.Row([*[
                dbc.Row([
                    dbc.Col(html.Div(article[1]),
                            width=1,
                            style={'font-weight': 'bold'}),
                    dbc.Col(html.Div(article[2]),
                            width=2),
                    dbc.Col(html.Div(article[3]), width=3),
                    dbc.Col(html.Div(article[4]), width=2),
                    dbc.Col(html.Div(article[5]), width=2),
                    dbc.Col(html.Div(article[6]), width=2),
                    dbc.Button("View", color="primary", size="sm", id=f"article_bttn_{article[0]}")
                ]),
            ]], style={"flexWrap": "nowrap"}),
            html.Br()
        ])
        # print(element)
        return element

    def article_statistics(self, article_index):
        a_ind = int(float(article_index))
        d = self.df.loc[article_index]
        a = []
        for i in range(0, len(self.df.loc[a_ind][self.top_list].to_list())):
            if self.df.loc[a_ind][self.top_list].to_list()[i] > 0:
                a.append(str(self.top_list[i]) + " : " + str(round(self.df.loc[a_ind][self.top_list].to_list()[i], 4)))
        b = []
        for i in range(0, len(self.df.loc[a_ind][self.top_sent_list].to_list())):
            if abs(self.df.loc[a_ind][self.top_sent_list].to_list()[i]) > 0.001:
                b.append(str(self.top_sent_list[i]) + " : " + str(round(self.df.loc[a_ind][self.top_sent_list].to_list()[i], 4)))

        element = dbc.Col([
            dbc.Row(html.Div(d["title"]), style={"font-style": "bold",
                                                 'fontSize': 18}),
            dbc.Row(html.Div(d["date"]), style={"font-style": "italic",
                                                'fontSize': 12}),
            dbc.Row(html.A("Source", href=d['link'])),
            html.Br(),
            html.Div("Topic weights"),
            dbc.Row(dbc.Card(str(a)[1:-1])),
            html.Br(),
            html.Div("Topic sentiment"),
            dbc.Row(dbc.Card(str(b)[1:-1])),
            html.Br(),
            html.Div("Article Sentiment Score"),
            dbc.Row(dbc.Card([
                html.Div(["Positive: ", d['positive']]),
                html.Div(["Negative: ", d['negative']]),
            ])),
            html.Br(),
            html.Div("Article Content"),
            dbc.Row(dbc.Card(d["content"]))])
        return element
