from nicegui import events, ui

import os
from glob import glob

import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio as rio
from rasterio.transform import from_origin
import xarray as xr
import rioxarray as rxr
import numpy as np
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
from shapely.geometry import mapping
import sqlite3
import cv2

import processData


# Download data and set working directory
#data = et.data.get_data('cold-springs-fire')
#os.chdir(os.path.join(et.io.HOME,
#                      'satData'))

def handle_upload(e: events.UploadEventArguments):
    aoi = gpd.read_file(e.content)
    print(e.name)
    layername = (e.name).split('.')[0]
    #conn = sqlite3.connect('app.sqlite')
    #aoi.to_sql('aoi', conn, if_exists='replace', index=False, dtype={'geometry': 'GEOMETRY'})

    #aoi.to_file('/home/sebastian/apps/kenya/vector/'+e.name, driver='GeoJSON', layer=layername)
    #conn.commit()
    #conn.close()
    
def storeBands(e: events.UploadEventArguments):
    print(e.name)
    e.content.seek(0)
    content_bytes = e.content.read()

    # Decode the image using cv2.imdecode
    satBand = cv2.imdecode(np.frombuffer(content_bytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    if satBand is not None:
        # Create a temporary GeoTIFF file to store the image
        with NamedTemporaryFile(suffix='.tif', delete=False) as temp_file:
            # Adjust these parameters as needed
            width, height = satBand.shape[1], satBand.shape[0]
            pixel_width = 1.0
            pixel_height = 1.0
            transform = from_origin(0, 0, pixel_width, pixel_height)

            # Use rasterio to write the image data to the temporary GeoTIFF file
            with rasterio.open(temp_file.name, 'w', driver='GTiff', width=width, height=height, count=1, dtype=satBand.dtype, crs='EPSG:4326', transform=transform) as dst:
                dst.write(satBand, 1)

            # Now, you can use rasterio to read the temporary GeoTIFF file if needed
            with rasterio.open(temp_file.name, 'r') as src:
                # Perform any desired operations with the image data
                image_data = src.read(1)  # Read the image data

        # Delete the temporary GeoTIFF file after use
        os.remove(temp_file.name)

        print("Image data loaded and processed.")
    else:
        print("Failed to decode the image content")
####################################################################################################################

# Connect to the SQLite database
conn = sqlite3.connect('app.sqlite')
cursor = conn.cursor()

# Execute a SQL query
def getDBdata(tablename):
    conn = sqlite3.connect('app.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM '+tablename)
    # Fetch the results
    results = cursor.fetchall()
    # Close the database connection
    conn.close()
    return results

def uploadGeoJSON(e: events.UploadEventArguments):
    conn = sqlite3.connect('app.sqlite')
    cursor = conn.cursor()
    # Read the GeoJSON file
    # with open(e.content, 'r') as geojson_file:
    #     geojson_data = geojson_file.read()
    geojson_data = e.content.read()
    # Execute an SQL command to insert the GeoJSON data into the database
    cursor.execute("INSERT INTO aoi (name, geojson) VALUES (?,?)", (e.name, geojson_data,))
    # Commit the transaction and close the database connection
    conn.commit()
    conn.close()

####################################################################################################################
#def uploadAOI():
#    ui.upload(on_upload=uploadGeoJSON).props('accept=.geojson, .json').classes('max-w-full')
def uploadAOI():
    ui.upload(on_upload=uploadGeoJSON).props('accept=.geojson, .json').classes('max-w-full')
def uploadBand():
    ui.upload(on_upload=storeBands).props('accept=.jp2').classes('max-w-full')

