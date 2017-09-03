#!/usr/bin/python
#coding:utf-8

file = open("data\\PMI_important_word_1.txt","r")
fileall = file.read().split("\n")
print len(fileall)
file.close()

word = open("data\\vector_wzp_2.txt","r")
wordall = word.read().decode('utf-8').split("\n")
print len(wordall)
word.close()

important = open("data\\important_character3.txt","w")

for i in range(len(fileall)-1):
    if(int(fileall[i]) == 1):
        wordall[i] = wordall[i].split(" ")
        important.write(wordall[i][0].encode("utf-8") + "\n")

important.close()