import sqlite3

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