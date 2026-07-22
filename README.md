## austria-gip-decoder

Decodes access permissions from Austria GIP (Geographisches Informationssystem) road network dataset


[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Library-Pandas-blue)](https://pandas.pydata.org/)
[![GeoPandas](https://img.shields.io/badge/Library-GeoPandas-blue)](https://geopandas.org/)
[![GIP](https://img.shields.io/badge/Data%20Source-Austria%20GIP-green)](https://www.gip.gv.at/)
[![License](https://img.shields.io/badge/License-CC0-red)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen)](https://github.com)


## Description
The Graph Integration Platform (GIP) is the intermodal Geographic Information System of public administration for Austria's road network. It represents this as a reference graph in standardized digital form.

GIP is freely available as an Open Data download and is provided in GeoPackage format. The GeoPackage layer LINKNETZ contains the geometries of road center lines as GIP-Links, which form a routable network – at intersections, the geometries are accordingly subdivided.

The attribute "ACCESS_TOW" encodes traversability in digitization direction as a bitmask, while "ACCESS_BKW" encodes traversability against the digitization direction.

Example: The decimal value 2383631 means in binary:

Bits 0–3 are set: pedestrians, cyclists, cars, and buses are allowed
Bits 4–7 are not set: trains, trams, subways, and waterborne traffic are not allowed
Bits from position 8 onwards are set by automated rules but are not maintained in GIP and are therefore not relevant – exception: taxi traversability, which is fully mapped in Vienna

This project creates from the decimal values of the attributes "ACCESS_TOW" and "ACCESS_BKW" a bitmask that represents the different modes of transport in digitization direction and against it.


## Project Structure

### Data Files
- `Intermodales Verkehrsreferenzsystem Österreich (GIP.at) Österreich` 


### Code
- `gip_decoder.py` main python script 

## Requirements
- Python 3.8 or higher
- GDAL/OGR libraries (for GeoPackage support)
- RAM: 8-16 GB (for full dataset processing)

### Python Dependencies
```bash
pip install pandas geopandas requests
```

Or individually:
```bash
pip install pandas
pip install geopandas
pip install requests
```


## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/FloFrank/austria-gip-decoder.git
cd austria-gip-decoder
```

2. **Create a virtual environment (optional but recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install pandas geopandas requests
```

4. **Run the decoder:**
```bash
python gip_decoder.py
```


## Features

- **Automatic Download**: Downloads the latest GIP dataset from Austria's open data portal
- **Bitmask Conversion**: Converts decimal ACCESS_TOW and ACCESS_BKW values to 22-bit binary masks
- **Transport Mode Extraction**: Automatically splits bitmasks into individual transport mode permissions:
  - Pedestrians, cyclists, motorcycles
  - Cars, buses, taxis, coaches
  - Trains, trams, subways
  - Ferries, trolleys
  - Emergency and hazmat vehicles
- **GeoPackage Output**: Saves results in GeoPackage format for geographic information systems
- **Spatial Data Preservation**: Maintains geometry information for mapping and spatial analysis


## Usage

The script performs the following workflow:

1. **Downloads** the GIP network dataset (if not already present)
2. **Extracts** the LINK layer from the GeoPackage
3. **Converts** ACCESS_TOW and ACCESS_BKW decimal values to binary bitmasks
4. **Decodes** each bit into transport mode columns
5. **Saves** the enriched dataset as `LINK.gpkg`

### Output Files
- `LINK.gpkg` – GeoPackage containing the decoded access permissions with 44 columns (22 for TOW direction, 22 for BKW direction)


## Output

The script generates a new GeoPackage (`LINK.gpkg`) with the following decoded columns:

### Forward Direction (TOW - Toward/Digitization Direction)
- `walk_tow`, `bike_tow`, `car_tow`, `bus_tow`, `taxi_tow`, `truck16_tow`, `truck35_tow`, `truck75_tow`
- `coach_tow`, `ferry_tow`, `subway_tow`, `tram_tow`, `railway_tow`
- `hazard_tow`, `garbage_tow`, `camper_tow`, `cferry_tow`, `crailway_tow`, `rrailway_tow`, `mcycle_tow`, `trolly_tow`, `comb_tow`

### Backward Direction (BKW - Against Digitization Direction)
- Same 22 columns as TOW but with `_bkw` suffix

Each cell contains `"0"` (not permitted) or `"1"` (permitted) for that transport mode.


## Data Source

Data is automatically downloaded from:
- **Austria Open Data Portal**: https://www.gip.gv.at/
- **Dataset**: Intermodales Verkehrsreferenzsystem Österreich (GIP)
- **Format**: GeoPackage (.gpkg)
- **License**: CC0 (Public Domain)



## License

This project is licensed under the **CC0 1.0 Universal (CC0 1.0) Public Domain Dedication**.

The GIP dataset is provided by Austria's public administration and is freely available under CC0.



## Author

Florian Frank

For questions or contributions, please contact via GitHub issues.


## References

- [GIP Official Website](https://www.gip.gv.at/)
- [Austria Open Data Portal](https://www.data.gv.at/datasets/3fefc838-791d-4dde-975b-a4131a54e7c5?locale=de)
- [Documentation GIP](https://www.gip.gv.at/assets/downloads/2509_dokumentation_gipat_ogd.pdf)
- [GeoPandas Documentation](https://geopandas.org/)
- [Pandas Documentation](https://pandas.pydata.org/)





