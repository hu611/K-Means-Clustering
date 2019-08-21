#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import csv
import math
import matplotlib.pyplot as plt
from random import randrange, seed
import time


# In[33]:


class MyKmeans:
    def readData(self,filename):
        try:
            mylist = []
            with open(filename) as csvfile:
                readCSV = csv.reader(csvfile,delimiter=',')
                self.mylist = []
                for row in readCSV:
                    rowlist =[]
                    rowlist.append((int)(row[0]))
                    rowlist.append((int)(row[1]))
                    rowlist.append((float)(row[2]))
                    rowlist.append((float)(row[3]))
                    mylist.append(rowlist)
            return mylist
        except:
            return 'it is not a csv file'
    def cluster(self,parsedData,iterCount,k,centroids):
        try:
            centroidlist = []
            centroidvaluelist = []
            finallist = []
            length = 0
            if centroids == []:
                seed(1111)
                for f in range(k):
                    random_number = randrange(0,len(parsedData))
                    while parsedData[random_number] == []:
                        random_number = randrange(0,len(parsedData))
                    centroids.append(random_number)
            for i in range(k):
                centroidlist = [parsedData[centroids[i]][2],parsedData[centroids[i]][3]]
                centroidvaluelist.append(centroidlist)
                finallist.append([])
            for a in range(len(parsedData)):
                if parsedData[a] != []:
                    minnumber = math.sqrt((centroidvaluelist[0][0]-parsedData[a][2])**2
                                     + (centroidvaluelist[0][1]-parsedData[a][3])**2)
                    indexformaxnumber = 0
                    for b in range(len(centroidvaluelist)):
                        if math.sqrt((centroidvaluelist[b][0]-parsedData[a][2])**2 + (centroidvaluelist[b][1]-parsedData[a][3])**2) < minnumber:
                            indexformaxnumber = b
                            minnumber = math.sqrt((centroidvaluelist[b][0]-parsedData[a][2])**2
                                     + (centroidvaluelist[b][1]-parsedData[a][3])**2)
                    finallist[indexformaxnumber].append(parsedData[a][0])
                    length += 1
            for numberofiteration in range(iterCount-1):
                centroidvaluelist = []
                for c in range(k):
                    xtotalnumber = 0
                    ytotalnumber = 0
                    for xaxis in range(len(finallist[c])):
                        xtotalnumber += parsedData[finallist[c][xaxis]][2]
                    for yaxis in range(len(finallist[c])):
                        ytotalnumber += parsedData[finallist[c][yaxis]][3]
                    xaverage = xtotalnumber/len(finallist[c])
                    yaverage = ytotalnumber/len(finallist[c])
                    centroidvaluelist.append([xaverage,yaverage])
                    finallist[c]=[]
                for d in range(len(parsedData)):
                    if parsedData[d] != []:
                        minnumber = math.sqrt((centroidvaluelist[0][0]-parsedData[d][2])**2
                                     + (centroidvaluelist[0][1]-parsedData[d][3])**2)
                        indexformaxnumber = 0
                        for e in range(len(centroidvaluelist)):
                            if math.sqrt((centroidvaluelist[e][0]-parsedData[d][2])**2 + (centroidvaluelist[e][1]-parsedData[d][3])**2) < minnumber:
                                indexformaxnumber = e
                                minnumber = math.sqrt((centroidvaluelist[e][0]-parsedData[d][2])**2
                                         + (centroidvaluelist[e][1]-parsedData[d][3])**2)
                        finallist[indexformaxnumber].append(parsedData[d][0])
            return finallist
        except:
            return 'there is an error occured'
    def calculateSC(self,clusters,parsedData):
        try:
            scvalue = 0
            for clusterindex in range(len(clusters)):
                for numberincluster in range(len(clusters[clusterindex])):
                    anumber = 0
                    bnumberlist = []
                    '''calculate anumber'''
                    for othernumberincluster in range(len(clusters[clusterindex])):
                        if othernumberincluster != numberincluster:
                            c = clusters[clusterindex][numberincluster]
                            d = clusters[clusterindex][othernumberincluster]
                            anumber += math.sqrt((parsedData[c][2]-
                                                  parsedData[d][2])**2 +
                                                 (parsedData[c][3]-
                                                  parsedData[d][3])**2)
                    anumber = anumber/(len(clusters[clusterindex])-1)
                    '''calculate bnumber'''
                    for otherclusterindex in range(len(clusters)):
                        if otherclusterindex != clusterindex:
                            bnumber = 0
                            for othernumberinothercluster in range(len(clusters[otherclusterindex])):
                                parseddataindex = clusters[clusterindex][numberincluster]
                                otherclusterindexi = clusters[otherclusterindex][othernumberinothercluster]
                                bnumber += math.sqrt((parsedData[parseddataindex][2]-
                                                     parsedData[otherclusterindexi][2])**2 +
                                                    (parsedData[parseddataindex][3]-
                                                    parsedData[otherclusterindexi][3])**2)
                            bnumber = bnumber/(len(clusters[otherclusterindex]))
                            bnumberlist.append(bnumber)
                    minbnumber = min(bnumberlist)
                    s = (minbnumber - anumber)/max(minbnumber,anumber)
                    scvalue += s
            length = 0
            for numberofcluster in range(len(clusters)):
                length += len(clusters[numberofcluster])
            scvalue = scvalue/length
            return scvalue
        except:
            return 'SC value cannot be returned properly'


# In[32]:


'''km = MyKmeans()
rd = km.readData('digits-embedding.csv')
mylist = []
subsetdata = []
for i in range(len(rd)):
    if rd[i][1] == 2 or rd[i][1] == 4 or rd[i][1] == 6 or rd[i][1]==7:
        mylist.append(rd[i][0])
        subsetdata.append(rd[i])
    else:
        subsetdata.append([])
j = 1
for a in range(len(mylist)):
    classlabel = rd[mylist[a]][1]
    xaxis = rd[mylist[a]][2]
    yaxis = rd[mylist[a]][3]
    if classlabel == 2:
        plt.plot([xaxis],[yaxis],'ro',label='2')
    if classlabel == 4:
        plt.plot([xaxis],[yaxis],'ko',label='4')
    if classlabel == 6:
        plt.plot([xaxis],[yaxis],'yo',label='6')
    if classlabel == 7:
        plt.plot([xaxis],[yaxis],'go',label='7')
        if j == 1:
            plt.legend()
            j += 1
plt.title('Number Distribution')
plt.show()
clusters = km.cluster(subsetdata, iterCount=50, k=16, centroids=[])
print km.calculateSC(clusters,subsetdata)'''


# In[ ]:


'''plt.plot([2],[0.4890767461],'ro')
plt.plot([4],[0.5830137691],'yo')
plt.plot([8],[0.4712494508],'go')
plt.plot([16],[0.4085709711],'bo')
plt.title('Relation between K value and SC value')
plt.xlabel('K value')
plt.ylabel('SC value')
plt.show()'''


# In[36]:


'''km = MyKmeans()
rd = km.readData('digits-embedding.csv')
mylist = []
subsetdata = []
for i in range(len(rd)):
    if rd[i][1] == 6 or rd[i][1]==7:
        mylist.append(rd[i][0])
        subsetdata.append(rd[i])
    else:
        subsetdata.append([])
j = 1
clusters = km.cluster(subsetdata, iterCount=50, k=8, centroids=[])
print km.calculateSC(clusters,subsetdata)'''


# In[ ]:


'''plt.plot([2],[0.821833304671],'ro')
plt.plot([4],[0.613565616509],'yo')
plt.plot([8],[0.38626762722],'go')
plt.plot([16],[0.375335126119],'bo')
plt.title('Relation between K value and SC value')
plt.xlabel('K value')
plt.ylabel('SC value')
plt.show()'''


# In[38]:


'''km = MyKmeans()
rd = km.readData('digits-embedding.csv')
mylist = []
subsetdata = []
for i in range(len(rd)):
    if rd[i][1] == 2 or rd[i][1] == 4 or rd[i][1] == 6 or rd[i][1]==7:
        mylist.append(rd[i][0])
        subsetdata.append(rd[i])
    else:
        subsetdata.append([])
j = 1
for a in range(len(mylist)):
    classlabel = rd[mylist[a]][1]
    xaxis = rd[mylist[a]][2]
    yaxis = rd[mylist[a]][3]
    if classlabel == 6:
        plt.plot([xaxis],[yaxis],'yo',label='6')
    if classlabel == 7:
        plt.plot([xaxis],[yaxis],'go',label='7')
        if j == 1:
            plt.legend()
            j += 1
plt.title('Number Distribution')
plt.show()'''


# In[34]:


#Example in the handout
'''km = MyKmeans() #creating an object
parsedData = km.readData('digits-embedding.csv') #reading, parsing the data.
clusters = km.cluster(parsedData, iterCount=50, k=5, centroids=[]) #perform clustering with initially random centroids
SC = km.calculateSC(clusters,parsedData)
print SC'''


# In[30]:


'''km =MyKmeans()
parsedData = km.readData('digits-embedding.csv')
clusters = km.cluster(parsedData, iterCount=10, k=3, centroids=[10,20,30]) #perform clustering using the provided initial centroids
SC = km.calculateSC(clusters,parsedData) #c
print SC'''


# In[ ]:
