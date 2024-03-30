#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 14:38:08 2021

@author: wrenteria
Download DEM from NCEI repository
https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ngdc.mgg.dem:724/html
Check vertical datum and spatial resolution
Usefull to get the raster data required on GEOCLAW model
"""

import xarray as xa
import matplotlib.pyplot as plt

# the file where you want to save your data
path='./clawpack/geoclaw/scratch/'

dap_url="https://www.ngdc.noaa.gov/thredds/dodsC/regional/crescent_city_13_navd88_2010.nc"


data = xa.open_dataset(dap_url)
topo=data['Band1'].sel(lat=slice(41.715,41.770), lon=slice(-124.258,-124.150))
x_len = len(topo.lon.values)
y_len = len(topo.lat.values)

# Write the name for your file
fout=open(path+"crescent.asc",'w')

fout.write("%i ncols\n"%(x_len))
fout.write("%i nrows\n"%(y_len))
fout.write("%3.1f xll\n"%(topo.lon.values[0]))
fout.write("%3.1f yll\n"%(topo.lat.values[0]))
fout.write("%3.4f cellsize\n"%(0.00009259259))
fout.write("%i nodata_value\n"%(999999))

for j in range(y_len):
    for i in range(x_len):
        #print (etp0.z.values[j,i])
        fout.write("%3.1f\n"%(topo.data[-j,i]+1.013))

fout.close()
plt.pcolor(topo.data)
plt.colorbar()
plt.show()
