import numpy as np
from Read_N import readN
from Read_O import readO
from Hatch_file import Hatch_filter
from TimeChange import TIMEchange
from GetSat import getsat
from SateTimeCorrection import SateTimecorrection
from SatellitePosition import satelliteposition
from SPLocation import SPLocation
from Second import format_time
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全

import time
start_time = time.time()
eph,noeph,ALPHA,BETA=readN('C:/Users/ASUS/Desktop/导航大作业/GNSS-pseudo-range-positioning-master/gold2950.17n','C:/Users/ASUS/Desktop/导航大作业/GNSS-pseudo-range-positioning-master/eph.txt')
Ocontent,sates,year,month,day,nx,ny,nz,K=readO('C:/Users/ASUS/Desktop/导航大作业/GNSS-pseudo-range-positioning-master/gold2950.171o','C:/Users/ASUS/Desktop/导航大作业/GNSS-pseudo-range-positioning-master/Ocontent.txt')
Ocontent=Hatch_filter(Ocontent, sates, K)
error=np.zeros((2879))
X=np.zeros((2879))
Y=np.zeros((2879))
Z=np.zeros((2879))
x_error=np.zeros((2879))
y_error=np.zeros((2879))
z_error=np.zeros((2879))
Reciver_position=np.zeros((1,3))
Reciver_position[0][0]=nx
Reciver_position[0][1]=ny
Reciver_position[0][2]=nz
file=open("C:/Users/ASUS/Desktop/导航大作业/GNSS-pseudo-range-positioning-master/接收机一天内的位置估计(WGS-84).txt","w")
file.write("接收机初始位置：" + str(Reciver_position[0]) + '\n')
for time_num in range(12):
	ST=52650+30*time_num
	sec_of_week=TIMEchange(year,month,day,ST)
	sateeph_new,Ocontent_same_eph,ture_O_satenum=getsat(eph,noeph,Ocontent,sec_of_week,sates,ST)
	tx_GPS,tcorr=SateTimecorrection(ture_O_satenum,sateeph_new,Ocontent_same_eph,sec_of_week)
	Xdg,Ydg,Zdg=satelliteposition(sateeph_new,ture_O_satenum,tx_GPS)
	xjsj,yjsj,zjsj,vT,accuracy=SPLocation(tcorr,Ocontent_same_eph,ture_O_satenum,Xdg,Ydg,Zdg,nx,ny,nz)
	Reciver_position_estimate=np.zeros((12, 3))
	Reciver_position_estimate[time_num][0]=xjsj
	Reciver_position_estimate[time_num][1]=yjsj
	Reciver_position_estimate[time_num][2]=zjsj
	error[time_num]=accuracy
	hours,minutes,seconds=format_time(30*time_num)
	file.write("历元:2017年10月22日" + str(hours) + "时" + str(minutes) + "分" + str(seconds) + "秒" + " WGS-84接收机位置是:" + str(Reciver_position_estimate[time_num]) + "精度评定为：" + str(error[time_num]) + '\n')