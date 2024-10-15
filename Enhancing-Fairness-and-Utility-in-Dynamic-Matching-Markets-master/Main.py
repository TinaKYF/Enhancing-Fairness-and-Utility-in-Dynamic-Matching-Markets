# -*- coding: utf-8 -*-
"""
Created on Fri May 11 19:15:58 2018

@author: kyleq

Args algorithm_index, officer_num, fair_weight, cluster_method_index
min(fair_weight) = 1
"""
import pandas as pd
import numpy as np
import sys
import gc
from CarParkMap import CarParkMap
from cluster import CLUSTER
from consKmean import CONSKEANM
from Genetic2 import GeneticAlgorithm2
from Genetic3 import GeneticAlgorithm3
from Genetic4 import GeneticAlgorithm4
from Genetic5 import GeneticAlgorithm5
from Genetic6 import GeneticAlgorithm6
from Genetic7 import GeneticAlgorithm7
from Genetic8 import GeneticAlgorithm8
from Genetic9 import GeneticAlgorithm9
from Genetic10 import GeneticAlgorithm10
from Genetic11 import GeneticAlgorithm11

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
mainPath = './data/'

resultPath = mainPath  + 'results/' + dataDate + '/'
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
timeRange = (1, 1080)  # 480 - 8am; 780 - 12:30pm; 800 - 1pm; 1080 - 6pm; 1140 - 7pm

vioData = vioData[(vioData.RequestTime > timeRange[0])]


clusterType = "Uncluster"
clusterIndex = int(sys.argv[4])
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


if algorithm == 2:
    geneticAlgorithm = GeneticAlgorithm2(startTime, endTime, updateTime, carParkMap, clusterType=clusterType)
    geneticAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    geneticAlgorithm.execute()
#GA基础，utility计算时只采用request的发出点


if algorithm == 3:
    geneticAlgorithm = GeneticAlgorithm3(startTime, endTime, updateTime, carParkMap, clusterWaitList=clusterWaitList, clusterType=clusterType)
    geneticAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    geneticAlgorithm.execute()
#计算LERK uitility时采用上一个request的目标地点


if algorithm == 4:
    geneticAlgorithm = GeneticAlgorithm4(startTime, endTime, updateTime, carParkMap, clusterWaitList=clusterWaitList, clusterType=clusterType)
    geneticAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    geneticAlgorithm.execute()
'''
计算LERK uitility时采用上一个request的目标地点
采用utility和fairness两个标准排序。用于选优作为父母染色体
实际是等候安排的时间
'''


if algorithm == 5:
    geneticAlgorithm = GeneticAlgorithm5(startTime, endTime, updateTime, carParkMap, clusterWaitList=clusterWaitList, clusterType=clusterType)
    geneticAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    geneticAlgorithm.execute()
'''
计算LERK uitility时采用上一个request的目标地点
采用utility和fairness两个标准排序。用于选优作为父母染色体
考虑到安排过但未上车的request，同样作为waiting time
'''


if algorithm == 6:
    geneticAlgorithm = GeneticAlgorithm6(startTime, endTime, updateTime, carParkMap, clusterWaitList=clusterWaitList, clusterType=clusterType)
    geneticAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    geneticAlgorithm.execute()
'''
其他同5，cluster不同。使用带限制的K-means聚类
'''


if algorithm==7:
    geneticAlgorithm = GeneticAlgorithm7(startTime, endTime, updateTime, carParkMap, clusterWaitList=clusterWaitList, clusterType=clusterType)
    geneticAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    geneticAlgorithm.execute()
'''
在进行local optimization时
1.新生成的子染色体100%执行local optimization
2.local optimization中，以每个cluster内部中request的waiting time的标准差为标准。旨在令cluster内request等待时间接近。
'''


if algorithm==8:
    geneticAlgorithm = GeneticAlgorithm8(startTime, endTime, updateTime, carParkMap, clusterWaitList=clusterWaitList, clusterType=clusterType)
    geneticAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    geneticAlgorithm.execute()
'''
在执行local optimization的的时候
local optimization只关心序列中距离driver最近的点
其他同7
'''


if algorithm==9:
    geneticAlgorithm = GeneticAlgorithm9(startTime, endTime, updateTime, carParkMap, clusterWaitList=clusterWaitList, clusterType=clusterType)
    geneticAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    geneticAlgorithm.execute()
'''
在赋予随机数时，每个cluster内的点对应的随机数上下界分明，不同cluster点对应的随机数范围不同。
随机给cluster安排顺序，如cluster1在同一个population的不同的染色体中可以安排[0,1]或[3,4]
'''

if algorithm==10:
    geneticAlgorithm = GeneticAlgorithm10(startTime, endTime, updateTime, carParkMap, clusterWaitList=clusterWaitList, clusterType=clusterType, fairWeight=int(sys.argv[3]))
    geneticAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    geneticAlgorithm.execute()
'''
每隔fairWeight个周期运行一次fair
'''

if algorithm==11:
    geneticAlgorithm = GeneticAlgorithm11(startTime, endTime, updateTime, carParkMap, clusterWaitList=clusterWaitList, clusterType=clusterType,fairWeight=int(sys.argv[3]))
    geneticAlgorithm.initialOfficers(speed, startPointMarker, officerNum)
    geneticAlgorithm.execute()
'''
7+9，综合local optimization和random
'''
