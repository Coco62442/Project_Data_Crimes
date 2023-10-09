#Imports
import geoviews as gv
import geoviews.feature as gf
import geopandas as gpd
import numpy as np
from geoviews import dim
sf = gpd.read_file('../originalData/departements-version-simplifiee.geojson')


sf['value'] = np.random.randint(1, 10, sf.shape[0])
deps = gv.Polygons(sf, vdims=['nom','value'])
deps.opts(width=600, height=600, toolbar='above', color=dim('value'), colorbar=True, tools=['hover'], aspect='equal')