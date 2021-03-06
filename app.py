import flask
import dash
import dash_html_components as html
import plotly.express as px
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import time
from keywordQuery import knowledge_graph, KG_API
from twitterQuery import scale_bird
from twitterNLP import the_burd_is_the_word
from pages import (
    blog,
    serpScraper,
    home,
    knowledgeGraph,
    twitterGraph,
    nlpStats,
    overview,
)


server = flask.Flask(__name__)



app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True
)
app.layout = html.Div(
    [dcc.Location(id="url", refresh=True), html.Div(id="page-content")]
)


# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/blog":
        return blog.create_layout(app)
    elif pathname == "/graphapi":
        return knowledgeGraph.create_layout(app)
    elif pathname == "/serpscrape":
        return serpScraper.create_layout(app)
    elif pathname == "/twitterscrape":
        return twitterGraph.create_layout(app)
    elif pathname == "/":
        return home.create_layout(app)
    elif pathname == "/nlpstats":
        return nlpStats.create_layout(app)
    else:
        return overview.create_layout(app)


# all callbacks for pages go here
# SERP Scraper Callback
# @app.callback(
#     Output("serp_scrape", "data"),
#     [Input('serp_button', 'n_clicks')],
#     state=[State("serp_input", "value")]
# )
# def update_output2(n_clicks, serp_input):
#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         pass
        

# Knowledge Graph Callback
@app.callback(
    Output("scraped", "data"),
    [Input('button', 'n_clicks')],
    state=[State("input2", "value")]
)
def update_output(n_clicks, input2):
    if n_clicks is None:
        raise PreventUpdate
    else:
        searched2 =  knowledge_graph(key=KG_API, query=input2)
        searched2['#'] = list(range(1, len(searched2) + 1))
        return searched2.to_dict('rows')
        
        # return clickMethod(input2)

# Twitter Page Callbacks
@app.callback(
    Output("twitter_scraped", "data"),
    [Input('twitter_button', 'n_clicks')],
    state=[State("twitter_input", "value")]
)
def update_output(n_clicks, twitter_input):
    if n_clicks is None:
        raise PreventUpdate
    else:
        tweeter =  scale_bird(twitter_input)
        print(tweeter)
        # searched2['#'] = list(range(1, len(searched2) + 1))
        return tweeter.to_dict('rows')
        
        # return clickMethod(input2)



# Twitter NLP Histogram of Tweets Callback
@app.callback(
    Output("graph", "figure"), 
    [Input("timeline_vectors", "data")])
def display_color(timeline_vectors):
    # data = np.random.normal(mean, std, size=500)
    # fig = px.histogram(data, nbins=30, range_x=[-10, 10])
    new = pd.DataFrame.from_dict(timeline_vectors)
    results_words = the_burd_is_the_word(new)
    # df = px.data.tips()
    fig = px.histogram(x=results_words['count'], y=results_words['keyword'], title="Twitter Word Frequency")
    fig.update_xaxes(title_text='Counts')
    fig.update_yaxes(title_text='Keywords')
    return fig

# Twitter Timeline Processing Callback
@app.callback(
    Output("timeline_vectors", "data"),
    [Input('twitter_button', 'n_clicks')],
    state=[State("twitter_input", "value")]
)
def update_output(n_clicks, twitter_input):
    if n_clicks is None:
        raise PreventUpdate
    else:
        tweeter =  scale_bird(twitter_input)
        print(tweeter)
        # searched2['#'] = list(range(1, len(searched2) + 1))
        return tweeter.to_dict('rows')



# keeping data queries withing data callbacks ensures fresh data is coming in upon input change

if __name__ == '__main__':
    app.run_server(debug=False)