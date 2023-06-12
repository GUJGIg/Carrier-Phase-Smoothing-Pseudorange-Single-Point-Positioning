import numpy as np
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全

def readN(ephemerisfile,outputfile):
	fide = open(ephemerisfile,'r+')
	#line=fide.readlines	#读整个文件
	lines = fide.readlines()
	fide.seek(0)

	for s in lines:
		fide.write(s.replace('D','e'))# replace是替换，write是写入
	
	fide.close()
	fide = open(ephemerisfile,'r')
	line = fide.readlines()#.splitlines(True)
	ALPHA = np.zeros((4))
	BETA = np.zeros((4))
	for i,content in enumerate(line):#i为行数，content为内容
		if "ION ALPHA" in content:
			ALPHA[0]=line[i][3:14]
			ALPHA[1]=line[i][15:26]
			ALPHA[2]=line[i][27:38]
			ALPHA[3]=line[i][39:50]
			i=i+1
			BETA[0]=line[i][3:14]
			BETA[1]=line[i][15:26]
			BETA[2]=line[i][27:38]
			BETA[3]=line[i][39:50]
			break

	for i,content in enumerate(line):#i为行数，content为内容
		if "ENe OF HEAeER" in content:
			i=i+1
			break

	noeph = int((len(line)-i)/8)#卫星数
	#print(noeph)
	fide.close()

	year=np.zeros((noeph))
	month=np.zeros((noeph))
	day=np.zeros((noeph))
	hour=np.zeros((noeph))
	minute=np.zeros((noeph))
	second=np.zeros((noeph))
	svprn=np.zeros((noeph))
	weekno=np.zeros((noeph))
	t0c=np.zeros((noeph))
	tgd=np.zeros((noeph))
	aodc=np.zeros((noeph))
	toe=np.zeros((noeph))
	af2=np.zeros((noeph))
	af1=np.zeros((noeph))
	af0=np.zeros((noeph))
	aode=np.zeros((noeph))
	deltan=np.zeros((noeph))
	M0=np.zeros((noeph))
	ecc=np.zeros((noeph))
	roota=np.zeros((noeph))
	toe=np.zeros((noeph))
	cic=np.zeros((noeph))
	crc=np.zeros((noeph))
	cis=np.zeros((noeph))
	crs=np.zeros((noeph))
	cuc=np.zeros((noeph))
	cus=np.zeros((noeph))
	Omega0=np.zeros((noeph))
	omega=np.zeros((noeph))
	i0=np.zeros((noeph))
	Omegadot=np.zeros((noeph))
	idot=np.zeros((noeph))
	accuracy=np.zeros((noeph))
	health=np.zeros((noeph))
	fit=np.zeros((noeph))
	IODE=np.zeros((noeph))
	codes=np.zeros((noeph))
	L2flag=np.zeros((noeph))
	svaccur=np.zeros((noeph))
	svhealth=np.zeros((noeph))
	iodc=np.zeros((noeph))
	tom=np.zeros((noeph))
	spare=np.zeros((noeph))
	eph=np.zeros((21,noeph))
	
	j=0
	for x in range(noeph):
		svprn[j]=(line[i][0:2])
		year[j] = line[i][3:5]
		month[j] = line[i][6:8]
		day[j] = line[i][9:11]
		hour[j] = line[i][12:14]
		minute[j] = line[i][15:17]
		second[j] = line[i][19:22]
		af0[j] = (line[i][22:41])
		af1[j] = line[i][41:60]
		af2[j] = line[i][60:79]
		i=i+1
		IODE[j] = line[i][3:22]
		crs[j] = line[i][22:41]
		deltan[j] = line[i][41:60]
		M0[j] = (line[i][60:79])
		i=i+1
		cuc[j] = (line[i][3:22])
		ecc[j] = (line[i][22:41])
		cus[j] = (line[i][41:60])
		roota[j] = (line[i][60:79])
		i=i+1
		toe[j] = (line[i][3:22])
		cic[j] = (line[i][22:41])
		Omega0[j] = (line[i][41:60])
		cis[j] = (line[i][60:79])
		i=i+1
		i0[j] =  (line[i][3:22])
		crc[j] = (line[i][22:41])
		omega[j] = (line[i][41:60])
		Omegadot[j] = (line[i][60:79])
		i=i+1
		idot[j] = (line[i][3:22])
		codes[j] = (line[i][22:41])
		weekno[j] = (line[i][41:60])
		L2flag[j] = (line[i][60:79])
		i=i+1
		svaccur[j] = (line[i][3:22])
		svhealth[j] = (line[i][22:41])
		tgd[j] = (line[i][41:60])
		iodc[j] = line[i][60:79]
		i=i+1
		tom[j] = ((line[i][3:22]))
		spare[j] = line[i][22:79]
		i=i+1
		j=j+1
	
	eph[0][:noeph]  = svprn  #卫星prn号
	eph[1][:noeph]  = af2 #钟漂
	eph[2][:noeph]  = M0 # 参考时刻的平近点角（开普勒参数）
	eph[3][:noeph]  = roota #参考时刻的轨道半径平方根（开普勒参数）
	eph[4][:noeph]  = deltan #卫星平均角速度的改正值
	eph[5][:noeph]  = ecc #轨道偏心率（开普勒参数）
	eph[6][:noeph]  = omega #近地角距（开普勒参数）
	eph[7][:noeph]  = cuc #升交角距的正弦余值
	eph[8][:noeph]  = cus #升角距的改正项振幅
	eph[9][:noeph]  = crc #轨道向径的正余弦调
	eph[10][:noeph] = crs #轨道向径的改正项振幅
	eph[11][:noeph] = i0 #轨道倾角
	eph[12][:noeph] = idot #卫星轨道倾角变化率
	eph[13][:noeph] = cic #轨道倾角的正余弦调
	eph[14][:noeph] = cis #轨道倾角的改正项振幅
	eph[15][:noeph] = Omega0 #升交点赤径（开普勒参数）
	eph[16][:noeph] = Omegadot #升交点赤径变化率
	eph[17][:noeph] = toe #星历参考时间
	eph[18][:noeph] = af0 #钟差
	eph[19][:noeph] = af1 #钟速
	eph[20][:noeph] = tom #信息传输时间
		
	with open(outputfile,'w') as fidu:
		fidu.write(str(eph))
		#print(svprn[2])
	return eph,noeph,ALPHA,BETA