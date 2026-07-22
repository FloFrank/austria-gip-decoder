import os
import requests
import traceback
import zipfile
import sys
import pandas as pd
import geopandas as gpd


#Define URLs and paths
url = "https://open.gip.gv.at/ogd/B_gip_network_ogd.zip"  
zipname = "gip_network_ogd.zip"

if not os.path.exists("gip_network_ogd.gpkg"):
    print("Downloading …")
    print(f"URL: {url}")
    print(f"Target location: {os.path.abspath(zipname)}")
    
    download_successful = False
    
    try:
        response = requests.get(url, timeout=600, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        print(f"Download size: {total_size / 1024 / 1024:.2f} MB")
        
        with open(zipname, 'wb') as f:
            downloaded = 0
            last_progress = 0
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = int((downloaded / total_size) * 100)
                        if progress > last_progress:
                            sys.stdout.write(f"\r  Progress: {progress}%  ")
                            sys.stdout.flush()
                            last_progress = progress
        print(f"\nDownload complete. File: {os.path.abspath(zipname)}")
        download_successful = True
        
    except Exception as e:
        print(f"\nError downloading: {e}")
        traceback.print_exc()
    
    # Extraktion nur wenn Download erfolgreich war
    if download_successful and os.path.exists(zipname):
        print("Extracting ...")
        try:
            with zipfile.ZipFile(zipname, 'r') as zip_ref:
                zip_ref.extractall()
            os.remove(zipname)
            print("Extraction complete")
        except Exception as e:
            print(f"Error extracting: {e}")
            traceback.print_exc()
    else:
        print("Download file does not exist")

else:
    print("gip_network_ogd.gpkg already exists")


# LINK layer extraction
print("\n--- LINK layer is being extracted ---")
try:
    gpkg_file = "gip_network_ogd.gpkg"
    if os.path.exists(gpkg_file):
        print(f"Reading {gpkg_file}...")
        link_gdf = gpd.read_file(gpkg_file, layer="LINK")
        
        print(f"LINK layer loaded: {len(link_gdf)} features")
        print(f"Columns: {list(link_gdf.columns)}")
        
        # Optional: Save as new GeoPackage
        output_file = "LINK.gpkg"
        link_gdf.to_file(output_file, driver="GPKG")
        print(f"=== extraction complete ===: {output_file}")
        
        # Delete the geopackage after extraction
        os.remove(gpkg_file)
        print(f"GeoPackage deleted: {gpkg_file}")
        
    else:
        print("gip_network_ogd.gpkg not found")
        
except Exception as e:
    print(f"Error extracting: {e}")
    traceback.print_exc()


print("\n--- Calculate bitmask ---")

### Read extracted shapefile 
gip_link = gpd.read_file("LINK.gpkg", layer="LINK")

#Convert access_tow and access_bkw to integer (nullable Int64 to support NaN values)
gip_link['access_tow'] = gip_link['access_tow'].astype('Int64')
gip_link['access_bkw'] = gip_link['access_bkw'].astype('Int64')

# List columns
#print(gip_link.columns.tolist())
#>>> print(gip_link.columns.tolist())
#['object_id', 'short_id', 'node_from_', 'node_fro_1', 'node_to_id', 'node_to_sh', 'edge_id', 'edge_short', 'name_text_', 
# 'short_name', 'name_tex_1', 'speed_tow_', 'speed_bkw_', 'maxspeed_t', 'maxspeed_b', 'access_tow', 'access_bkw', 'length', 
# 'functional', 'lanes_tow_', 'lanes_to_1', 'lanes_bkw_', 'lanes_bk_1', 'form_of_wa', 'abutter_ca', 'urban', 'level_inte', 
# 'constructi', 'toll', 'subnet', 'edge_categ', 'sustainer', 'regional_c', 'connector', 'max_width', 'max_height', 'max_weight',
#  'owner', 'oneway_car', 'oneway_ped', 'oneway_bik', 'oneway_bus', 'geometry']


#Function to convert integer to 22-bit binary string
def convert_to_bitmask(value):
    # Handle NaN/NA values
    if pd.isna(value):
        return "0" * 22
    
    # Convert to int (if float or Int64)
    value = int(value)
    
    # Convert integer to binary (without '0b' prefix)
    binary = bin(value)[2:] if value > 0 else "0"
    # Pad with zeros to 22 places (left)
    return binary.zfill(22)


#Convert access_tow to bitmask
gip_link['bit_tow'] = gip_link['access_tow'].apply(convert_to_bitmask)

#Convert access_bkw to bitmask
gip_link['bit_bkw'] = gip_link['access_bkw'].apply(convert_to_bitmask)


#Split bits for TOW (direction)
bit_labels = ['garbage_tow', 'hazard_tow', 'comb_tow', 'camper_tow', 'cferry_tow', 
              'crailway_tow', 'rrailway_tow', 'mcycle_tow', 'trolly_tow', 'coach_tow',
              'truck16_tow', 'taxi_tow', 'truck75_tow', 'truck35_tow', 'ferry_tow',
              'subway_tow', 'tram_tow', 'railway_tow', 'bus_tow', 'car_tow',
              'bike_tow', 'walk_tow']

for i, label in enumerate(bit_labels):
    gip_link[label] = gip_link['bit_tow'].str[i]


#Split bits for BKW (backward direction)
bit_labels_bkw = ['garbage_bkw', 'hazard_bkw', 'comb_bkw', 'camper_bkw', 'cferry_bkw',
                  'crailway_bkw', 'rrailway_bkw', 'mcycle_bkw', 'trolly_bkw', 'coach_bkw',
                  'truck16_bkw', 'taxi_bkw', 'truck75_bkw', 'truck35_bkw', 'ferry_bkw',
                  'subway_bkw', 'tram_bkw', 'railway_bkw', 'bus_bkw', 'car_bkw',
                  'bike_bkw', 'walk_bkw']

for i, label in enumerate(bit_labels_bkw):
    gip_link[label] = gip_link['bit_bkw'].str[i]

print("Bitmask conversion completed")

#Save the modified GeoDataFrame as LINK.gpkg
output_file = "LINK.gpkg"
if os.path.exists(output_file):
    os.remove(output_file)
gip_link.to_file(output_file, driver="GPKG", layer="LINK")
print("LINK.gpkg saved successfully")


gip_link = gpd.read_file("LINK.gpkg", layer="LINK")
print("Completed: LINK.gpkg has been read back successfully")