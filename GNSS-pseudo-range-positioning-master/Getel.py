import math
import numpy as np
from Togeod import togeod
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全

def getel(nx,ny,nz,X0,Y0,Z0,ture_O_satenum):
	dx=X0-nx
	dy=Y0-ny
	dz=Z0-nz
	dtr=math.pi/180
	phi,dlambda,h=togeod(nx,ny,nz)
	cl = math.cos(dlambda*dtr)
	sl = math.sin(dlambda*dtr)
	cb = math.cos(phi*dtr)
	sb = math.sin(phi*dtr)
	E=-sl*dx+(-sb)*cl*dy+cb*cl*dz
	N=cl*dx+(-sb)*sl*dy+cb*sl*dz
	U=cb*dy+sb*dz
	hor_dis=np.zeros((ture_O_satenum))
	Az=np.zeros((ture_O_satenum))
	EI=np.zeros((ture_O_satenum))
	for i in range(ture_O_satenum):
		hor_dis[i]=math.sqrt(E[i]*E[i]+N[i]*N[i])
		Az[i]=math.atan2(E[i],N[i])/dtr
		EI[i]=math.atan2(U[i],hor_dis[i])/dtr
		if(Az[i]<0):
			Az[i]=Az[i]+360
	#D=math.sqrt(dx*dx+dy*dy+dz*dz)
	return EI