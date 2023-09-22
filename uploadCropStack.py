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
    aoi.to_file('/home/sebastian/apps/kenya/app.sqlite', driver='SQLite', spatialite=True, layer=layername)
    aoi.to_file('/home/sebastian/apps/kenya/vector/'+e.name, driver='GPKG', layer=layername)
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

def uploadAOI():
    ui.upload(on_upload=handle_upload).props('accept=.gpkg').classes('max-w-full')
def uploadBand():
    ui.upload(on_upload=storeBands).props('accept=.jp2').classes('max-w-full')

## process data

import os
from glob import glob

import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio as rio
import xarray as xr
import rioxarray as rxr
import numpy as np
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
from shapely.geometry import mapping

def open_clean_band(band_path, clip_extent, valid_range=None):
    try:
        clip_bound = clip_extent.geometry
    except Exception as err:
        print("Oops, I need a geodataframe object for this to work.")
        print(err)

    cleaned_band = rxr.open_rasterio(band_path,
                                     masked=True).rio.clip(clip_bound,
                                                           from_disk=True).squeeze()

    # Only mask the data if a valid range tuple is provided
    if valid_range:
        mask = ((sentinel_xr_clip < valid_range[0]) | (
            sentinel_xr_clip > valid_range[1]))
        cleaned_band = sentinel_post_xr_clip.where(
            ~xr.where(mask, True, False))

    return cleaned_band

def process_bands(paths, crop_layer, stack=False):
    all_bands = []
    for i, aband in enumerate(paths):
        cleaned = open_clean_band(aband, crop_layer)
        #cleaned["band"] = i+1
        #cleaned.rio.to_raster(
        #    "/home/jovyan/results/bands_cropped/"+str(i)+"cropped_to_aoi.tiff",
        #    tiled=True,  # GDAL: By default striped TIFF files are created. This option can be used to force creation of tiled TIFF files.
        #    windowed=True,  # rioxarray: read & write one window at a time
        #)
        all_bands.append(cleaned)

    if stack:
        print("I'm stacking your data now.")
        allBandStack = xr.concat(all_bands, dim="band")
        
        #with rio.open(paths[0]) as src:
        #    meta = src.meta
        #with rio.open('/home/jovyan/results/bands_cropped/allbands_croppped.tiff', 'w', **meta) as dst:
        #    dst.write(arr_st, indexes=4)
                
        return allBandStack
    else:
        print("Returning a list of xarray objects.")
        return all_bands
    
def loadSatData(satFolder):
    sentinel_data_path = os.path.join("/home/jovyan/",
                                          "satData/",
                                          satFolder+"/"
                                      )
    
    glob(os.path.join(sentinel_data_path, "*"))
    
    all_sentinel_bands = glob(os.path.join(sentinel_data_path,
                                              "*B*.jp2"))
                                            # "*TCI*.jp2"))
    all_sentinel_bands.sort()
    return all_sentinel_bands

def loadSatData(satFolder):
    sentinel_data_path = os.path.join("/home/jovyan/",
                                          "satData/",
                                          satFolder+"/"
                                      )
    
    glob(os.path.join(sentinel_data_path, "*"))
    
    all_sentinel_bands = glob(os.path.join(sentinel_data_path,
                                              "*B*.jp2"))
                                            # "*TCI*.jp2"))
    all_sentinel_bands.sort()
    return all_sentinel_bands

def loadAOI(aoi):
    # Open up boundary extent using GeoPandas
    #aoi_boundary_path = os.path.join("aoi.gpkg")
    aoi_boundary_path = os.path.join("/home/jovyan/",
                                     "vector_data/",
                                     aoi)
    aoi_boundary = gpd.read_file(aoi_boundary_path)
    return aoi_boundary

def reprojectCRS(all_sentinel_bands, aoi):
    # Get a list of required bands - bands 2 through 5
    #all_sentinel_bands
    # Get CRS of landsat data and reproject fire boundary
    # Reproject your vector layer
    crs_sat = es.crs_check(all_sentinel_bands[0])
    aoi_boundary = loadAOI(aoi)
    crs_aoi = aoi_boundary.crs
    
    # Reproject aoi boundary for clipping
    aoi_reprojected = aoi_boundary.to_crs(crs_sat)
    return aoi_reprojected

def performCropping(sat, aoi):
    all_sentinel_bands = loadSatData("wiz")
    aoi_reprojected = reprojectCRS(all_sentinel_bands, "wiz.gpkg")
    
    processed_stack = process_bands(all_sentinel_bands, 
                                    aoi_reprojected, 
                                    stack=True)
    print(processed_stack.shape)
    return processed_stack