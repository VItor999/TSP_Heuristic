import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import dash_bootstrap_components as dbc  
from GA_implemented import GA_implemented
from benchmark import benchmark, find_route
from tsp_utils.general import *
import base64
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div(
    style={"backgroundColor": "#1e1e1e", "color": "white", "padding": "20px"},
    children=[
        html.H1(
            "Genetic Algorithm Dashboard",
            style={"textAlign": "left", "color": "white", "marginBottom": "20px"},
        ),
        html.Div(
            style={"display": "flex", "flexDirection": "row"},
            children=[
                # Plot 1
                html.Div(
                    dcc.Graph(id="plot1"),
                    style={"width": "49%", "marginRight": "2%", "backgroundColor": "#333"},
                ),
                # Plot 2
                html.Div(
                    dcc.Graph(id="plot2"),
                    style={"width": "49%", "backgroundColor": "#333"},
                ),
            ],
        ),
        # Control panel with radio buttons, text fields, and execute button
        html.Div(
            style={
                "marginTop": "40px",
                "padding": "20px",
                "backgroundColor": "#333",
                "borderRadius": "10px",
                "textAlign": "center",
            },
            children=[
                # Label for radio button group
                html.Label(
                    "City Distribution Options:",
                    style={"color": "white", "fontSize": "22px", "fontWeight": "bold", "display": "block", "marginBottom": "15px"},
                ),
                # Radio buttons for selecting options (including Upload File option)
                dcc.RadioItems(
                    id="radio-options",
                    options=[
                        {"label": "Random", "value": "random"},
                        {"label": "Square", "value": "square"},
                        {"label": "Circle", "value": "circle"},
                        {"label": "Triangle", "value": "triangle"},
                        {"label": "Hexagon", "value": "hexagon"},
                        {"label": "Upload File", "value": "file"},
                    ],
                    value="square",
                    style={"marginBottom": "20px", "color": "white"},
                    labelStyle={"display": "inline-block", "marginRight": "20px", "fontSize": "20px"},
                    inputStyle={"marginRight": "10px", "transform": "scale(1.8)"},
                ),
                # File upload field (shown only when Upload File is selected)
                html.Div(
                    id="file-upload-div",
                    children=[
                        dcc.Upload(
                            id="file-upload",
                            children=html.Div(["Drag and Drop or ", html.A("Select a File")]),
                            style={
                                "width": "50%",
                                "height": "60px",
                                "lineHeight": "60px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "10px",
                                "textAlign": "center",
                                "margin": "auto",
                                "color": "white",
                            },
                            multiple=False,
                        )
                    ],
                    style={"display": "none"},
                ),
                html.Br(),
                # Label for GA algorithm parameters
                html.Label(
                    "GA Algorithm Parameters:",
                    style={"color": "white", "fontSize": "22px", "fontWeight": "bold", "display": "block", "marginBottom": "15px"},
                ),
                # Text fields for parameters (aligned properly)
                html.Div(
                    style={"marginTop": "20px", "display": "grid", "gridTemplateColumns": "repeat(3, 1fr)", "gap": "30px"},
                    children=[
                        # Number of Cities
                        html.Div(
                            children=[
                                html.Label("num_cities:", style={"color": "white", "fontSize": "20px", "marginBottom": "8px"}),
                                dcc.Input(id="num-cities", type="number", value=20, style={"width": "100%", "padding": "8px", "borderRadius": "5px"}),
                            ],
                            style={"textAlign": "left"},
                        ),
                        # Population Size
                        html.Div(
                            children=[
                                html.Label("population_size:", style={"color": "white", "fontSize": "20px", "marginBottom": "8px"}),
                                dcc.Input(id="population-size", type="number", value=100, style={"width": "100%", "padding": "8px", "borderRadius": "5px"}),
                            ],
                            style={"textAlign": "left"},
                        ),
                        # Number of Generations
                        html.Div(
                            children=[
                                html.Label("num_generations:", style={"color": "white", "fontSize": "20px", "marginBottom": "8px"}),
                                dcc.Input(id="num-generations", type="number", value=100, style={"width": "100%", "padding": "8px", "borderRadius": "5px"}),
                            ],
                            style={"textAlign": "left"},
                        ),
                        # Mutation Rate
                        html.Div(
                            children=[
                                html.Label("mutation_rate:", style={"color": "white", "fontSize": "20px", "marginBottom": "8px"}),
                                dcc.Input(id="mutation-rate", type="number", value=0.01, step=0.01, style={"width": "100%", "padding": "8px", "borderRadius": "5px"}),
                            ],
                            style={"textAlign": "left"},
                        ),
                        # Tournament Size
                        html.Div(
                            children=[
                                html.Label("tournament_size:", style={"color": "white", "fontSize": "20px", "marginBottom": "8px"}),
                                dcc.Input(id="tournament-size", type="number", value=5, style={"width": "100%", "padding": "8px", "borderRadius": "5px"}),
                            ],
                            style={"textAlign": "left"},
                        ),
                        # Elite Size
                        html.Div(
                            children=[
                                html.Label("elite_size:", style={"color": "white", "fontSize": "20px", "marginBottom": "8px"}),
                                dcc.Input(id="elite-size", type="number", value=5, style={"width": "100%", "padding": "8px", "borderRadius": "5px"}),
                            ],
                            style={"textAlign": "left"},
                        ),
                    ],
                ),
                html.Br(),
                # Execute button centered in the container
                html.Div(
                    style={
                        "marginTop": "30px",
                        "display": "flex",
                        "justifyContent": "center",
                        "alignItems": "center",
                    },
                    children=[
                        html.Button(
                            "Execute", id="execute-button", n_clicks=0,
                            style={
                                "padding": "20px 40px",
                                "fontSize": "18px",
                                "borderRadius": "10px",
                                "backgroundColor": "#007bff",
                                "color": "white",
                                "border": "none",
                                "cursor": "pointer",
                            }
                        ),
                    ],
                ),
            ],
        ),
        # Notification for file upload
        html.Div(id="upload-notification", children=[]),
        # Store to hold parsed file data
        dcc.Store(id='parsed-data-store', storage_type='memory')
    ],
)

@app.callback(
    Output("file-upload-div", "style"),
    [Input("radio-options", "value")],
)
def toggle_file_upload(radio_value):
    if radio_value == "file":
        return {"display": "block", "marginBottom": "20px"}
    else:
        return {"display": "none"}

# Callback to parse uploaded file and store data
@app.callback(
    [Output("upload-notification", "children"), Output("parsed-data-store", "data")],
    [Input("file-upload", "contents")],
    [State("file-upload", "filename")],
)
def parse_input(contents, filename):
    if contents is not None and filename != '':
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        try:
            if filename.endswith('.csv') or filename.endswith('.txt'):
                # Read the file using standard tools
                decoded_text = decoded.decode('utf-8')
                lines = decoded_text.strip().split("\n")
                if len(lines) != 2:
                    raise ValueError("The file must contain exactly two lines.")
                    
                # Parse each line into a list of numbers
                x_v = [int(num) for num in lines[0].split()]
                y_v = [int(num) for num in lines[1].split()]

                # Print out or use the parsed data
                print("Line 1 Data:", x_v)
                print("Line 2 Data:", y_v)
                parsed_data = list(zip(x_v, y_v))
                return (
                    dbc.Toast(
                        f"File '{filename}' uploaded and parsed successfully!",
                        id="file-upload-toast",
                        header="Upload Notification",
                        icon="success",
                        dismissable=True,
                        duration=4000,
                        style={"position": "fixed", "top": "10px", "right": "10px"},
                    ),
                    parsed_data 
                )
            else:
                return (
                    dbc.Toast(
                        f"Unsupported file type '{filename}'",
                        id="file-upload-toast",
                        header="Upload Error",
                        icon="danger",
                        dismissable=True,
                        duration=4000,
                        style={"position": "fixed", "top": "10px", "right": "10px"},
                    ),
                    None
                )
        except Exception as e:
            return (
                dbc.Toast(
                    f"There was an error processing the file: {str(e)}",
                    id="file-upload-toast",
                    header="Upload Error",
                    icon="danger",
                    dismissable=True,
                    duration=4000,
                    style={"position": "fixed", "top": "10px", "right": "10px"},
                ),
                None
            )
    return None, None


# Callback to update the plots when the "Execute" button is clicked
@app.callback(
    [Output("plot1", "figure"), Output("plot2", "figure")],
    [Input("execute-button", "n_clicks")],
    [
        State("radio-options", "value"),
        State("parsed-data-store", "data"),
        State("num-cities", "value"),
        State("population-size", "value"),
        State("num-generations", "value"),
        State("mutation-rate", "value"),
        State("tournament-size", "value"),
        State("elite-size", "value"),
    ],
)
def update_plots(n_clicks, selected_option, uploaded_data, num_cities, population_size,
                 num_generations, mutation_rate, tournament_size, elite_size ):
    num_cities = num_cities
    cities = None
    if selected_option == "file" and uploaded_data is not None:
        print(uploaded_data)
        cities = uploaded_data
    elif selected_option == "random":
        cities = generate_random_points(num_cities )
    else:
        cities = generate_form_points(num_cities,selected_option)

    data_model = create_data_model(cities)
    distance_matrix = compute_euclidean_distance_matrix(data_model["locations"])
    
    print("################# Benchmark Solution #################")
    solution_benchmark = benchmark(data_model["locations"])
    route_bench = find_route(solution_benchmark[1], solution_benchmark[2])
    benchmark_dist = calculate_route_distance(distance_matrix, route_bench)
    print(f"Distance: {benchmark_dist:.2f} m\n")
    print("Route Bench:\n\t",end = "")
    print_route(route_bench)

    
    print("################# Custom GA Solution #################")
    solution_GA = GA_implemented(data_model,population_size,num_generations,mutation_rate,tournament_size,elite_size)
    print(f"Distance: {solution_GA[2]:.2f} m\n")
    route_GA = solution_GA[1]
    print("Route GA:\n\t",end = "")
    print_route(route_GA)
    
    locations = data_model["locations"]
    x_coords, y_coords = zip(*locations)

    # Create plot 1 using Plotly for nodes and connections
    fig1 = go.Figure()

    # Add nodes (scatter plot of locations)
    fig1.add_trace(go.Scatter(
        x=x_coords, y=y_coords,
        mode='markers+text',
        marker=dict(size=10, color='blue'),
        text=[str(i) for i in range(len(locations))],
        textposition="top center",
        name='Nodes'
    ))

    # Add connections (lines between nodes)
    for i in range(len(route_bench) - 1):
        start_index = route_bench[i]
        end_index = route_bench[i + 1]
        fig1.add_trace(go.Scatter(
            x=[locations[start_index][0], locations[end_index][0]],
            y=[locations[start_index][1], locations[end_index][1]],
            mode='lines',
            line=dict(color='red', width=2),
            name='Connection'
        ))

    # Update layout for fig1
    fig1.update_layout(
        title=f"Plot 1: {selected_option}",
        plot_bgcolor="#333",
        paper_bgcolor="#333",
        font={"color": "white"},
        xaxis_title="X Coordinates",
        yaxis_title="Y Coordinates",
        showlegend=False,
    )

    # Create plot 2 similarly to fig1, or modify as needed for different data
    fig2 = go.Figure()

    # Add nodes (scatter plot of locations)
    fig2.add_trace(go.Scatter(
        x=x_coords, y=y_coords,
        mode='markers+text',
        marker=dict(size=10, color='blue'),
        text=[str(i) for i in range(len(locations))],
        textposition="top center",
        name='Nodes'
    ))

    # Add connections (lines between nodes)
    for i in range(len(route_GA) - 1):
        start_index = route_GA[i]
        end_index = route_GA[i + 1]
        fig2.add_trace(go.Scatter(
            x=[locations[start_index][0], locations[end_index][0]],
            y=[locations[start_index][1], locations[end_index][1]],
            mode='lines',
            line=dict(color='red', width=2),
            name='Connection'
        ))

    # Update layout for fig2
    fig2.update_layout(
        title=f"Plot 2: {selected_option}",
        plot_bgcolor="#333",
        paper_bgcolor="#333",
        font={"color": "white"},
        xaxis_title="X Coordinates",
        yaxis_title="Y Coordinates",
        showlegend=False,
    )
    return fig1, fig2

# Run app
if __name__ == "__main__":
    app.run_server(debug=False)
