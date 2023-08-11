# sentinel 2 imgae clustering classification

import rasterio as rio
from rasterio.plot import show
from sklearn import cluster
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import numpy as np

# Open the image 
rasterImage = rio.open("./satData/copped/....tiff")

print(rasterImage.meta)