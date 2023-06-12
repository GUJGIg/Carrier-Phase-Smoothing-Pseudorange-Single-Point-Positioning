import math
import numpy as np
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全

def Klobuchar(Ocontent_same_eph):
	#el=getel(nx,ny,nz,X0,Y0,Z0,ture_O_satenum)
	#sida=445/(el+20)-4#地心夹角
	Vion=-(Ocontent_same_eph[4][:]-Ocontent_same_eph[5][:])*1.54573
	return Vion