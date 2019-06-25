import pyads
import time
import pandas as pd

remote_ip = '134.130.56.144' 
plc = pyads.Connection('5.53.34.234.1.1', 851) 
plc.open() 

# declare variables for CCA Pre-test
ValveSet_CCA_list = []  # list for CCA valve setpoint specified value 
ValvePos_CCA_list = []  # list for CCA valve position feedback
ValveError_CCA_list = []  #list for CCa valve error Boolean, TRUE if set value and feedback position differs
T_CCASup_list = []  # list for supply temperature of CCA
T_CCARet_list = []  # list for return temperature of CCA
PumpPowerCCA_list = []  # list for logging pump power data of CCA
PumpSpeedCCA_list = []  # list for logging pump rotation speed data of CCA
PumpPressDiffCCA_list = []  # list for logging pump pressure difference data of CCA
PumpVolFlowCCA_list = []  # list for logging pump volume flow data of CCA
ValveSet_CCA = 0  # initial setpoint in %
ValveSet_min_CCA = 0
ValveSet_max_CCA = 100
ValveSet_interval_CCA = 10
num_iteration_CCA = int(2 * (ValveSet_max_CCA - ValveSet_min_CCA) / ValveSet_interval_CCA + 1)

plc.write_by_name('FB_CCA_OOP.eModSet', 2, pyads.PLCTYPE_INT)  # set Manual as control mode of CCA
# get temperature setpoint, 1. the maximal setpoint is specified as 50 Celsius
plc.write_by_name('FB_CCA_OOP.fbControl.TsetLim', 50, pyads.PLCTYPE_REAL)
# get temperature setpoint, 2. take the set temperature of CCA stored in GVL HeatDistribution
Tset_CCA = plc.read_by_name('HeatDistribution.TsetCCA', pyads.PLCTYPE_REAL)
plc.write_by_name('FB_CCA_OOP.fbControl.TsetLim', Tset_CCA, pyads.PLCTYPE_REAL)

for i in range(num_iteration_CCA):
	if i < ((num_iteration_CCA + 1) / 2):
		ValveSet_CCA += ValveSet_interval_CCA * i
	else:
		ValveSet_CCA -= ValveSet_interval_CCA * (i - ((num_iteration_CCA - 1) / 2))
	ValveSet_CCA_list.append(ValveSet_CCA)
	plc.write_by_name('FB_CCA_OOP.fbControl.ValveSet', ValveSet_CCA, pyads.PLCTYPE_REAL)  # set CCA valve setpoint as 0%, then 10%, 20%, ...
	time.sleep(3600)  # time interval between each step change of setpoint: 1h
	ValvePos_CCA = plc.read_by_name('ValvePos.ValPosCCA', pyads.PLCTYPE_REAL)  # actual valve position of CCA
	ValvePos_CCA_list.append(ValvePos_CCA)
	ValveError_CCA = plc.read_by_name('FB_CCA_OOP.fbValve.Error', pyads.PLCTYPE_BOOL)  # check if difference between set and actual value exceeds the maximum limit
	ValveError_CCA_list.append(ValveError_CCA)
	T_CCASup = plc.read_by_name('TempSensors.TempCCASup', pyads.PLCTYPE_REAL) # current supply flow temperature of CCA
	T_CCASup_list.append(T_CCASup)
	T_CCARet = plc.read_by_name('TempSensors.TempCCARet', pyads.PLCTYPE_REAL)	# current return temperature of CCA
	T_CCARet_list.append(T_CCARet)
	PumpPowerCCA = plc.read_by_name('PumpInfos.stPumpCCAInfo.fPower', pyads.PLCTYPE_REAL)	# current pump operating power of CCA
	PumpPowerCCA_list.append(PumpPowerCCA)
	PumpSpeedCCA = plc.read_by_name('PumpInfos.stPumpCCAInfo.fSpeed', pyads.PLCTYPE_REAL)	# current pump rotation speed of CCA
	PumpSpeedCCA_list.append(PumpSpeedCCA)
	PumpPressDiffCCA = plc.read_by_name('PumpInfos.stPumpCCAInfo.fPressDiff', pyads.PLCTYPE_REAL)	# current pump pressure difference of CCA
	PumpPressDiffCCA_list.append(PumpPressDiffCCA)
	PumpVolFlowCCA = plc.read_by_name('PumpInfos.stPumpCCAInfo.fVolFlow', pyads.PLCTYPE_REAL)	# current pump volume flow of CCA
	PumpVolFlowCCA_list.append(PumpVolFlowCCA)

DataCCA = pd.DataFrame({'ValveSet_CCA':ValveSet_CCA_list,'Temp_CCASup':T_CCASup_list,'Temp_CCARet':T_CCARet_list,'PumpPowerCCA':PumpPowerCCA_list,'PumpSpeedCCA':PumpSpeedCCA_list,'PumpPressDiffCCA':PumpPressDiffCCA_list,'PumpVolFlowCCA':PumpVolFlowCCA_list})
DataCCA.to_csv('dataCCA.csv',index=False)  #write relevant data to csv for following data process
	
plc.close()