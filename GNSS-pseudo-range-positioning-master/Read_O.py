import numpy as np
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全

def readO(ephemerisfile,outputfile):
	fide= open(ephemerisfile,'r') 
	lines = fide.readlines()
	fide.close()
	for i,content in enumerate(lines):#i为行数，content为内容
		if "APPROX POSITION XYZ " in content:#大致坐标
			nx=float(lines[i][:15])
			ny=float(lines[i][15:28])
			nz=float(lines[i][30:42])	
			break
	i=i+1
	TXH=lines[i][:15] #天线高
	
	for i,content in enumerate(lines):#i为行数，content为内容
		if "INTERVAL" in content:
			interval=int(float(lines[i][4:10])) #时间间隔
			break
	i=i+1
	year=int(lines[i][2:6]) #用于时间转换
	month=int(lines[i][10:12])
	day=int(lines[i][16:18])
	first_clock=lines[i][22:25]#为了计算循环参数K
	first_minute=lines[i][28:31]
	first_second=lines[i][33:35]
	i=i+1
	last_clock=lines[i][22:25]
	last_minute=lines[i][28:31]
	last_second=lines[i][33:35]
	
	K=int(((int(last_clock)-int(first_clock))*3600+(int(last_minute)-int(first_clock))*60+(int(last_second)-int(first_second))*1)/interval)
	#观测数(历元数)
	#print(K)
	for i,content in enumerate(lines):#i为行数，content为内容
		if "END OF HEADER" in content:
			break

	j=i+1#用于确定各个观测历元中观测到的卫星最大值，从而确定Ocontent的维数
	sates=[] #每个历元观测的卫星数，sates[]形式为[11,11,...,11],11表示每个观测历元的观测卫星数

	for x in range(K):
		sa=0
		sa=int(lines[j][33:35])#lines[j][33:35]表示的是11
		sates.append(lines[j][33:35])
		j=j+sa+1
		

	M=int(max(sates)) #观测卫星数最多的历元

	Ocontent=np.zeros((8,K,M))#K表示观测的历元数，M表示所有历元中观测的最大卫星数
	
	for x in range(K):   #大循环
		i=i+1#i未加1前，此时i仍在第83行，即END OF HEADER处
		sate_num=lines[i][33:35] #卫星数，非数组
		
		for n in range(int(sate_num)):
			i=i+1
			Ocontent[0][x][n]=int(lines[i][1:3])#卫星的prn号
			if lines[i][5:17].isspace():#.isspace()用检测lines[i][5:17]是否是空白值
				Ocontent[1][x][n]=None
			else:
				Ocontent[1][x][n]=lines[i][5:17]#卫星的L1频率的伪距观测值

			if lines[i][20:33].isspace():
				Ocontent[2][x][n]=None
			else:
				Ocontent[2][x][n]=lines[i][20:33]#L1频率的载波相位观测值
			
			if lines[i][36:49].isspace():
				Ocontent[3][x][n]=None
			else:
				Ocontent[3][x][n]=lines[i][36:51]#L2频率的载波相位观测值

			if lines[i][53:65].isspace():
				Ocontent[4][x][n]=None
			else:
				Ocontent[4][x][n]=lines[i][53:65]#表示宽巷的L1频率的伪距观测值

			if lines[i][69:81].isspace():
				Ocontent[5][x][n]=None
			else:
				Ocontent[5][x][n]=lines[i][69:81]#表示宽巷的L2频率的伪距观测值

			if lines[i][90:97].isspace():
				Ocontent[6][x][n]=None
			else:
				Ocontent[6][x][n]=lines[i][90:97]#表示L1频率的信号强度观测值

			if (lines[i][107:114].isspace())or(not lines[i][107:114]): #可能存在全是空格或为空两种情况
				Ocontent[7][x][n]=None
			else:
				Ocontent[7][x][n]=lines[i][107:114]#表示L2频率的信号强度观测值
			
	with open(outputfile,'w') as fidu:
		fidu.write(str(Ocontent))
	
	return Ocontent,sates,year,month,day,nx,ny,nz,K
	#Oconten表示.o文件中的主题内容包括伪距观测值、载波相位观测值、卫星PRN值；sates表示每个历元观测卫星数；year、mouth、day表示观测时间年月日；nx、ny、nz表示.o文件中接收机概略位置