#!/usr/bin/python
#coding:utf-8

vectorfile = open("data\\source_wzp_2.txt", "r")
vectorfile.readline()
vectorfile_split = [0,0,0]
for i in range(3):
    vectorfile_split[i] = open("data\\source_wzp_2_%d.txt"%(i*10000+10000), "w")

n=0
while(True):
    sentance = vectorfile.readline().replace("\n","")
    sentance = sentance[:-1]
    if not sentance:
        break
    sentences = sentance.split("\t")

    for i in range(3):
        split = sentences[i*10000:i*10000+10000]
        #print len(split)
        for item in split:
            vectorfile_split[i].write("%f\t" % (float(item)))
        vectorfile_split[i].write("\n")
    n = n+1
    print n

for i in range(3):
    vectorfile_split[i].close()
