import pandas as pd
import geopandas as gpd
from shapely import wkt
import matplotlib.pyplot as plt

# --- Load pickup/dropoff data ---
df_counts = pd.read_csv("sum_by_location_complete.csv", header=None)
df_counts.columns = ["year", "geometry_wkt", "departures", "arrivals"]
df_counts = df_counts[df_counts["geometry_wkt"].fillna("").str.startswith("POINT")]

# Convert to GeoDataFrame
gdf_counts = gpd.GeoDataFrame(
    df_counts,
    geometry=df_counts["geometry_wkt"].apply(wkt.loads),
    crs="EPSG:4326"
).to_crs("EPSG:3857")

# --- Load Chicago Community Areas shapefile ---
areas_df = pd.read_csv("chicago_community_areas_2025.csv")
areas_df["geometry"] = areas_df["the_geom"].apply(wkt.loads)
areas_gdf = gpd.GeoDataFrame(areas_df, geometry="geometry", crs="EPSG:4326").to_crs("EPSG:3857")
areas_summary = areas_gdf.set_index("COMMUNITY")

# --- Spatial join: assign points to communities ---
joined = gpd.sjoin(gdf_counts, areas_summary, how="inner", predicate="within")

# --- Group and join back to areas ---
summary = joined.groupby("COMMUNITY")[["departures", "arrivals"]].sum()
plot_gdf = areas_summary.join(summary, how="left").fillna(0)

# --- Choropleth plotting ---
def plot_choropleth_with_labels(gdf, column, title, cmap, filename):
    fig, ax = plt.subplots(figsize=(12, 12))
    gdf.plot(column=column, cmap=cmap, legend=True, edgecolor="white", ax=ax)

    label_map = {
        "ENGLEWOOD": "ENGLE-\nWOOD",
        "WEST ENGLEWOOD": "WEST\nENGLE-\nWOOD",
        "GRAND BOULEVARD": "GRAND\nBOULE-\nVARD",
        "BRIDGEPORT": "BRIDGE-\nPORT"
    }

    for idx, row in gdf.iterrows():
        if row[column] > 0:
            x, y = row.geometry.representative_point().coords[0]
            label = label_map.get(idx, "\n".join(idx.split()))
            ax.text(x, y, label, fontsize=5.5, ha="center", va="center", color="black")

    ax.set_title(title, fontsize=14)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(f"plots/{filename}")
    plt.close()

# --- Difference Map ---
def plot_difference_map_with_labels(gdf, col1="departures", col2="arrivals", title="Pickup vs Dropoff Balance", filename="diff_map.png"):
    gdf["diff"] = gdf[col1] - gdf[col2]
    vmax = max(abs(gdf["diff"].max()), abs(gdf["diff"].min()), 2000)

    fig, ax = plt.subplots(figsize=(12, 12))
    gdf.plot(column="diff", cmap="bwr", legend=True, edgecolor="white",
             vmin=-vmax, vmax=vmax, ax=ax)

    label_map = {
        "ENGLEWOOD": "ENGLE-\nWOOD",
        "WEST ENGLEWOOD": "WEST\nENGLE-\nWOOD",
        "GRAND BOULEVARD": "GRAND\nBOULE-\nVARD",
        "BRIDGEPORT": "BRIDGE-\nPORT"
    }

    for idx, row in gdf.iterrows():
        if row["diff"] != 0:
            x, y = row.geometry.representative_point().coords[0]
            label = label_map.get(idx, "\n".join(idx.split()))
            ax.text(x, y, label, fontsize=5.5, ha="center", va="center", color="black")

    ax.set_title(title, fontsize=14)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(f"plots/{filename}")
    plt.close()

# --- Run Plots ---
plot_choropleth_with_labels(plot_gdf, "departures", "Pickups by Community Area", cmap="YlGnBu", filename="choropleth_departures.png")
plot_choropleth_with_labels(plot_gdf, "arrivals", "Dropoffs by Community Area", cmap="YlGnBu", filename="choropleth_arrivals.png")
plot_difference_map_with_labels(plot_gdf, filename="choropleth_diff.png")
