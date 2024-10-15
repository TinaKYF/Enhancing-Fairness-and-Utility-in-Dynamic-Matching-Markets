# -*- coding: utf-8 -*-
"""
Created on Fri May 11 19:15:58 2018

@author: kyleq
"""
from Officer import Officer
import Log as log
import datetime
import copy
import statistics


class GreedyAlgorithm1:
    """
    In TOP or MTOP, a vio node will be assigned to the officer who has the highest probability to collect fines.
    The vio node will be scanned in order in the list.
    """

    def __init__(self, startTime=0, endTime=0, updateTime=1, carParkMap=None, stayProList=None):
        self.startTime = startTime
        self.currentTime = startTime
        self.endTime = endTime
        self.updateTime = updateTime
        self.carParkMap = carParkMap
        self.stayProList = stayProList
        self.freeOfficers = None
        self.totalBenefit = 0


    def initialOfficers(self, speed, startPointMarker, officerNum):
        for i in range(officerNum):
            self.carParkMap.officers.append(Officer(i, speed, startPointMarker))

    def execute(self):
        runTime = datetime.datetime.now()
        while self.currentTime < self.endTime:
            log.debugTag('currentTime', self.currentTime)
            self.updateOfficersStatus()
            self.assignNextPToOfficers()
            self.currentTime += self.updateTime
        stopTime = datetime.datetime.now()
        officerdis_record = []
        officerBenefit = []
        for officer in self.carParkMap.officers:
            officerdis_record.append(officer.totalDis)
            officerBenefit.append(officer.benefit)
        stdofficerdis_record = statistics.stdev(officerdis_record)
        stdofficerBenefit = statistics.stdev(officerBenefit)

        waitList = []
        for node in self.carParkMap.nodes:
            if node.takeTime and node.takeTime >= node.requestTime:
                waitList.append(node.takeTime - node.requestTime)

        stdWait = statistics.stdev(waitList)


        # write results to file
        fileName = 'greedy1_result.csv'
        titles = ['runTime', 'stopTime', 'startTime', 'endTime','officerdis_record', 'stdofficerdis_record',"officerBenefit", "stdofficerBenefit", "waitList", "stdWait"]
        params = [runTime, stopTime, self.startTime, self.endTime,officerdis_record, stdofficerdis_record,officerBenefit, stdofficerBenefit,  waitList, stdWait]
        self.carParkMap.printAllResults(fileName, titles, params)

    def updateOfficersStatus(self):
        for officer in self.carParkMap.officers:
            # when an officer finish his traveling
            if officer.assigned is True and officer.aimTime <= self.currentTime:
                officer.assigned = False
                officer.nextIntendedPoint = None
                self.carParkMap.releaseNode(officer.occupiedMarker)

    def assignNextPToOfficers(self):


        freeMenNum = self.carParkMap.getFreeOfficersNum()
        if freeMenNum > 0:  # if there are free officers this time
            assignedNum = 0
            # find current violation records at current time
            for index, row in self.carParkMap.vioHistories.iterrows():
                if assignedNum == freeMenNum:  # if all the officers have been assigned
                    break

                if row['RequestTime'] < self.currentTime :

                    marker = row['street_marker']
                    node = self.carParkMap.findNodeByMarkerId(marker)

                    self.freeOfficers = self.carParkMap.getFreeOfficers()
                    # the parking violation is happening
                    if node.assigned is False:
                        officer = self.getOfficerWithMaxPro(marker)
                        dis = self.carParkMap.getDistance(officer.occupiedMarker, marker)
                        travelTime = dis / officer.walkingSpeed
                        officer.arriveTime = self.currentTime + travelTime
                        officer.aimTime = officer.arriveTime + node.tripDistance / officer.walkingSpeed

                        officer.myPath.append(marker)
                        officer.occupiedMarker = node.aimMarker
                        officer.assigned = True
                        officer.totalDis += dis
                        node.assigned = True  # update node's status
                        assignedNum += 1
                        node.takeTime = self.currentTime + travelTime

                        # benefit increase when officer arrive before leaving for this record

                        officer.benefit += node.tripDistance - dis
                        officer.validDis += node.tripDistance
                        # benefit increase when officer arrive before leaving for this record

                        # remove this record from record history
                        self.carParkMap.vioHistories.drop(index, inplace=True)

            # if there are officers who have no assignment after scanning records at this time
            for officer in self.carParkMap.officers:
                if officer.assigned is False:
                    officer.saveTime += self.updateTime

    def getOfficerWithMaxPro(self, nodeMarker):
        maxPro = -float('inf')
        winnerOffi = None


        for officer in self.freeOfficers:
            if officer.assigned is False:
                nextNode=self.carParkMap.findNodeByMarkerId(nodeMarker)
                dis = self.carParkMap.getDistance(officer.occupiedMarker,nodeMarker)
                utility = nextNode.tripDistance - dis
                if utility > maxPro:
                    maxPro = utility
                    winnerOffi = officer
        return winnerOffi

