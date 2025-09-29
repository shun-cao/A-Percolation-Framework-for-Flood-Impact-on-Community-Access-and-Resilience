# Flood Resilience Percolation Simulator

A clean, reproducible Python toolkit to study how incremental flooding (by water level) fragments an urban road network and degrades accessibility.

- **Inputs:** OpenStreetMap roads (via `osmnx`) and one or more local DEM GeoTIFFs for elevation.
- **Outputs:** CSV of simulation metrics and publication-quality figures.
- **Scope:** Node-percolation by water level (remove nodes below or equal to the level). Edge-percolation and very advanced diagnostics are optional and off by default to keep runs simple and fast.

> This repository is a streamlined, documented rework of an internal script, trimmed to remove ad‑hoc references, machine-specific paths, and exploratory extras so paper readers can repeat the study or run a new area with minimal friction.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run simulation:
   ```bash
   python simulate.py "Broome County, NY, USA" /path/to/dem.tif
   ```

3. Output:
   - metrics.csv
   - fragmentation.png


## Quick Start

1. **Create a Python env** (conda recommended):
   ```bash
   conda create -n floodres python=3.11 -y
   conda activate floodres
   pip install -r requirements.txt
   ```

2. **Prepare a config** (copy and edit `config.example.yaml`):
   ```bash
   cp config.example.yaml config.yaml
   ```

3. **Run**:
   ```bash
   python -m scripts.run_simulation --config config.yaml
   ```

4. **Results** will be written into a new timestamped folder under `runs/`:
   - `metrics.csv`: all time series metrics by water level
   - `fig_fragmentation.png`: fragmentation dynamics
   - `fig_efficiency.png`: efficiency & path-based metrics
   - `fig_damage_population.png`: infrastructure & population proxy
   - (optional) `fig_facility_*` if facility tags exist in your AOI

## Configure a New Area

Edit `config.yaml`:
- `place_name`: any place resolvable by OSM (e.g., `Broome County, NY, USA` or `West University Place, Texas, USA`)
- `elevation_rasters`: list of paths to your DEM GeoTIFFs covering the AOI. (Use USGS 1/3 arc-second, 10 m DEM tiles you download locally.)
- `water_level`: start, end, and steps (meters).
- `facilities`: amenity/shop tags to pull (optional).
- `skip_expensive`: set `true` to speed up by skipping heavy metrics.

## Notes

- All figures are designed with white background, large fonts, and clear legends for direct use in papers.
- The code avoids machine-specific paths and uses only local raster inputs; OSM downloading happens at runtime.
- For deterministic sampling and reproducibility, random seeds are fixed where applicable.

## Citation

If you adapt this code for your publication, please include a citation or link to the repository.
