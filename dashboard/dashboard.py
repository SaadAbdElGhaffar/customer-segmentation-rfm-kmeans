import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os

# Initialize the app with external CSS
app = dash.Dash(__name__)

# Custom CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Roboto', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
            }
            .main-container {
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                padding: 30px;
                margin: 0 auto;
                max-width: 1400px;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
                padding: 20px;
                background: linear-gradient(45deg, #667eea, #764ba2);
                border-radius: 10px;
                color: white;
            }
            .stats-container {
                display: flex;
                justify-content: space-around;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }
            .stat-card {
                background: linear-gradient(45deg, #4facfe, #00f2fe);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin: 10px;
                min-width: 200px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            }
            .chart-container {
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                margin: 20px 0;
                padding: 20px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

def load_data():
    try:
        if os.path.exists("../outputs/rfm_segments.csv"):
            rfm_segments = pd.read_csv("../outputs/rfm_segments.csv")
        else:
            rfm_segments = None
        
        if os.path.exists("../outputs/clustered_segments.csv"):
            clustered_data = pd.read_csv("../outputs/clustered_segments.csv")
        else:
            clustered_data = None
            
        return rfm_segments, clustered_data
    except:
        return None, None

rfm_segments, clustered_data = load_data()

# Define color schemes
colors = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#00d4aa',
    'info': '#4facfe',
    'warning': '#f0b90b',
    'danger': '#ef5777'
}

app.layout = html.Div([
    html.Div([
        # Header
        html.Div([
            html.H1([
                html.I(className="fas fa-chart-pie", style={'margin-right': '15px'}),
                "Customer Segmentation Analytics"
            ], style={'margin': '0', 'font-size': '2.5rem', 'font-weight': '300'}),
            html.P("RFM Analysis & K-Means Clustering Dashboard", 
                  style={'margin': '10px 0 0 0', 'font-size': '1.2rem', 'opacity': '0.9'})
        ], className='header'),
        
        # Stats Cards
        html.Div([
            html.Div([
                html.H3(f"{len(rfm_segments) if rfm_segments is not None else 'N/A'}", 
                       style={'margin': '0', 'font-size': '2rem'}),
                html.P("Total Customers", style={'margin': '5px 0 0 0'})
            ], className='stat-card'),
            
            html.Div([
                html.H3(f"{rfm_segments['segment'].nunique() if rfm_segments is not None else 'N/A'}", 
                       style={'margin': '0', 'font-size': '2rem'}),
                html.P("RFM Segments", style={'margin': '5px 0 0 0'})
            ], className='stat-card'),
            
            html.Div([
                html.H3(f"{clustered_data['Cluster'].nunique() if clustered_data is not None else 'N/A'}", 
                       style={'margin': '0', 'font-size': '2rem'}),
                html.P("Clusters", style={'margin': '5px 0 0 0'})
            ], className='stat-card'),
            
            html.Div([
                html.H3(f"{len(rfm_segments[rfm_segments['segment'] == 'champions']) if rfm_segments is not None else 'N/A'}", 
                       style={'margin': '0', 'font-size': '2rem'}),
                html.P("Champions", style={'margin': '5px 0 0 0'})
            ], className='stat-card'),
        ], className='stats-container'),
        
        # Charts Row 1
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id="rfm-sunburst")
                ], className='chart-container')
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.Div([
                    dcc.Graph(id="cluster-3d")
                ], className='chart-container')
            ], style={'width': '50%', 'display': 'inline-block'}),
        ]),
        
        # Charts Row 2
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id="rfm-heatmap")
                ], className='chart-container')
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.Div([
                    dcc.Graph(id="cluster-comparison")
                ], className='chart-container')
            ], style={'width': '50%', 'display': 'inline-block'}),
        ]),
        
        # Data Table
        html.Div([
            html.Div([
                html.H3("📊 Customer Segments Summary", 
                       style={'color': colors['primary'], 'margin-bottom': '20px'}),
                html.Div(id="segments-table")
            ], className='chart-container')
        ])
        
    ], className='main-container')
])

@app.callback(
    Output("rfm-sunburst", "figure"),
    Input("rfm-sunburst", "id")
)
def update_sunburst(_):
    if rfm_segments is None:
        return {"data": [], "layout": {"title": "No RFM data found. Run main.py first."}}
    
    # Create hierarchical data for sunburst
    segment_counts = rfm_segments['segment'].value_counts()
    
    fig = go.Figure(go.Sunburst(
        labels=list(segment_counts.index) + ['All Customers'],
        parents=['All Customers'] * len(segment_counts.index) + [''],
        values=list(segment_counts.values) + [segment_counts.sum()],
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percentParent}<extra></extra>',
        maxdepth=2,
    ))
    
    fig.update_layout(
        title="🌅 Customer Segments Hierarchy",
        font_size=12,
        font_family="Roboto",
        title_font_size=18,
        title_font_color=colors['primary'],
        height=500
    )
    
    return fig

@app.callback(
    Output("cluster-3d", "figure"),
    Input("cluster-3d", "id")
)
def update_3d_scatter(_):
    if clustered_data is None:
        return {"data": [], "layout": {"title": "No cluster data found. Run main.py first."}}
    
    fig = px.scatter_3d(
        clustered_data,
        x='Recency',
        y='Frequency',
        z='Monetary',
        color='Cluster_Labels',
        title="🎯 3D Cluster Visualization",
        labels={'Cluster_Labels': 'Cluster'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_layout(
        scene=dict(
            xaxis_title="Recency (Log)",
            yaxis_title="Frequency (Log)",
            zaxis_title="Monetary (Log)",
            bgcolor="white"
        ),
        font_family="Roboto",
        title_font_size=18,
        title_font_color=colors['primary'],
        height=500
    )
    
    return fig

@app.callback(
    Output("rfm-heatmap", "figure"),
    Input("rfm-heatmap", "id")
)
def update_heatmap(_):
    if rfm_segments is None:
        return {"data": [], "layout": {"title": "No RFM data found. Run main.py first."}}
    
    # Create RFM score heatmap
    heatmap_data = rfm_segments.groupby(['recency_score', 'frequency_score']).size().reset_index(name='count')
    heatmap_pivot = heatmap_data.pivot(index='recency_score', columns='frequency_score', values='count').fillna(0)
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values,
        x=[f'F{i}' for i in heatmap_pivot.columns],
        y=[f'R{i}' for i in heatmap_pivot.index],
        colorscale='Viridis',
        hoverongaps=False,
        hovertemplate='Recency: %{y}<br>Frequency: %{x}<br>Count: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title="🔥 RFM Score Heatmap",
        xaxis_title="Frequency Score",
        yaxis_title="Recency Score",
        font_family="Roboto",
        title_font_size=18,
        title_font_color=colors['primary'],
        height=500
    )
    
    return fig

@app.callback(
    Output("cluster-comparison", "figure"),
    Input("cluster-comparison", "id")
)
def update_comparison(_):
    if rfm_segments is None or clustered_data is None:
        return {"data": [], "layout": {"title": "No data found. Run main.py first."}}
    
    # Create subplot for comparison
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "domain"}, {"type": "domain"}]],
        subplot_titles=("RFM Segments", "K-Means Clusters")
    )
    
    # RFM pie
    rfm_counts = rfm_segments['segment'].value_counts()
    fig.add_trace(
        go.Pie(labels=rfm_counts.index, values=rfm_counts.values, name="RFM"),
        row=1, col=1
    )
    
    # Cluster pie
    cluster_counts = clustered_data['Cluster_Labels'].value_counts()
    fig.add_trace(
        go.Pie(labels=cluster_counts.index, values=cluster_counts.values, name="Clusters"),
        row=1, col=2
    )
    
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig.update_layout(
        title_text="📈 Segmentation Methods Comparison",
        font_family="Roboto",
        title_font_size=18,
        title_font_color=colors['primary'],
        height=500
    )
    
    return fig

@app.callback(
    Output("segments-table", "children"),
    Input("segments-table", "id")
)
def update_table(_):
    if rfm_segments is None:
        return html.P("No data available. Please run main.py first.", 
                     style={'text-align': 'center', 'color': colors['danger']})
    
    # Create summary table
    summary = rfm_segments.groupby('segment').agg({
        'CustomerID': 'count',
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean'
    }).round(2)
    
    summary.columns = ['Count', 'Avg_Recency', 'Avg_Frequency', 'Avg_Monetary']
    summary['Percentage'] = (summary['Count'] / summary['Count'].sum() * 100).round(1)
    summary = summary.reset_index()
    
    return dash_table.DataTable(
        data=summary.to_dict('records'),
        columns=[{"name": i.replace('_', ' '), "id": i} for i in summary.columns],
        style_cell={
            'textAlign': 'center',
            'fontFamily': 'Roboto',
            'fontSize': '14px',
            'padding': '12px'
        },
        style_header={
            'backgroundColor': colors['primary'],
            'fontWeight': 'bold',
            'color': 'white',
            'fontSize': '16px'
        },
        style_data_conditional=[
            {
                'if': {'filter_query': '{segment} = champions'},
                'backgroundColor': '#e8f5e8',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{segment} = at_Risk'},
                'backgroundColor': '#ffe8e8',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{segment} = loyal_customers'},
                'backgroundColor': '#e8f0ff',
                'color': 'black',
            }
        ],
        style_table={'margin': '20px 0'}
    )

if __name__ == "__main__":
    print("🌐 Open http://127.0.0.1:8050 in your browser")
    app.run(debug=True)