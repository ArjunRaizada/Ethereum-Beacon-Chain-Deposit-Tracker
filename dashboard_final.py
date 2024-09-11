import pymongo
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from datetime import datetime

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Luganodes"]
collection = db["Ethereum1"]


# Fetch data from MongoDB and load it into a DataFrame
def fetch_data():
    data = list(collection.find())
    df = pd.DataFrame(data)

    # Convert block_time_stamp to a datetime object for proper plotting
    df['block_time_stamp'] = pd.to_datetime(df['block_time_stamp'], unit='s')

    return df


# Prepare Dash app
app = dash.Dash(__name__)

# Fetch data and create DataFrame
df = fetch_data()
df.head()

# Layout of the app
app.layout = html.Div([
    html.H1("Ethereum Block Data Visualization"),

    # Dropdown to select what to visualize (gas_fee, amount)
    dcc.Dropdown(
        id='yaxis-column',
        options=[
            {'label': 'Gas Fee', 'value': 'gas_fee'},
            {'label': 'Amount', 'value': 'Amount'}
        ],
        value='gas_fee'
    ),

    # Graph for visualization
    dcc.Graph(id='block-graph')
])


# Callback to update the graph based on the selected y-axis value
@app.callback(
    dash.dependencies.Output('block-graph', 'figure'),
    [dash.dependencies.Input('yaxis-column', 'value')]
)
def update_graph(yaxis_column_name):
    fig = px.line(df, x='block_time_stamp', y=yaxis_column_name, title=f'{yaxis_column_name} over time')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
