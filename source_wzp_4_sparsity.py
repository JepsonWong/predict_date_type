#!/usr/bin/python
#coding:utf-8

vector = []

file = open("data\\source_wzp_4.txt","r")
file.readline().decode('utf-8')

file1 = open("data\\vectoritems_combination_2.txt", "r")
allword = file1.read().decode('utf-8')
allwords = allword.split("\n")
#这里会有一个问题，allwords切分的时候，会多出一个空格，可能是最后\n后面的空格也被切分了
for i in xrange(len(allwords)-1):
    vector.append(allwords[i])

print len(vector)

file2 = open("data\\vectoritems_combination_has1.txt","w")

while(True):
    s = file.readline().decode('utf-8')
    if not s:
        break

    s_all = s.strip("\n").strip("\t").split("\t")
    m = 0
    for i in range(len(s_all)):
        if float(s_all[i]) == 1:
            print vector[i]
            #file2.write("%s\n".encode('utf-8') % vector[i])
            file2.write(vector[i].encode('utf-8') + "\n")
            m = m + 1
    if(m!=0):
        print m
    pass

file.close()
file1.close()
file2.close()