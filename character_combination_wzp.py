#!/usr/bin/python
#coding:utf-8

#增加提取组合特征

import jieba
import re

words = []

def combination():
    global words
    file_combination = open("data\\vectoritems_combination_3.txt", "w")
    for i in range(len(words)-2):
        print i
        for j in range(i+1,len(words)-1):
            file_combination.write(words[i].encode('utf-8') + "#" +words[j].encode('utf-8') + "\n")
    file_combination.close()

def main():
    global words
    file = open("data\\important_character3.txt", "r")
    words = file.read().decode("utf-8").split("\n")
    print len(words)

    combination()

main()

