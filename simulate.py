import sys, os
import numpy as np, pandas as pd, geopandas as gpd
import matplotlib.pyplot as plt
import osmnx as ox, networkx as nx, rasterio
from rasterio.merge import merge
from scipy.ndimage import label
from shapely.geometry import shape
from shapely.ops import unary_union

def load_dem(path):
    with rasterio.open(path) as src:
        dem = src.read(1)
        transform, crs, nodata = src.transform, src.crs, src.nodata
    return dem, transform, crs, nodata

def assign_elevations(nodes, dem, transform, crs, nodata):
    with rasterio.io.MemoryFile() as memfile:
        with memfile.open(driver='GTiff', height=dem.shape[0], width=dem.shape[1], count=1,
                          dtype=dem.dtype, crs=crs, transform=transform, nodata=nodata) as ds:
            ds.write(dem, 1)
            elev = [val[0] for val in rasterio.sample.sample_gen(ds, [(p.x,p.y) for p in nodes.geometry])]
    nodes['elevation'] = elev
    return nodes

def run(place, dem_path):
    # Load DEM and network
    dem, transform, crs, nodata = load_dem(dem_path)
    Gd = ox.graph_from_place(place, network_type='drive')
    nodes, edges = ox.graph_to_gdfs(Gd)
    nodes = nodes.to_crs(crs)
    nodes = assign_elevations(nodes, dem, transform, crs, nodata)
    G = nx.Graph(ox.graph_from_gdfs(nodes, edges).to_undirected())

    # Sweep water levels
    wl_start, wl_end = nodes['elevation'].min()-1, nodes['elevation'].min()+10
    levels = np.linspace(wl_start, wl_end, 20)
    results = []

    for level in levels:
        flooded = nodes[nodes['elevation'] <= level].index
        Gs = G.copy(); Gs.remove_nodes_from(flooded)
        comps = sorted(nx.connected_components(Gs), key=len, reverse=True)
        lcc_size = len(comps[0]) if comps else 0
        results.append({'level': level, 'lcc_size': lcc_size, 'flooded': len(flooded)})

    df = pd.DataFrame(results)
    df.to_csv("metrics.csv", index=False)
    plt.plot(df['level'], df['lcc_size'], label='LCC size')
    plt.plot(df['level'], df['flooded'], label='Flooded nodes')
    plt.xlabel("Water level (m)"); plt.legend(); plt.grid(True)
    plt.savefig("fragmentation.png", dpi=200)
    print("Simulation finished. See metrics.csv and fragmentation.png")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python simulate.py \"PLACE NAME\" /path/to/dem.tif")
        sys.exit(1)
    run(sys.argv[1], sys.argv[2])
