import math
import numpy as np
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全
GM=3.986005e+14  
we=7.29211567e-5

def satelliteposition(sateeph_new,ture_O_satenum,tx_GPS):

	prn=np.zeros((ture_O_satenum))
	toe=np.zeros((ture_O_satenum))
	n0=np.zeros((ture_O_satenum)) #未改正的平均角速度
	n =np.zeros((ture_O_satenum)) #改正后的平均角速度
	PJD0=np.zeros((ture_O_satenum))#参考历元平近点角
	PJD=np.zeros((ture_O_satenum)) #瞬时历元平近点角
	E=np.zeros((ture_O_satenum))  #偏近点角
	ecc=np.zeros((ture_O_satenum))#偏心率
	f=np.zeros((ture_O_satenum))  #真近点角
	u0=np.zeros((ture_O_satenum))  #升交距角(未考虑摄动改正)
	u=np.zeros((ture_O_satenum))   #升交距角（已改正）
	r0=np.zeros((ture_O_satenum)) #卫星矢径（未改正）
	r=np.zeros((ture_O_satenum))  #卫星矢径（已改正）
	i0=np.zeros((ture_O_satenum)) #卫星轨道倾角（未改正）
	ii=np.zeros((ture_O_satenum)) #卫星轨道倾角（已改正）
	idot=np.zeros((ture_O_satenum))#卫星轨道倾角变化率
	omega=np.zeros((ture_O_satenum)) #近地点角距
	cuc=np.zeros((ture_O_satenum))#摄动改正参数
	cus=np.zeros((ture_O_satenum))
	crc=np.zeros((ture_O_satenum))
	crs=np.zeros((ture_O_satenum))
	cic=np.zeros((ture_O_satenum))
	cis=np.zeros((ture_O_satenum))
	GZu=np.zeros((ture_O_satenum))#摄动改正项
	GZr=np.zeros((ture_O_satenum))
	GZi=np.zeros((ture_O_satenum))
	for x in range(ture_O_satenum):
		n0[x]=math.sqrt(GM)/(math.pow(sateeph_new[3][x],3)) #eph[3][:]为参考时刻的轨道半径平方根

	n=n0+sateeph_new[4][:]
	PJD0=sateeph_new[2][:]
	ecc=sateeph_new[5][:]
	toe=sateeph_new[17][:]
	prn=sateeph_new[0][:]

	tk=tx_GPS-toe
	#print(tk)
	#GPS时间超限或下溢的修复:
	half_week = 302400
	for x in range(ture_O_satenum):
		if(tk[x] > half_week):
			tk[x] = tk-2*half_week
		if(tk[x] < -half_week):
			tk[x] = tk+2*half_week
	#print(tk)
	PJD=PJD0+np.multiply(n,tk) #矩阵点乘
	PJD=(PJD+2*math.pi)%(2*math.pi)
	#print(PJD)
	#迭代求E，偏近点角,这里要注意不用把E化为角度，因为在python使用sin（）内部默认为弧度
	for x in range(7):#发现7次迭代基本收敛
		E=PJD+np.multiply(ecc,np.sin(E))
		#print(E)
	E=(E+2*math.pi)%(2*math.pi)
	for x in range(ture_O_satenum):
		f[x]=math.atan2((math.sqrt(1-ecc[x]*ecc[x])*math.sin(E[x])),(math.cos(E[x])-ecc[x]))
	
	omega=sateeph_new[6][:]
	u0=f+omega #升交距角
	#u0=(u0+2*math.pi)%(2*math.pi)
	#计算摄动改正项
	
	cuc=sateeph_new[7][:]
	cus=sateeph_new[8][:]
	crc=sateeph_new[9][:]
	crs=sateeph_new[10][:]
	cic=sateeph_new[13][:]
	cis=sateeph_new[14][:]
	GZu=np.multiply(cuc,np.cos(2*u0))+np.multiply(cus,np.sin(2*u0))
	GZr=np.multiply(crc,np.cos(2*u0))+np.multiply(crs,np.sin(2*u0))
	GZi=np.multiply(cic,np.cos(2*u0))+np.multiply(cis,np.sin(2*u0))
	#计算受摄卫星矢径r0（改正计算中要用到）
	for x in range(ture_O_satenum):
		r0[x]=math.pow(sateeph_new[3][x],2)*(1-ecc[x]*math.cos(E[x]))
	i0=sateeph_new[11][:]
	idot=sateeph_new[12][:]
	#进行改正计算
	u=u0+GZu
	r=r0+GZr
	ii=i0+GZi+np.multiply(idot,tk)
	
	#卫星在轨道平面坐标系的坐标计算：
	xk=np.zeros((ture_O_satenum))
	yk=np.zeros((ture_O_satenum))
	xk=np.multiply(r,np.cos(u))
	yk=np.multiply(r,np.sin(u))

	#计算观测瞬间升交点的经度L：
	Omega0=np.zeros((ture_O_satenum))#升交点赤径（开普勒参数）
	#注意：广播星历给出的不是Omegatoe，而是该值与本周起始时刻的格林尼治恒星时GASTweek之差，Omega0
	Omegadot=np.zeros((ture_O_satenum))#升交点赤径变化率
	#Omegas=np.zeros((len(j)))#观测瞬时的升径交点赤径（待计算）
	#for x in range(len(j)):#导出Omega0和Omegadot数据
	Omega0=sateeph_new[15][:]
	Omegadot=sateeph_new[16][:]
	L=Omega0+(Omegadot-we)*tk-we*toe#注意，书上的公式是错的
	L=(L+2*math.pi)%(2*math.pi) #保证在小周期中
	#print(L)
	#计算在地固坐标系下的坐标
	Xdg=np.zeros((ture_O_satenum))
	Ydg=np.zeros((ture_O_satenum))
	Zdg=np.zeros((ture_O_satenum))
	Xdg=np.multiply(xk,np.cos(L))-np.multiply(yk,(np.multiply(np.cos(ii),np.sin(L))))
	Ydg=np.multiply(xk,np.sin(L))+np.multiply(yk,(np.multiply(np.cos(ii),np.cos(L))))
	Zdg=np.multiply(yk,np.sin(ii))

	#print(L)
	#print(Xdg,Ydg,Zdg)
	return Xdg,Ydg,Zdg