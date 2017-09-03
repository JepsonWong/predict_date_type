#!/usr/bin/python
#coding:utf-8

import jieba
import re

allwords = {}

stoplist = {}.fromkeys([ line.strip() for line in open("data/stopwords1.txt") ])

def loadsentences():
    file = open("data\\sentences.txt".decode('utf-8'), "r")
    str = file.read()
    file.close()
    return str

def loadwords(str):
    sentences = str.split("\n")
    for sentence in sentences:
        sentence = sentence.decode('utf-8')
        sentence = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）《》／-；：”“‰【:］［-]+".decode('utf-8'), "".decode('utf-8'), sentence)
        seg_list = jieba.cut(sentence)
        for word in seg_list:
            if word.isdigit():
                continue
            if word in stoplist:
                continue

            if not allwords.__contains__(word):
                allwords[word] = 1
            else:
                allwords[word] += 1
    return

def main():
    file = open("data\\vectoritems_lda.txt", "w")
    file1 = open("data\\vectoritems_lda_1.txt", "w")
    loadwords(loadsentences())

    allwordsnew = sorted(allwords.iteritems(), key=lambda d: d[1], reverse=True)
    for word in allwordsnew:
        #if word[1] > 10:  # 提取一定频率的词语
        file.write(word[0].encode('utf-8') + " %d" % word[1] + "\n")
        file1.write(word[0].encode('utf-8') + "\n")

    file.close()
    return

main()

