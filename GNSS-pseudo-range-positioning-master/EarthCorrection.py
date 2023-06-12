import math
import numpy as np
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全
LV=299792458
we=7.29211567e-5

def earthcorr(ture_O_satenum,Xdg,Ydg,Zdg,nx,ny,nz):
	D0=np.zeros((ture_O_satenum))
	for x in range(ture_O_satenum):
		D0[x]=math.sqrt((Xdg[x]-nx)*(Xdg[x]-nx)+(Ydg[x]-ny)*(Ydg[x]-ny)+(Zdg[x]-nz)*(Zdg[x]-nz))
	#消除地球自转影响：
	traveltime=D0/LV
	omegatau=traveltime*we
	X0=Xdg*np.cos(omegatau)+Ydg*np.sin(omegatau)
	Y0=-Xdg*np.sin(omegatau)+Ydg*np.cos(omegatau)
	Z0=Zdg
	xjsj=nx
	yjsj=ny
	zjsj=nz
	return xjsj,yjsj,zjsj,X0,Y0,Z0
	#X0、Y0、Z0表示的是经过地球自转误差改正之后的卫星坐标;xjsj、yjsj、zjsj表示的是.o文件中接收机的概略坐标