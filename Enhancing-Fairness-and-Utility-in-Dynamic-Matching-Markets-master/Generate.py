# 生成必要的数据文件

import pandas as pd
# from geopy.distance import geodesic
from math import radians, cos, sin, asin, sqrt

nrow = 1000
taxicsv = pd.read_csv('2016_03_filter.csv', header=0, dtype='object', nrows=nrow)
pickupCood = []
dropoffCood = []


def geodistance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])  # 经纬度转换成弧度
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
    distance = round(distance / 1000, 3)
    return distance


for i in range(nrow):
    pickupCood.append((float(taxicsv["pickup_longitude"][i]), float(taxicsv["pickup_latitude"][i])))
    dropoffCood.append((float(taxicsv["dropoff_longitude"][i]), float(taxicsv["dropoff_latitude"][i])))
# 所有点，包含重复
# eliminCood = list(set(pickupCood + dropoffCood))
eliminCood = pickupCood + dropoffCood
# 不重复的所有点
coodMarkerDict = {}
marker = []
for i in range(len(eliminCood)):
    coodMarkerDict[eliminCood[i]] = "A" + str(i)
# 给这些点打上标记，eliminCood与marker成字典关系
bayVio = []
baySensor = []
for i in range(nrow):
    bayVio.append([coodMarkerDict[pickupCood[i]],
                   int(taxicsv["pickup_datetime"][i][-5:-3]) + int(taxicsv["pickup_datetime"][i][-8:-6] * 60),
                   float(taxicsv["trip_distance"][i]) * 1000, coodMarkerDict[dropoffCood[i]],pickupCood[i][0],pickupCood[i][1]])
    baySensor.append(
        [coodMarkerDict[pickupCood[i]], float(taxicsv["pickup_longitude"][i]), float(taxicsv["pickup_latitude"][i])])
    baySensor.append(
        [coodMarkerDict[dropoffCood[i]], float(taxicsv["dropoff_longitude"][i]), float(taxicsv["dropoff_latitude"][i])])
baySensorDf = pd.DataFrame(baySensor, columns=["st_marker_id", "lon", "lat"])
bayVioDf = pd.DataFrame(bayVio, columns=["street_marker", "RequestTime", "tripDistance","aim_marker","lon","lat"])
bayVioDf.to_csv("data//bay_vio_data_03_19.csv", index=False)

baySensorDf.to_csv("data//bay_sensors_vio_loc_03_19.csv", index=False)
disPs = []

for i in range(len(eliminCood)):
    for j in range(i, len(eliminCood)):
        dis = geodistance(eliminCood[i][0], eliminCood[i][1], eliminCood[j][0], eliminCood[j][1]) * 1000
        disPs.append([dis, coodMarkerDict[eliminCood[i]] + "_" + coodMarkerDict[eliminCood[j]]])
for i in range(len(eliminCood)):
    dis = geodistance(eliminCood[i][0], eliminCood[i][1], eliminCood[0][0], eliminCood[0][1]) * 1000
    disPs.append([dis, coodMarkerDict[eliminCood[i]] + "_central_station"])
disPsDf = pd.DataFrame(disPs, columns=["distance", "twoPs"])
disPsDf.to_csv("data//dis_CBD_twoPs_03_19.csv", index=False)

print(bayVio)
