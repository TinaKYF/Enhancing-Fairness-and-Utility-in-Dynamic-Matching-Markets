# -*- coding: utf-8 -*-
"""
Created on Fri May 11 19:15:58 2018

@author: kyleq
Args algorithm_index, officer_num
"""
import pandas as pd
import numpy as np
import gc
from CarParkMap import CarParkMap
from cluster import CLUSTER
from consKmean import CONSKEANM
from Genetic2 import GeneticAlgorithm2
from Greedy1 import GreedyAlgorithm1
from Nearest import NearestAlgorithm
from PSO1 import PSOAlgorithm
from Cuckoo import CuckooAlgorithm
import sys

# Records number per day
# 02_08 - 1795 (420, 1140)
# 02_09 - 2152 (420, 1140)
# 02_10 - 2143 (420, 1140)
# 02_11 - 2129 (420, 1140)
# 02_12 - 2128 (420, 1140)
# 02_13 - 1470 (420, 1140)
# 02_14 - 1764 (420, 1140)

# 02_08 - 1657 (480, 1080)
# 02_09 - 1970 (480, 1080)
# 02_10 - 1972 (480, 1080)
# 02_11 - 1976 (480, 1080)
# 02_12 - 1940 (480, 1080)
# 02_13 - 1279 (480, 1080)
# 02_14 - 1643 (480, 1080)

dataDate = '03_19'
# dayRange = '02_08-12'  # 02_08-12; 02_15-19;
mainPath = '../data/'

resultPath = '../data/baseline_results/' + dataDate + '/'
# nodesFileName = mainPath + dataSubset + 'bay_sensors_vio_loc_' + dayRange + '.csv'
nodesFileName = mainPath  + 'bay_sensors_vio_loc_' + dataDate + '.csv'
distanceFileName = mainPath  + 'dis_CBD_twoPs_' + dataDate + '.csv'
vioRecordsFileName = mainPath  + 'bay_vio_data_' + dataDate + '.csv'
# stayProFileName = mainPath + 'stayPro_jan.csv'

nodesData = pd.read_csv(nodesFileName)
disData = pd.read_csv(distanceFileName)
vioData = pd.read_csv(vioRecordsFileName)
# stayProData = pd.read_csv(stayProFileName)
officerNum = int(sys.argv[2])
timeRange = (1, 2500000)  # 480 - 8am; 780 - 12:30pm; 800 - 1pm; 1080 - 6pm; 1140 - 7pm

vioData = vioData[(vioData.RequestTime > timeRange[0])]


clusterType= "Uncluster"
clusterIndex=0
if clusterIndex==0:
    vioData['central_marker'] = ['B000']*len(vioData)
    vioData['central_aimMarker'] = ['B001']*len(vioData)
    vioData['cluster'] = [-1]*len(vioData)
if clusterIndex==1:
    vioData = CLUSTER(officerNum, dataDate, vioData).cluster_hisdata()
    clusterType= "Kmean"
if clusterIndex==2:
    vioData = CONSKEANM(officerNum, dataDate, vioData).cluster_hisdata()
    clusterType= "ConsKmean"


clusterWaitList=[0 for _ in range(officerNum)]
# read distribution of leaving probability in the current area
# leavingFileName = mainPath + 'leaving_pro.csv'
# leaveProList = np.genfromtxt(leavingFileName, delimiter=',')
# stayProList = [1 - x for x in leaveProList]
# stayProList = stayProData['pro'].tolist()

carParkMap = CarParkMap()
carParkMap.initialMap(nodesData, disData, vioData, resultPath)

# delete data from memory
del nodesData
del disData
del vioData
gc.collect()

startTime = timeRange[0] + 1  # Officer begin to collect fines from this time
endTime = timeRange[1]  # Officer end collecting fines at this time
updateTime = 1  # the violation information update frequency in minutes
speed = 700  # officers' avg speed
startPointMarker = 'A0'  # (-37.810393, 144.964267, 'central_station')
algorithm = int(sys.argv[1])
 # 15, 20, 30, 40, 50




if algorithm == 22:
    GenAlgorithm = GeneticAlgorithm2(startTime, endTime, updateTime, carParkMap)
    GenAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    GenAlgorithm.execute()

if algorithm == 23:
    GreAlgorithm = GreedyAlgorithm1(startTime, endTime, updateTime, carParkMap)
    GreAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    GreAlgorithm.execute()

if algorithm == 24:
    NeaAlgorithm = NearestAlgorithm(startTime, endTime, updateTime, carParkMap)
    NeaAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    NeaAlgorithm.execute()

if algorithm == 25:
    PsoAlgorithm = PSOAlgorithm(startTime, endTime, updateTime, carParkMap)
    PsoAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    PsoAlgorithm.execute()

if algorithm == 26:
    CucAlgorithm = CuckooAlgorithm(startTime, endTime, updateTime, carParkMap)
    CucAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    CucAlgorithm.execute()
