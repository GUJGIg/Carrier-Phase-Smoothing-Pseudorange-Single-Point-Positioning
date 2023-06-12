import math
import numpy as np
from EarthCorrection import earthcorr
from Getel import getel
from Klobuchar import Klobuchar
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全
LV=299792458

def SPLocation(tcorr,Ocontent_same_eph,ture_O_satenum,Xdg,Ydg,Zdg,nx,ny,nz):

	vT=0#接收机钟差
	xjsj,yjsj,zjsj,X0,Y0,Z0=earthcorr(ture_O_satenum,Xdg,Ydg,Zdg,nx,ny,nz)
	el=getel(nx,ny,nz,X0,Y0,Z0,ture_O_satenum)
	#筛选出高度角小于10度的卫星:
	el_dele=[]
	for i in range(ture_O_satenum):
		if(abs(el[i])<10):
			el_dele.append(i)
	Vion=Klobuchar(Ocontent_same_eph)#进行电离层改正
	Vion=np.delete(Vion[0:ture_O_satenum],el_dele)
	#print(Vion)
	X0=np.delete(X0[0:ture_O_satenum],el_dele)
	Y0=np.delete(Y0[0:ture_O_satenum],el_dele)
	Z0=np.delete(Z0[0:ture_O_satenum],el_dele)
	tcorr=np.delete(tcorr[0:ture_O_satenum],el_dele)
	el=np.delete(el[0:ture_O_satenum],el_dele)

	ture_O_satenum=ture_O_satenum-len(el_dele)
	if(ture_O_satenum<4):
		print('卫星数不足，无法计算接收机位置')
	else:
		Ocontent_P1_fin=np.zeros((ture_O_satenum))
		Ocontent_P1_fin=np.delete(Ocontent_same_eph[4][:],el_dele)
		#print(smoothed_code)
		low0=np.zeros((ture_O_satenum))
		cs=np.zeros((ture_O_satenum))

		P=np.eye(ture_O_satenum) #暂且让其为1
		#print(el)
			#利用卫星高度角进行定权：
		el=math.pi*el/180#角度化弧度
		#print(el)
		for i in range(ture_O_satenum):
			P[i][i]=math.sin(el[i])*math.sin(el[i])

		#print(Ocontent_P1_fin)
		for e in range(6):#迭代6次
			for x in range(ture_O_satenum):
				low0[x]=math.sqrt((X0[x]-xjsj)*(X0[x]-xjsj)+(Y0[x]-yjsj)*(Y0[x]-yjsj)+(Z0[x]-zjsj)*(Z0[x]-zjsj))
			#print(low0)
			#准备位置计算矩阵数据：
			l=((X0-xjsj)/low0).T
			l.shape=(ture_O_satenum,1) #一维数组转置的时候有个坑，光transpose没有用，需要指定shape参数
			m=((Y0-yjsj)/low0).T
			m.shape=(ture_O_satenum,1)
			n=((Z0-zjsj)/low0).T
			n.shape=(ture_O_satenum,1)
			for x in range(ture_O_satenum):
				cs[x]=1
			cs.shape=(ture_O_satenum,1)
			B=np.hstack((-l,-m))#在行上合并
			B=np.hstack((B,-n))
			B=np.hstack((B,cs))
			
			
			L=(Ocontent_P1_fin-low0).T+tcorr*LV-Vion
			#print(L)
			L.shape=(ture_O_satenum,1)
			#print(L.shape)
			x=np.dot(np.dot(np.dot(np.linalg.inv(np.dot(np.dot(np.transpose(B),P),B)),B.T),P),L)
			xjsj=xjsj+x[0]
			yjsj=yjsj+x[1]
			zjsj=zjsj+x[2]
			vT=vT+x[3]
		#精度评定：
		accuracy=math.sqrt((nx-xjsj)*(nx-xjsj)+(ny-yjsj)*(ny-yjsj)+(nz-zjsj)*(nz-zjsj))
		#print(accuracy)
		#print(vT) #LV*pos机钟差
	return xjsj,yjsj,zjsj,vT,accuracy