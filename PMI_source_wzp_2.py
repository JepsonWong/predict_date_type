#!/usr/bin/python
#coding:utf-8

from sklearn import metrics as mr
import numpy as np

X = []

#features is a array
def selectFeature1(features,label):
    print type(features)
    x = []
    s=[]
    print "compute multual begin!"
    for i in range(len(features[0])):
        for j in range(len(features)):
            x.append(features[j][i])#2899 numbers;
        s.append(mr.mutual_info_score(label,x))#10000 numbers
        x[:] = []
    print "compute multual end!"

    print len(s)

    m = []
    for i in range(len(s)):
        if s[i]<0.050:
            m.append(False)
        else:
            m.append(True)
    print len(m)

    file = open("data\\PMI_important_word_2.txt","a")
    for i in range(len(m)):
        if m[i]==True:
            file.write("1" + "\n")
        if m[i]==False:
            file.write("0" + "\n")

    features = features[:, np.array(m)]

    print features.shape

#features is a list
def selectFeature(features,label):
    x = []
    s=[]
    print "compute multual begin!"
    for i in range(len(features[0])):
        for j in range(len(features)):
            x.append(features[j][i])#2899 numbers;
        s.append(mr.mutual_info_score(label,x))#10000 numbers
        x[:] = []
    print "compute multual end!"

    print len(s)
    m = 0
    for i in range(len(s)):#10000 numbers
        #print "i:%d"%i
        if s[i]<0.050:
            m = m + 1
            for j in range(len(features)):#2899 numbers
                #print "j:%d"%j
                del features[j][i-m]# #(features[j]).remove(features[j][i])

    print len(features)#2899
    print len(features[0])#10000 转变为3326

print "read begin!"
y = np.genfromtxt("data\\target_wzp.txt",skip_header=1,dtype = np.float32)
print len(y)
X = np.genfromtxt("data\\source_wzp_2_10000.txt",dtype = np.float32)
print X.shape
print "read end!"

#selectFeature(X.tolist(),y)
selectFeature1(X,y)