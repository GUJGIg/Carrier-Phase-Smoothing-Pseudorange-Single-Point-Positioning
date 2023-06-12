import math
import numpy as np
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全

def togeod(nx,ny,nz):
	a=6378137 #椭圆长半径
	finv=298.257223563 #扁率
	h = 0
	tolsq = 1.e-10
	maxit = 10
	rtd = 180/math.pi
	esq=(2-1/finv)/finv
	oneesq=1-esq
	P=math.sqrt(nx*nx+ny*ny)
	dlambda=math.atan2(ny,nx)*rtd
	if(dlambda<0):
		dlambda=dlambda+360
	r=math.sqrt(P*P+nz*nz)
	sinphi=nz/r
	dphi=math.asin(sinphi)
	h=r-a*(1-sinphi*sinphi/finv)
	for i in range(maxit):
		sinphi=math.sin(dphi)
		cosphi=math.cos(dphi)
		N_phi=a/math.sqrt(1-esq*sinphi*sinphi)
		dP=P-(N_phi+h)*cosphi
		dZ=nz-(N_phi*oneesq+h)*sinphi
		h=h+(sinphi*dZ+cosphi*dP)
		dphi = dphi+(cosphi*dZ-sinphi*dP)/(N_phi + h)
		if(dP*dP+dZ*dZ<tolsq):
			break
	dphi=dphi*rtd
	return dphi,dlambda,h
	#dphi、dlambda、h表示经纬度、大地高