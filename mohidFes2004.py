# -*- coding: utf-8 -*-
from netCDF4 import Dataset
import numpy as np
from math import floor,ceil
from pyproj import Proj, transform
from scipy import interpolate
tidegauges='D:/AntarticResearch/mohid/GIS/TideInputPoints.xyz'

intide=np.loadtxt(tidegauges,comments='<')

dat=Dataset('D:/MohidModels/mohidBatteries/TideFes2004/tide.fes2004.nc')

lat=dat.variables['lat'][:]
lon=dat.variables['lon'][:]
sp=dat.variables['spectrum'][:]
fase=dat.variables['Hg'][:]
amp=dat.variables['Ha'][:]
rl=0.0000
tr=-4.0000
##### Escribir la salida
class cfile(file):
    #subclass file to have a more convienient use of writeline
    def __init__(self, name, mode = 'r'):
        self = file.__init__(self, name, mode)

    def wl(self, string):
        self.writelines(string + '\n')
        return None

out=cfile('D:/AntarticResearch/mohid/GIS/Tidedata.dat','w')
p1=Proj(init='epsg:32721')
p2=Proj(proj='latlong',datum='WGS84')
def dms(degrees = 0.0):
    if type(degrees) != 'float':
        try:
            degrees = float(degrees)
        except:
            print '\nERROR: Could not convert %s to float.' %(type(degrees))
            return 0
    minutes = abs(degrees)%1.0*60
    seconds = abs(minutes)%1.0*60
    dg=degrees
    if degrees>0:
        dg=floor(degrees)
    else:
        dg=ceil(degrees)
    return '{:3.4f} {:3.4f} {:3.4f}'.format(float(dg), float(minutes), float(seconds))

for tg in intide:
    x=tg[0]
    y=tg[1]
    loni, lati = transform(p1,p2,x,y)
    
    out.wl('<begingauge>')
    out.wl('{:13}'.format('NAME')+':'+'test')
    out.wl( '{:13}'.format('LONGITUDE')+':'+dms(loni))
    out.wl( '{:13}'.format('LATITUDE')+':'+dms(lati))
    out.wl( '{:13}'.format('METRIC_X')+':'+'{:3.4f}'.format(x))
    out.wl( '{:13}'.format('METRIC_Y')+':'+'{:3.4f}'.format(y))
    out.wl( '{:13}'.format('REF_LEVEL')+':'+'{:>10}'.format(rl))
    out.wl( '{:13}'.format('TIME_REF')+':'+'{:>10}'.format(tr))
    loni=loni+360
    for i in range(len(sp)):
        arm='-'.join(sp[i]).replace('-','')
        intp1=interpolate.RegularGridInterpolator((lat[:,0],lon[0,:]),amp[i])
        intp2=interpolate.RegularGridInterpolator((lat[:,0],lon[0,:]),fase[i])
        pts=np.array([[lati,loni]])
        z1=intp1(pts)
        z2=intp2(pts)
        out.wl( '{:13}'.format(arm)+': '+'{:3.4f} {:3.4f}'.format(z1[0],z2[0]))
    out.wl( '<endgauge>')
    out.wl( ' ')
    out.wl( ' ')
out.close()
####
##VEr: https://pyformat.info/