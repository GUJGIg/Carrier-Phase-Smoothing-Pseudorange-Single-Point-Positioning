import numpy as np
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全
LV=299792458

def SateTimecorrection(ture_O_satenum,sateeph_new,Ocontent_same_eph,sec_of_week):
	#tx_RAW=np.zeros((len(o1)))
	tx_RAW = sec_of_week - Ocontent_same_eph[4][:]/LV #考虑信号传播过程中的卫星运动
	toe=sateeph_new[17][:]
	tt=tx_RAW-toe#卫星钟的参考时刻
	#GPS时间超限或下溢的修复:
	half_week = 302400
	for x in range(ture_O_satenum):
		if(tt[x] > half_week):
			tt[x] = tt-2*half_week
		if(tt[x] < -half_week):
			tt[x] = tt+2*half_week
	#钟差改正：
	tcorr = (sateeph_new[1][:]*tt + sateeph_new[19][:])*tt + sateeph_new[18][:]
	tx_GPS = tx_RAW-tcorr
	#print(tcorr*LV)
	return tx_GPS,tcorr