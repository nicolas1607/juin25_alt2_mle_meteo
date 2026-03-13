import folium
from branca.colormap import LinearColormap

location_coords = {
    'Albury': (-36.0737, 146.9135),
    'BadgerysCreek': (-33.8817, 150.7443),
    'Cobar': (-31.4949, 145.8402),
    'CoffsHarbour': (-30.2963, 153.1135),
    'Moree': (-29.4658, 149.8407),
    'Newcastle': (-32.9283, 151.7817),
    'NorahHead': (-33.2817, 151.5677),
    'NorfolkIsland': (-29.0333, 167.9500),
    'Penrith': (-33.7507, 150.6942),
    'Richmond': (-33.5996, 150.7515),
    'Sydney': (-33.8688, 151.2093),
    'SydneyAirport': (-33.9399, 151.1753),
    'WaggaWagga': (-35.1082, 147.3598),
    'Williamtown': (-32.7932, 151.8360),
    'Wollongong': (-34.4278, 150.8931),
    'Canberra': (-35.2809, 149.1300),
    'Tuggeranong': (-35.4244, 149.0888),
    'MountGinini': (-35.5294, 148.7723),
    'Ballarat': (-37.5622, 143.8503),
    'Bendigo': (-36.7570, 144.2794),
    'Sale': (-38.1026, 147.0657),
    'MelbourneAirport': (-37.6690, 144.8410),
    'Melbourne': (-37.8136, 144.9631),
    'Mildura': (-34.2080, 142.1246),
    'Nhil': (-36.3328, 141.6503),
    'Portland': (-38.3463, 141.6042),
    'Watsonia': (-37.7121, 145.0827),
    'Dartmoor': (-37.9144, 141.2730),
    'Brisbane': (-27.4705, 153.0260),
    'Cairns': (-16.9186, 145.7781),
    'GoldCoast': (-28.0167, 153.4000),
    'Townsville': (-19.2590, 146.8169),
    'Adelaide': (-34.9285, 138.6007),
    'MountGambier': (-37.8284, 140.7804),
    'Nuriootpa': (-34.4693, 138.9973),
    'Woomera': (-31.1998, 136.8254),
    'Albany': (-35.0275, 117.8840),
    'Witchcliffe': (-34.0261, 115.1005),
    'PearceRAAF': (-31.6676, 116.0290),
    'PerthAirport': (-31.9403, 115.9668),
    'Perth': (-31.9505, 115.8605),
    'SalmonGums': (-32.9815, 121.6438),
    'Walpole': (-34.9777, 116.7338),
    'Hobart': (-42.8821, 147.3272),
    'Launceston': (-41.4332, 147.1441),
    'AliceSprings': (-23.6980, 133.8807),
    'Darwin': (-12.4634, 130.8456),
    'Katherine': (-14.4652, 132.2635),
    'Uluru': (-25.3444, 131.0369)
}

def create_numerical_map(df, location, num_data):
    """
    Creates a Folium map visualizing numerical data for different locations.

    Args:
        df (pd.DataFrame): The dataframe containing the data.
        location (str or None): The column name for location. If None, the index is used.
        num_data (str): The column name for numerical data.

    Returns:
        folium.Map: The generated map.
    """
    # Create a base map centered on Australia
    m = folium.Map(location=[-25.2744, 133.7751], zoom_start=4)

    # Create a linear colormap from red to green based on the data range
    # We'll use the min and max data from our analysis for the scale
    min_val = df[num_data].min()
    max_val = df[num_data].max()
    colormap = LinearColormap(['blue', 'green', 'red'], vmin=min_val, vmax=max_val)
    colormap.caption = f'{num_data} Value'

    # Add markers for each location in df that exists in location_coords
    for index, row in df.iterrows():
        # Determine location name: use column if provided, else use index
        loc_name = row[location] if location else index

        if loc_name in location_coords:
            coords = location_coords[loc_name]
            val = row[num_data]

            # Get hex color from colormap
            hex_color = colormap(val)

            # Create popup text
            popup_text = f"""
            <b>Location:</b> {loc_name}<br>
            <b>{num_data}:</b> {val:.2f}
            """

            # Use CircleMarker for better gradient visualization
            folium.CircleMarker(
                location=coords,
                radius=10,
                popup=folium.Popup(popup_text, max_width=300),
                color='black',
                weight=1,
                fill=True,
                fill_color=hex_color,
                fill_opacity=0.8,
                tooltip=loc_name
            ).add_to(m)

    # Add the colormap legend to the map
    m.add_child(colormap)

    # Return the map
    return m
