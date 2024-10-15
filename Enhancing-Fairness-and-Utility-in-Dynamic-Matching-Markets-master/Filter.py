#去掉含0的经纬度坐标
import pandas as pd
taxicsv = pd.read_csv('D:\\MTOP\\On-Demand-Ridesourcing-Project-master\\Data\\2016_03.csv', header=0, dtype='object')
taxicsv=taxicsv[taxicsv["pickup_longitude"]!="0.0"]
taxicsv=taxicsv.drop_duplicates(subset=['pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude'])

taxicsv.to_csv("2016_03_filter.csv",index=False)