import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans2, whiten
import pandas as pd
from sklearn.cluster import KMeans
import csv
from collections import Counter

class CLUSTER:
    def __init__(self,officernum,dataDate,vioData):
        self.officernum=officernum
        self.datadate=dataDate
        self.vioData=vioData

    def cluster_hisdata(self):
        self.vioData=self.vioData.reset_index(drop=True)
        nodelist = []
        arealist = []
        # nodeData = pd.read_csv('data\\bay_vio_data_'+self.datadate+'.csv')
        for i in range(len(self.vioData)):
            nodelist.append([self.vioData['lon'][i], self.vioData['lat'][i]])

        # latlist=[]
        # lonlist=[]
        # for i in range(len(self.viodata)):
        #     for j in range(len(self.nodedata)):
        #         if self.viodata['street_marker'][i]==self.nodedata['st_marker_id'][j]:
        #             latlist.append(self.nodedata['lat'][j])
        #             lonlist.append(self.nodedata['lon'][j])
        # self.viodata['lat']=latlist
        # self.viodata['lon']=lonlist



        # num_min = int(1900/ self.officernum * 0.7)#11148
        # num_max = int(1900 / self.officernum * 1.3)
        coordinates = np.array(nodelist)
        clf = KMeans(
            n_clusters=self.officernum,
            # size_min=num_min,
            # size_max=num_max,
            random_state=0
        )
        y = clf.fit_predict(coordinates)
        # plt.scatter(coordinates[:,0],coordinates[:,1],c=y)
        # plt.show()
        # y_list = []
        # keylist = [i for i in range(self.officernum)]
        # valuelist = [0 for j in range(self.officernum)]
        # res = dict(zip(keylist, valuelist))

        # for i in y:
        #     res[i] += 1
        #     y_list.append(i)
        # nodeData['area'] = y_list

        # for i in sensordata['st_marker_id']:
        #     for j in range(len(nodeData)):
        #         if nodeData['street_marker'][j]==i:
        #             arealist.append(nodeData['area'][j])
        #             break
        # sensordata['AREA']=arealist
        # sensordata.to_csv('data\\filter_bay_sensors_vio_loc_02_08_'+str(num)+'.csv',index=0)
        centralnodelist = []
        for j in clf.cluster_centers_:
            centralnodelist.append(list(j))#[lon,lat]形式的各个簇的中心坐标

        candicoolist = []
        candimarkerlist = []
        for centralnode in centralnodelist:
            mindis = 99999
            for i in range(len(self.vioData)):
                nowdis = (centralnode[0] - self.vioData['lon'][i]) ** 2 + (centralnode[1] - self.vioData['lat'][i]) ** 2
                if nowdis < mindis:
                    mindis = nowdis
                    candicoo = [self.vioData['lon'][i], self.vioData['lat'][i]]
                    candimarker = self.vioData['street_marker'][i]
            candicoolist.append(candicoo)
            candimarkerlist.append(candimarker)

        clusterCenter=[]#每个点所属簇的最接近中心点的点
        clusterCenterAim=[]
        for labelIndex in y:
            clusterCenter.append(candimarkerlist[labelIndex])
        for i in range(len(clusterCenter)):
            for j in range(len(self.vioData)):
                if self.vioData['street_marker'][j]==clusterCenter[i]:
                    clusterCenterAim.append(self.vioData['aim_marker'][j])
        self.vioData['central_marker']=clusterCenter
        self.vioData['central_aimMarker']=clusterCenterAim
        self.vioData['cluster']=y
        print(Counter(y))

        return self.vioData
if __name__ == '__main__':
    datadate="03_19"
    vioData = pd.read_csv('data\\bay_vio_data_' + datadate + '.csv')
    timeRange = (1, 1080)
    vioData = vioData[(vioData.RequestTime > timeRange[0])]
    clu=CLUSTER(100,datadate,vioData)
    print(clu.cluster_hisdata())
