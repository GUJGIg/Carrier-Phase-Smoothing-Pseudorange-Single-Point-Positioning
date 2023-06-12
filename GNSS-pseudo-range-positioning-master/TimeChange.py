import math
import numpy as np
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全

def TIMEchange(year,month,day,ST):
	#年月日时转为儒略日
	clock=ST/3600
	if(month<=2):
		year=year-1
		month=month+12
	else:
		jd = math.floor(365.25*(year+4716))+math.floor(30.6001*(month+1))+day+clock/24-1537.5
	#儒略日转为GPS时
	a = math.floor(jd+0.5)
	b = a+1537
	c = math.floor((b-122.1)/365.25)
	e = math.floor(365.25*c)
	f = math.floor((b-e)/30.6001)
	d = b-e-math.floor(30.6001*f)+(jd+0.5)%1
	day_of_week = math.floor(jd+0.5)%7
	week = math.floor((jd-2444244.5)/7)
	sec_of_week = ((d%1)+day_of_week+1)*86400
	if(day_of_week==6):#如果当天就是周日
		sec_of_week=sec_of_week-7*24*3600
	#print(day_of_week)
	#print(sec_of_week)#周内秒
	return sec_of_week