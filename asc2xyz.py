"""
Script to convert from ASCII Raster Format to XYZ format (Mohid Model)
@wrenteria
30/11/2017
"""
inputfile='Raster.asc'
outputfile='Output.xyz'
#If bathymetry data is positive change  Line 14
#If longitude data is -180 +180, change Line 17
import numpy as np
par=open(inputfile)
dat=np.loadtxt(inputfile,skiprows=6)
out=open(outputfile,'w')
dat=dat*-1
nc=int(par.readline().split()[1])
nr=int(par.readline().split()[1])
xl=float(par.readline().split()[1])-360
yl=float(par.readline().split()[1])
cs=float(par.readline().split()[1])
ndv=int(par.readline().split()[1])
lons=[]
lats=[]
for i in range(nc):
    lons.append(xl)
    xl=xl+cs

for i in range(nr):
    lats.append(yl)
    yl=yl+cs
out.write('<begin_xyz>\n')
for j in range(nr):
    for i in range(nc):
        out.write('{:3.4f} {:3.4f} {:3.4f}'.format(lons[i],lats[-j],dat[j,i])+'\n')
out.write('<end_xyz>')
out.close()
    
    
    