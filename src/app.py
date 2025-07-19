import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

# Load dataset exactly as you had it
data_path = 'C:\\Users\\Cesar Dushimimana\\Documents\\aave-credit-scoring\\data\\aave_cleaned_transactions.csv'
df = pd.read_csv(data_path, parse_dates=['timestamp'])
df['date'] = df['timestamp'].dt.date

# Themes
LIGHT_THEME = {
    'background': '#ffffff',
    'text': '#000000',
    'table_header': '#e1e1e1'
}
DARK_THEME = {
    'background': '#2c2c2c',
    'text': '#f5f5f5',
    'table_header': '#444444'
}

# Initialize app WITH suppress_callback_exceptions=True to avoid the callback error on dynamic IDs
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = 'Assets & Transactions Time Series Dashboard'

# Layout with tabs and main container
app.layout = html.Div([
    html.H1("Assets & Transactions Dashboard", style={'textAlign': 'center', 'marginBottom': 30}),

    # Dark mode toggle
    html.Div([
        dcc.Checklist(
            id='dark-mode-toggle',
            options=[{'label': 'Dark Mode', 'value': 'dark'}],
            value=[],
            style={'display': 'inline-block'}
        )
    ], style={'textAlign': 'center', 'marginBottom': 20}),

    # Tabs
    dcc.Tabs(id='tabs', value='tab-assets', children=[
        dcc.Tab(label='Assets Time Series', value='tab-assets'),
        dcc.Tab(label='Total Volume by Action', value='tab-volume'),
    ]),

    # Tab content container
    html.Div(id='tab-content', style={'marginTop': 30}),

], id='main-container', style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'minHeight': '100vh'})

# Helper function to get theme dict
def get_theme(dark_mode_values):
    return DARK_THEME if 'dark' in dark_mode_values else LIGHT_THEME

# Callback to render the tabs content
@app.callback(
    Output('tab-content', 'children'),
    Output('main-container', 'style'),
    Input('tabs', 'value'),
    Input('dark-mode-toggle', 'value'),
)
def render_tab_content(selected_tab, dark_mode_values):
    theme = get_theme(dark_mode_values)
    style = {
        'backgroundColor': theme['background'],
        'color': theme['text'],
        'fontFamily': 'Arial, sans-serif',
        'minHeight': '100vh',
        'padding': '20px'
    }

    if selected_tab == 'tab-assets':
        # Layout for the Assets Time Series tab
        layout = html.Div([
            html.Div([
                html.Div([
                    html.Label("Select Timeframe:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='timeframe-dropdown',
                        options=[
                            {'label': 'Daily', 'value': 'D'},
                            {'label': 'Weekly', 'value': 'W'},
                            {'label': 'Monthly', 'value': 'M'}
                        ],
                        value='D',
                        clearable=False,
                        style={'width': '100%'}
                    )
                ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingRight': 20}),

                html.Div([
                    html.Label("Select Asset(s):", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='asset-dropdown',
                        options=[{'label': asset, 'value': asset} for asset in sorted(df['asset_symbol'].dropna().unique())],
                        value=[],
                        multi=True,
                        placeholder="Select one or more assets (default top 5)",
                        style={'width': '100%'}
                    ),
                ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            ], style={'marginBottom': 30, 'maxWidth': 900, 'margin': 'auto'}),

            html.Div(id='total-volume-summary', style={'textAlign': 'center', 'fontSize': 18, 'marginBottom': 15}),

            dcc.Graph(id='time-series-chart', style={'height': '600px', 'maxWidth': 1000, 'margin': 'auto'}),

            html.Div(id='data-table-container', style={'maxHeight': '400px', 'overflowY': 'auto', 'marginTop': 30, 'maxWidth': 1000, 'margin': 'auto'}),

            html.Div([
                html.Button("Download Filtered Data as CSV", id='download-button', n_clicks=0,
                            style={'padding': '10px 20px', 'fontSize': 16, 'cursor': 'pointer'}),
                dcc.Download(id='download-dataframe-csv')
            ], style={'textAlign': 'center', 'marginTop': 40}),
        ])

    elif selected_tab == 'tab-volume':
        # Layout for the Total Volume by Action tab
        layout = html.Div([
            dcc.Graph(id='volume-by-action-type')
        ])

    else:
        layout = html.Div("Tab not found")

    return layout, style


# Callback to update the time series chart, total volume and data table on tab-assets
@app.callback(
    Output('time-series-chart', 'figure'),
    Output('total-volume-summary', 'children'),
    Output('data-table-container', 'children'),
    Input('timeframe-dropdown', 'value'),
    Input('asset-dropdown', 'value'),
    Input('dark-mode-toggle', 'value')
)
def update_time_series(timeframe, selected_assets, dark_mode_values):
    theme = get_theme(dark_mode_values)
    is_dark_mode = 'dark' in dark_mode_values

    dff = df.copy()
    if not selected_assets:
        top_assets = dff.groupby('asset_symbol')['amount_usd'].sum().nlargest(5).index.tolist()
        selected_assets = top_assets
    dff = dff[dff['asset_symbol'].isin(selected_assets)]

    dff.set_index('timestamp', inplace=True)
    dff_resampled = dff.groupby('asset_symbol').resample(timeframe)['amount_usd'].sum().reset_index()

    fig = px.line(
        dff_resampled,
        x='timestamp',
        y='amount_usd',
        color='asset_symbol',
        labels={'timestamp': 'Date', 'amount_usd': 'USD Volume', 'asset_symbol': 'Asset'},
        title='USD Volume Over Time by Asset',
        template='plotly_dark' if is_dark_mode else 'plotly_white'
    )

    fig.update_layout(
        hovermode='x unified',
        legend_title_text='Assets',
        xaxis=dict(
            rangeselector=dict(
                buttons=[
                    dict(count=1, label='1m', step='month', stepmode='backward'),
                    dict(count=3, label='3m', step='month', stepmode='backward'),
                    dict(count=6, label='6m', step='month', stepmode='backward'),
                    dict(step='all')
                ]
            ),
            rangeslider=dict(visible=True),
            type='date',
            title='Date'
        ),
        yaxis=dict(title='USD Volume'),
        margin=dict(l=40, r=40, t=80, b=40)
    )

    total_volume = dff_resampled['amount_usd'].sum()
    total_volume_text = f"Total USD Volume for selected assets & timeframe: ${total_volume:,.2f}"

    # Data table (basic HTML)
    table_header_style = {
        'backgroundColor': theme['table_header'],
        'color': theme['text'],
        'padding': '8px',
        'border': '1px solid #ddd'
    }
    table_cell_style = {
        'padding': '8px',
        'border': '1px solid #ddd',
        'color': theme['text']
    }

    dff_resampled_sorted = dff_resampled.sort_values(['asset_symbol', 'timestamp'])
    dff_resampled_sorted['timestamp'] = dff_resampled_sorted['timestamp'].dt.strftime('%Y-%m-%d')

    table_rows = []
    for _, row in dff_resampled_sorted.iterrows():
        table_rows.append(html.Tr([
            html.Td(row['timestamp'], style=table_cell_style),
            html.Td(row['asset_symbol'], style=table_cell_style),
            html.Td(f"${row['amount_usd']:,.2f}", style=table_cell_style)
        ]))

    table = html.Table([
        html.Thead(html.Tr([
            html.Th("Date", style=table_header_style),
            html.Th("Asset", style=table_header_style),
            html.Th("USD Volume", style=table_header_style)
        ])),
        html.Tbody(table_rows)
    ], style={'width': '100%', 'borderCollapse': 'collapse'})

    container = html.Div(table, style={'overflowX': 'auto', 'maxHeight': '400px', 'overflowY': 'auto'})

    return fig, total_volume_text, container

# Callback for volume by action type bar chart on tab-volume
@app.callback(
    Output('volume-by-action-type', 'figure'),
    Input('dark-mode-toggle', 'value')
)
def update_volume_by_action(dark_mode_values):
    theme = get_theme(dark_mode_values)
    is_dark_mode = 'dark' in dark_mode_values

    action_volume = df.groupby('action_type')['amount_usd'].sum().sort_values(ascending=False).reset_index()

    fig = px.bar(
        action_volume,
        x='action_type',
        y='amount_usd',
        text='amount_usd',
        labels={'action_type': 'Action Type', 'amount_usd': 'Total USD Volume'},
        title='Total USD Volume by Action Type',
        template='plotly_dark' if is_dark_mode else 'plotly_white'
    )

    fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
    fig.update_layout(
        yaxis_title='USD Volume',
        xaxis_title='Action Type',
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig

# Callback to download filtered data CSV from tab-assets filters
@app.callback(
    Output('download-dataframe-csv', 'data'),
    Input('download-button', 'n_clicks'),
    State('timeframe-dropdown', 'value'),
    State('asset-dropdown', 'value'),
    prevent_initial_call=True
)
def download_filtered_data(n_clicks, timeframe, selected_assets):
    dff = df.copy()
    if not selected_assets:
        top_assets = dff.groupby('asset_symbol')['amount_usd'].sum().nlargest(5).index.tolist()
        selected_assets = top_assets
    dff = dff[dff['asset_symbol'].isin(selected_assets)]

    dff.set_index('timestamp', inplace=True)
    dff_resampled = dff.groupby('asset_symbol').resample(timeframe)['amount_usd'].sum().reset_index()
    dff_resampled['timestamp'] = dff_resampled['timestamp'].dt.strftime('%Y-%m-%d')

    return dcc.send_data_frame(dff_resampled.to_csv, "filtered_asset_data.csv", index=False)

if __name__ == '__main__':
    app.run(debug=True)
