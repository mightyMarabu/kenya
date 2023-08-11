from nicegui import events, ui

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
import sqlite3


# Download data and set working directory
#data = et.data.get_data('cold-springs-fire')
#os.chdir(os.path.join(et.io.HOME,
#                      'satData'))

def handle_upload(e: events.UploadEventArguments):
    aoi = gpd.read_file(e.content)
    print (e.name)
    layername = (e.name).split('.')[0]
    #conn = sqlite3.connect('app.sqlite')
    #aoi.to_sql('aoi', conn, if_exists='replace', index=False, dtype={'geometry': 'GEOMETRY'})
    aoi.to_file('/home/sebastian/apps/kenya/app.sqlite', driver='SQLite', spatialite=True, layer=layername)
    #conn.commit()
    #conn.close()

def uploadAOI():
    ui.upload(on_upload=handle_upload).props('accept=.gpkg').classes('max-w-full')
def uploadband():
    ui.upload(on_upload=handle_upload).props('accept=.jp2').classes('max-w-full')
