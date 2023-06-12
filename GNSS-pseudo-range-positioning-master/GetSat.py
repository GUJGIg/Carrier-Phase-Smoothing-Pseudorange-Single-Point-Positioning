import math
import numpy as np
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全

def getsat(eph,noeph,Ocontent,sec_of_week,sates,ST):
	i=int(ST/30)     #瞬时时间在Ocontent矩阵中的位置
	M=np.zeros((noeph))	
	j=[]		#eph矩阵离瞬时矩阵最近的时间的列号
	for x in range(noeph): #185是noeph的值
		M[x]=abs(sec_of_week-eph[17][x])#取绝对值
	MIN=min(M)
	#print(MIN)
	for x in range(noeph):
		if(sec_of_week-eph[17][x]==MIN):
			j.append(x) #看了下矩阵应该有12个卫星,但是瞬时只观测到9个卫星，应当把12个卫星位置都计算出来,j存了N文件卫星prn号的列号
	prn=np.zeros((len(j)))
	sateeph=np.zeros((21,int(sates[i])))
	for x in range(len(j)):
		prn[x]=eph[0][j[0]+x]
	for x in range(int(sates[i])):
		for n in range(len(j)):
			if(Ocontent[0][i][x]==prn[n]):
				for w in range(21):
					sateeph[w][x]=eph[w][j[0]+n] #让该历元N文件数据按O文件卫星顺序排列
					#print(sateeph[w][x])
	inde=[]

	for index,value in enumerate(sateeph[2][:]):#找出该数据块中在O文件但不在N文件的卫星行号
		if(value==0):
			inde.append(index)
	#print(inde)
	ture_O_satenum=int(sates[i])-len(inde)#ture_O_satenum表示一个历元内可用的卫星数量.
	sateeph_new=np.zeros((21,ture_O_satenum))
	#print(prn[0])
	
	for w in range(21):
		sateeph_new[w][:]=np.delete(sateeph[w][0:int(sates[i])],inde)
	#以上完成了N文件数据sateeph转换为O文件卫星排列对应格式,得到sateeph_new
	#以下完成了O文件删除无对应卫星数据的工作，并存到Ocontent_same_eph矩阵
	Ocontent_same_eph=np.zeros((8,ture_O_satenum))
	#print(sateeph_new)
	#Ocontent_same_eph代表同一历元内可用卫星的7个观测值及PRN号
	for w in range(8):
		Ocontent_same_eph[w][:]=np.delete(Ocontent[w][i][0:int(sates[i])],inde)
	#print(Ocontent_same_eph[1][:])
	#Ocontent_same_eph数组变为一个二维数组，因为在getsat函数中，不同历元被抽离
	return sateeph_new,Ocontent_same_eph,ture_O_satenum