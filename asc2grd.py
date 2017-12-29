import numpy as np
par=open('RasterAscii.asc')
dat=np.loadtxt('RasterAscii.asc',skiprows=6)
dat=dat*-1.0 # Mohid require bathymetry positive
nc=int(par.readline().split()[1])
nr=int(par.readline().split()[1])
###Verificar longitud en 360
#xl=float(par.readline().split()[1])-360
xl=float(par.readline().split()[1])
yl=float(par.readline().split()[1])
cs=float(par.readline().split()[1])
ndv=int(par.readline().split()[1])
if dat[-1,-1].mean()==ndv*-1:
    dat=dat[:-1,:]
    nr=nr-1
    yl=yl-cs
###
##### Escribir la salida
class cfile(file):
    #subclass file to have a more convienient use of writeline
    def __init__(self, name, mode = 'r'):
        self = file.__init__(self, name, mode)

    def wl(self, string):
        self.writelines(string + '\n')
        return None
out=cfile('Dominio.dat','w')
out.wl('{:13}: {}'.format('COMENT1','Archivo Generado por WR Script'))
out.wl('')
out.wl('')
out.wl('{:13}:{} {}'.format(' ILB_IUB',1,nr))
out.wl('{:13}:{} {}'.format(' JLB_JUB',1,nc))
out.wl('{:13}:{}'.format(' COORD_TIP',4))
out.wl('{:13}:{:3.5f} {:3.6f}'.format(' ORIGIN',xl,yl))
out.wl('{:13}:{:.7E}'.format(' GRID_ANGLE',0.0))
#out.wl('{:13}:{:3.5f}'.format(' LATITUDE',(yl+0.116)))
#out.wl('{:13}:{:3.5f}'.format(' LONGITUDE',(xl+0.150)))
out.wl('{:13}:{:3.5f}'.format(' FILL_VALUE',-99))
out.wl('')
out.wl('')
##XX
out.wl('<BeginXX>')
k=0.0
for i in range(nc+1):
    out.wl('{:3.5f}'.format(k))
    k+=cs
out.wl('<EndXX>')

##YY
out.wl('<BeginYY>')
h=0.0
for i in range(nr+1):
    out.wl('  {:3.5f}'.format(h))
    h+=cs    
out.wl('<EndYY>')
####
out.wl('<BeginGridData2D>')
dat=np.flipud(dat)

for i in range(nr):
    for j in range(nc):
        z=dat[i,j]
        if z<0:
            z=-99.0000
        out.wl('{:3.2f}'.format(z))
out.write('<EndGridData2D>')
out.close()  
