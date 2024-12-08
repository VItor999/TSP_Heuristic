import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import dash_bootstrap_components as dbc  
from TABU_implemented import tabu_search
from benchmark import benchmark, find_route
from tsp_utils.general import *
import base64
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

#TODO List:
#  - MUST: Clean this code and reorganize it. 
#  - MUST: Add more features to the statistics tab
#  - MUST: Document this code
#  - EXTRA: Add third tab with the population information per generation 

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div(
    style={"backgroundColor": "#1e1e1e", "color": "white", "padding": "20px"},
    children=[
        html.H1(
            "Genetic Algorithm Application",
            style={"textAlign": "center", "color": "white", "marginBottom": "20px"},
        ),
        dcc.Tabs(
            id="tabs",
            value='main',
            children=[
                dcc.Tab(label='Simulated Annealig Dashboard', value='main', style={'backgroundColor': '#333', 'color': 'white'},
                        selected_style={'backgroundColor': '#007bff', 'color': 'white'}),
                dcc.Tab(label='Statistics', value='statistics', style={'backgroundColor': '#333', 'color': 'white'},
                        selected_style={'backgroundColor': '#007bff', 'color': 'white'}),
            ],
            style={'marginBottom': '20px'}
        ),
        html.Div(id='tabs-content', style={'backgroundColor': '#1e1e1e', 'padding': '20px'}),
        dcc.Store(id='shared-data-store', storage_type='memory')
    ]
)

statatistics_tab_layout =html.Div(
            style={"backgroundColor": "#333", "padding": "20px", "borderRadius": "10px"},
            children=[
                html.H2("Statistics", style={"color": "white", "textAlign": "center", "marginBottom": "20px"}),
                html.P("Here you can display various statistics related to the Genetic Algorithm runs.", style={"color": "white", "textAlign": "center"}),
                html.Div(
                    style={"marginTop": "20px", "display": "flex", "justifyContent": "center", "alignItems": "center"},
                    children=[
                        html.Div(
                            style={"width": "80%", "backgroundColor": "#1e1e1e", "padding": "20px", "borderRadius": "10px"},
                            children=[
                                        html.H4('Statistics from Generated Data'),
                                        html.Div(id='statistics-output')
                                # You can add more detailed statistics here
                            ],
                        )
                    ],
                )
            ]
        )

# App layout
execute_tab = html.Div(
    style={"backgroundColor": "#1e1e1e", "color": "white", "padding": "20px"},
    children=[
        html.Div(
            style={"display": "flex", "flexDirection": "row", "justifyContent": "space-between", "alignItems": "center"},
            children=[
                # Plot 1 with total distance label
                html.Div(
                    children=[
                        dcc.Graph(id="plot1", style={"width": "100%", "height": "100%"}),  # Ensures square graph
                        html.Div(
                            children=[
                                html.Label(
                                    id="total-distance-label-plot1",
                                    children="Distance: 0 m",
                                    style={
                                        "color": "white",
                                        "fontSize": "18px",
                                        "textAlign": "center",
                                        "display": "block",
                                    },
                                ),
                            ],
                            style={"marginTop": "10px", "textAlign": "center"},
                        ),
                    ],
                    style={
                        "width": "49%",
                        "aspectRatio": "1 / 1",  # Ensures a square aspect ratio
                        "backgroundColor": "#333",
                        "padding": "10px",
                        "borderRadius": "10px",
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "center",
                        "justifyContent": "center",
                    },
                ),
                # Plot 2 with total distance label
                html.Div(
                    children=[
                        dcc.Graph(id="plot2", style={"width": "100%", "height": "100%"}),  # Ensures square graph
                        html.Div(
                            children=[
                                html.Label(
                                    id="total-distance-label-plot2",
                                    children="Distance: 0 m",
                                    style={
                                        "color": "white",
                                        "fontSize": "18px",
                                        "textAlign": "center",
                                        "display": "block",
                                    },
                                ),
                            ],
                            style={"marginTop": "10px", "textAlign": "center"},
                        ),
                    ],
                    style={
                        "width": "49%",
                        "aspectRatio": "1 / 1",  # Ensures a square aspect ratio
                        "backgroundColor": "#333",
                        "padding": "10px",
                        "borderRadius": "10px",
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "center",
                        "justifyContent": "center",
                    },
                ),
            ],
        ),
        # Scaled content starts here
        html.Div(
            style={
                "transform": "scale(0.75)",  # Apply scaling to 75%
                "transformOrigin": "top left",  # Keep scaling from the top left corner
                "width": "133%",  # Compensate width for scaling to fit the space
            },
            children=[
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
                            style={
                                "color": "white",
                                "fontSize": "22px",
                                "fontWeight": "bold",
                                "display": "block",
                                "marginBottom": "15px",
                            },
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
                        # Label for SA algorithm parameters
                        html.Label(
                            "Simulated Annealing Parameters:",
                            style={
                                "color": "white",
                                "fontSize": "22px",
                                "fontWeight": "bold",
                                "display": "block",
                                "marginBottom": "15px",
                            },
                        ),
                        # Text fields for parameters (aligned properly)
                        html.Div(
                            style={
                                "marginTop": "20px",
                                "display": "grid",
                                "gridTemplateColumns": "repeat(3, 1fr)",
                                "gap": "30px",
                            },
                            children=[
                                # Number of Cities
                                html.Div(
                                    children=[
                                        html.Label(
                                            "num_cities:",
                                            style={
                                                "color": "white",
                                                "fontSize": "20px",
                                                "marginBottom": "8px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="num-cities",
                                            type="number",
                                            value=20,
                                            style={"width": "100%", "padding": "8px", "borderRadius": "5px"},
                                        ),
                                    ],
                                    style={"textAlign": "left"},
                                ),
                                # neighborhood_size
                                html.Div(
                                    children=[
                                        html.Label(
                                            "neighborhood_size:",
                                            style={
                                                "color": "white",
                                                "fontSize": "20px",
                                                "marginBottom": "8px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="neighborhood-size",
                                            type="number",
                                            value=500,
                                            style={"width": "100%", "padding": "8px", "borderRadius": "5px"},
                                        ),
                                    ],
                                    style={"textAlign": "left"},
                                ),
                                # Elite Size
                                html.Div(
                                    children=[
                                        html.Label(
                                            "restart_threshold:",
                                            style={
                                                "color": "white",
                                                "fontSize": "20px",
                                                "marginBottom": "8px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="restart-threshold",
                                            type="number",
                                            value=50,
                                            style={"width": "100%", "padding": "8px", "borderRadius": "5px"},
                                        ),
                                    ],
                                    style={"textAlign": "left"},
                                ),
                                html.Div(
                                    children=[
                                        html.Label(
                                            "max_tries:",
                                            style={
                                                "color": "white",
                                                "fontSize": "20px",
                                                "marginBottom": "8px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="max_tries",
                                            type="number",
                                            value=100,
                                            style={"width": "100%", "padding": "8px", "borderRadius": "5px"},
                                        ),
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
                                    "Execute",
                                    id="execute-button",
                                    n_clicks=0,
                                    style={
                                        "padding": "20px 40px",
                                        "fontSize": "18px",
                                        "borderRadius": "10px",
                                        "backgroundColor": "#007bff",
                                        "color": "white",
                                        "border": "none",
                                        "cursor": "pointer",
                                    },
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
        ),
    ],
)


# Callback to update content based on selected tab
@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def update_tab_content(tab_name):
    if tab_name == 'main':
       return execute_tab
    elif tab_name == 'statistics':
        return statatistics_tab_layout


@app.callback(
    Output("file-upload-div", "style"),
    [Input("radio-options", "value")],
)
def toggle_file_upload(radio_value):
    if radio_value == "file":
        return {"display": "block", "marginBottom": "20px"}
    else:
        return {"display": "none"}

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
                
                # Check the dimensionality of the input
                if len(lines) < 2 or len(lines) > 3:
                    raise ValueError("The file must contain exactly two (2D) or three (3D) lines.")
                
                # Parse each line into a list of numbers
                data = [list(map(int, line.split())) for line in lines]
                
                # Ensure all lines have the same number of entries
                num_points = len(data[0])
                if not all(len(line) == num_points for line in data):
                    raise ValueError("All lines in the file must have the same number of points.")
                
                # Combine parsed data into tuples
                parsed_data = list(zip(*data))
                print("Parsed Data:", parsed_data)
                
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



@app.callback(
    [Output("plot1", "figure"), Output("plot2", "figure"), Output('shared-data-store', 'data'),
     Output("total-distance-label-plot1", "children"), Output("total-distance-label-plot2", "children")],
    [Input("execute-button", "n_clicks")],
    [
        State("radio-options", "value"),
        State("parsed-data-store", "data"),
        State("num-cities", "value"),
        State("neighborhood-size", "value"),
        State("restart-threshold", "value"),
        State("max_tries", "value")
    ],
)
def update_plots(n_clicks, selected_option, uploaded_data, num_cities,
                 neighborhood_size, restart_threshold, max_tries):
    # Generate or load city data
    if selected_option == "file" and uploaded_data is not None:
        cities = uploaded_data
    elif selected_option == "random":
        cities = generate_random_points(num_cities, dim=3)  # Adjust `dim` as needed
    else:
        cities = generate_form_points(num_cities, selected_option)

    data_model = create_data_model(cities)
    distance_matrix = compute_euclidean_distance_matrix(data_model["locations"])

    # Benchmark solution
    solution_benchmark = benchmark(data_model["locations"])
    route_bench = find_route(solution_benchmark[1], solution_benchmark[2])
    benchmark_dist = calculate_route_distance(distance_matrix, route_bench)
    benchmark_distance_label = f"Distance benchmark: {benchmark_dist:5.0f} m"

    # Simulated Annealing solution
    TS_best_solution_distance = float("inf")
    TS_best_solution = tabu_search(data_model, max_iter=max_tries, neighborhood_size=neighborhood_size)
    TS_best_solution[1].append(TS_best_solution[1][0])
    TS_best_solution_distance = TS_best_solution[2]
    TS_best_route = TS_best_solution[1]

    TS_distance_label = f"Distance: {TS_best_solution_distance:5.3f} m"

    # Determine dimensionality of the data
    dimensions = len(data_model["locations"][0])
    is_3d = dimensions == 3

    # Create Plotly plots
    fig1 = go.Figure()
    fig2 = go.Figure()

    # Generate Benchmark Plot
    add_plot_traces(fig1, data_model["locations"], route_bench, is_3d)
    fig1.update_layout(
        title=f"Benchmark (Google OR): {benchmark_dist:5.3} m",
        plot_bgcolor="#333",
        paper_bgcolor="#333",
        font={"color": "white"},
        xaxis_title="X [m]",
        yaxis_title="Y [m]" if not is_3d else None,
        scene=dict(  # Add scene for 3D plots
            xaxis_title="X [m]",
            yaxis_title="Y [m]",
            zaxis_title="Z [m]",
        ) if is_3d else None,
        showlegend=False,
    )

    # Generate Simulated Annealing Plot
    add_plot_traces(fig2, data_model["locations"], TS_best_route, is_3d)
    fig2.update_layout(
        title=f"Tabus Search: {TS_best_solution_distance:5.3f} m",
        plot_bgcolor="#333",
        paper_bgcolor="#333",
        font={"color": "white"},
        xaxis_title="X [m]",
        yaxis_title="Y [m]" if not is_3d else None,
        scene=dict(
            xaxis_title="X [m]",
            yaxis_title="Y [m]",
            zaxis_title="Z [m]",
        ) if is_3d else None,
        showlegend=False,
    )

    return fig1, fig2, TS_best_solution, benchmark_distance_label, TS_distance_label


def add_plot_traces(fig, locations, route, is_3d):
    """
    Add scatter and line traces to the plot based on the dimensionality.

    :param fig: Plotly figure object to update.
    :param locations: List of 2D or 3D points.
    :param route: List of route indices.
    :param is_3d: Boolean indicating if the plot is 3D.
    """
    if is_3d:
        x_coords, y_coords, z_coords = zip(*locations)
        fig.add_trace(go.Scatter3d(
            x=x_coords, y=y_coords, z=z_coords,
            mode='markers+text',
            marker=dict(size=5, color='blue'),
            text=[str(i) for i in range(len(locations))],
            name='Nodes'
        ))
        for i in range(len(route) - 1):
            start = route[i]
            end = route[i + 1]
            fig.add_trace(go.Scatter3d(
                x=[locations[start][0], locations[end][0]],
                y=[locations[start][1], locations[end][1]],
                z=[locations[start][2], locations[end][2]],
                mode='lines',
                line=dict(color='red', width=2),
                name='Connection'
            ))
    else:
        x_coords, y_coords = zip(*locations)
        fig.add_trace(go.Scatter(
            x=x_coords, y=y_coords,
            mode='markers+text',
            marker=dict(size=5, color='blue'),
            text=[str(i) for i in range(len(locations))],
            name='Nodes'
        ))
        for i in range(len(route) - 1):
            start = route[i]
            end = route[i + 1]
            fig.add_trace(go.Scatter(
                x=[locations[start][0], locations[end][0]],
                y=[locations[start][1], locations[end][1]],
                mode='lines',
                line=dict(color='red', width=2),
                name='Connection'
            ))


@app.callback(
    Output('statistics-output', 'children'),
    Input('shared-data-store', 'data'),
)
def display_statistics(data):
    #TODO add benchmark statistics for comparison sake
    #TODO Create a table with the results for each 10 generations 
    #TODO Plot graph of the route distance progress on the side of the table
    if data is not None:
        distance = data[2]
        route = data[1]

        # Create list of HTML elements to display each line separately
        stats = [
            html.P(f"Distance: {distance:.2f} m"),
            html.P("Route:"),
        ]
        str = ""
        #TODO remove this code and make the print_route used here
        for index in range(0,len(route)):
            if index != len(route)-1:
                str+=f"{route[index]:2d} -> "
            else:
                str+=f"{route[index]:2d}"
        stats.append(html.P(str))  # Loop back to the start

        return stats
    else:
        return 'No data available.'
# Run app
if __name__ == "__main__":
    app.run_server(debug=False, port=12345)
