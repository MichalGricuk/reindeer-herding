import osmnx as ox
import geopandas as gpd
from typing import Optional

def get_osm_roads(gdf_geometry: gpd.GeoDataFrame, output_file: Optional[str] = None) -> gpd.GeoDataFrame:
    """
    Scrapes all roads from OpenStreetMap within a given polygon and saves them as a .gpkg file.

    Args:
        gdf_geometry: The geometry of the are of interest.
        output_file: Path to the output .gpkg file.

    Returns:
        None
    """
    # Ensure the GeoDataFrame contains a single polygon geometry
    if gdf_geometry.empty or not gdf_geometry.geometry.iloc[0].is_valid:
        raise ValueError("The GeoDataFrame must contain a valid polygon geometry.")

    # Extract the polygon geometry
    polygon = gdf_geometry.geometry.iloc[0]

    # Download road network data within the polygon
    road_network = ox.graph_from_polygon(polygon, network_type='all')

    # Convert the road network to a GeoDataFrame
    gdf_road = ox.graph_to_gdfs(road_network, nodes=False, edges=True)

    # Save the GeoDataFrame to a GeoPackage file
    if output_file:
        gdf_road.to_file(output_file, driver="GPKG")
        print(f"Road data saved to {output_file}")
    
    return gdf_road