import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import dash_bootstrap_components as dbc  
from SA_implemented import simulated_annealing
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
                        dcc.Graph(id="plot1"),
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
                    style={"width": "49%", "backgroundColor": "#333", "padding": "10px", "borderRadius": "10px"},
                ),
                # Plot 2 with total distance label
                html.Div(
                    children=[
                        dcc.Graph(id="plot2"),
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
                    style={"width": "49%", "backgroundColor": "#333", "padding": "10px", "borderRadius": "10px"},
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
                                # Population Size
                                html.Div(
                                    children=[
                                        html.Label(
                                            "initial_temperature:",
                                            style={
                                                "color": "white",
                                                "fontSize": "20px",
                                                "marginBottom": "8px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="initial-temperature",
                                            type="number",
                                            value=10000000,
                                            style={"width": "100%", "padding": "8px", "borderRadius": "5px"},
                                        ),
                                    ],
                                    style={"textAlign": "left"},
                                ),
                                # Number of Generations
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
                                            value=100,
                                            style={"width": "100%", "padding": "8px", "borderRadius": "5px"},
                                        ),
                                    ],
                                    style={"textAlign": "left"},
                                ),
                                # Mutation Rate
                                html.Div(
                                    children=[
                                        html.Label(
                                            "min_temperature:",
                                            style={
                                                "color": "white",
                                                "fontSize": "20px",
                                                "marginBottom": "8px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="min-temperature",
                                            type="number",
                                            value=1,
                                            step=1,
                                            style={"width": "100%", "padding": "8px", "borderRadius": "5px"},
                                        ),
                                    ],
                                    style={"textAlign": "left"},
                                ),
                                # Tournament Size
                                html.Div(
                                    children=[
                                        html.Label(
                                            "cooling_rate:",
                                            style={
                                                "color": "white",
                                                "fontSize": "20px",
                                                "marginBottom": "8px",
                                            },
                                        ),
                                        dcc.Input(
                                            id="cooling-rate",
                                            type="number",
                                            value=3,
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
                                            value=1,
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
    [Output("plot1", "figure"), Output("plot2", "figure"),  Output('shared-data-store', 'data'),
     Output("total-distance-label-plot1","children"), Output("total-distance-label-plot2","children")],
    [Input("execute-button", "n_clicks")],
    [
        State("radio-options", "value"),
        State("parsed-data-store", "data"),
        State("num-cities", "value"),
        State("initial-temperature", "value"),
        State("neighborhood-size", "value"),
        State("min-temperature", "value"),
        State("cooling-rate", "value"),
        State("restart-threshold", "value"),
        State("max_tries", "value")
    ],
)
def update_plots(n_clicks, selected_option, uploaded_data, num_cities, initial_temperature,
                 neighborhood_size, min_temperature, cooling_rate, restart_threshold, max_tries ):
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
    str1 = f"Distance benchmark: {benchmark_dist:5.0f} m"
    print(str1)
    print("Route Benchmark:\n\t",end = "")
    print_route(route_bench)
    distance = 2*benchmark_dist
    tries = 0 
    print("################# Custom Simulated Annealing Solution #################")
    SA_best_solution_distance = distance
    SA_best_solution = None
    SA_best_route = None
    while (distance > benchmark_dist) and (tries < max_tries):
        solution_SA = simulated_annealing(distance_matrix = distance_matrix, initial_temperature=initial_temperature, 
                                          cooling_rate=cooling_rate,restart_threshold=restart_threshold,min_temperature = min_temperature,
                                          neighborhood_size=neighborhood_size)
        distance = solution_SA[1]
        str2 = f"Distance: {solution_SA[1]:5.0f} m"
        print(str2)
        route_SA = solution_SA[0]
        print("Route SA:\n\t",end = "")
        print_route(route_SA)
        if(distance < SA_best_solution_distance):
            SA_best_solution_distance = distance
            SA_best_solution = solution_SA
            SA_best_route = route_SA
        tries+=1
    
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
        title=f"Benchmark (Google OR), using {selected_option} data: {benchmark_dist:5.0f} m",
        plot_bgcolor="#333",
        paper_bgcolor="#333",
        font={"color": "white"},
        xaxis_title="X [m]",
        yaxis_title="Y [m]",
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
    for i in range(len(SA_best_route) - 1):
        start_index = SA_best_route[i]
        end_index = SA_best_route[i + 1]
        fig2.add_trace(go.Scatter(
            x=[locations[start_index][0], locations[end_index][0]],
            y=[locations[start_index][1], locations[end_index][1]],
            mode='lines',
            line=dict(color='red', width=2),
            name='Connection'
        ))

    # Update layout for fig2
    fig2.update_layout(
        title=f"SA Implemented, using {selected_option} data: : {SA_best_solution_distance:5.0f} m",
        plot_bgcolor="#333",
        paper_bgcolor="#333",
        font={"color": "white"},
        xaxis_title="X [m]",
        yaxis_title="Y [m]",
        showlegend=False,
    )
    return (fig1, fig2, SA_best_solution, str1, str2)


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
    app.run_server(debug=False)
