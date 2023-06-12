import math
import numpy as np
np.set_printoptions(threshold=np.inf)  #保证numpy矩阵显示完全

def Hatch_filter(Ocontent, sates, K):
	alpha = 0.5
	beta = 0.2
	gamma = 0.1
	M=int(max(sates))
	Smoothed_pseudorange=np.zeros((K, M))
	Pseudorange=np.zeros((K, M))
	Carrier_phase=np.zeros((K, M))
	PRN_Sat=np.zeros((K, M))
	for i in range(K):
		PRN_Sat[i][:]=Ocontent[0][i][:]
		Pseudorange[i][:]=Ocontent[1][i][:]
		Carrier_phase[i][:]=Ocontent[2][i][:]
	Smoothed_phase=np.zeros((M))
	Smoothed_pse=np.zeros((M))
	phase_residual=np.zeros((M))
	pse_residual=np.zeros((M))
	for s in range(M):
		Smoothed_phase[s]=Carrier_phase[0][s]
		Smoothed_pse[s]=Pseudorange[0][s]
	for i in range(1, 12):
		for s in range(M):
			j=s
			if PRN_Sat[i][s]==PRN_Sat[i-1][j]:
				phase_residual[s]=Carrier_phase[i][s]-Smoothed_phase[j]
				pse_residual[s]=Pseudorange[i][s]-Smoothed_pse[j]
				Smoothed_phase[s]=alpha*phase_residual[s]+Smoothed_phase[j]
				Smoothed_pse[s]=beta*pse_residual[s]+Smoothed_pse[j]
				Smoothed_pseudorange[i][s]=Smoothed_pse[s]+gamma*Smoothed_phase[s]
				Ocontent[1][i][s]=Smoothed_pseudorange[i][s]
			else:
				j=0
				while PRN_Sat[i][s]!=PRN_Sat[i-1][j]:
					j=j+1
					if j>=int(sates[i]):
						l=i-1
						Bool=True
						while Bool:
							l=l-1
							for j in range(M):
								if PRN_Sat[i][s]==PRN_Sat[l][j]:
									phase_residual[s]=Carrier_phase[i][s]-Smoothed_phase[j]
									pse_residual[s]=Pseudorange[i][s]-Smoothed_pse[j]
									Smoothed_phase[s]=alpha*phase_residual[s]+Smoothed_phase[j]
									Smoothed_pse[s]=beta*pse_residual[s]+Smoothed_pse[j]
									Smoothed_pseudorange[i][s]=Smoothed_pse[s]+gamma*Smoothed_phase[s]
									Ocontent[1][i][s]=Smoothed_pseudorange[i][s]
									Bool=False
				phase_residual[s]=Carrier_phase[i][s]-Smoothed_phase[j]
				pse_residual[s]=Pseudorange[i][s]-Smoothed_pse[j]
				Smoothed_phase[s]=alpha*phase_residual[s]+Smoothed_phase[j]
				Smoothed_pse[s]=beta*pse_residual[s]+Smoothed_pse[j]
				Smoothed_pseudorange[i][s]=Smoothed_pse[s]+gamma*Smoothed_phase[s]
				Ocontent[1][i][s]=Smoothed_pseudorange[i][s]
	return Ocontent