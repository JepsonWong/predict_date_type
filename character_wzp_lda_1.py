#!/usr/bin/python
#coding:utf-8

import jieba.posseg as psg
import re

allwords = {}

stoplist = {}.fromkeys([ line.strip() for line in open("data/stopwords1.txt") ])

def loadsentences():
    file = open("data\\sentences.txt".decode('utf-8'), "r")
    str = file.read()
    file.close()
    return str

#nr 人名
#ns 地名
#nt 机构团体
#nz 其他专名
def loadwords(str):
    sentences = str.split("\n")
    for sentence in sentences:
        sentence = sentence.decode('utf-8')
        sentence = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）《》／-；：”“‰【:］［-]+".decode('utf-8'), "".decode('utf-8'), sentence)
        seg_list = psg.cut(sentence)
        for word1 in seg_list:
            if word1.word.isdigit():
                continue
            if word1.word in stoplist:
                continue
            if word1.flag == 'nr' or word1.flag == 'ns' or word1.flag == 'nt' or word1.flag == 'nz':
                continue

            if not allwords.__contains__(word1.word):
                allwords[word1.word] = 1
            else:
                allwords[word1.word] += 1
    return

def main():
    file = open("data\\vectoritems_lda_2.txt", "w")
    file1 = open("data\\vectoritems_lda_3.txt", "w")
    loadwords(loadsentences())

    allwordsnew = sorted(allwords.iteritems(), key=lambda d: d[1], reverse=True)
    for word in allwordsnew:
        #if word[1] > 10:  # 提取一定频率的词语
        file.write(word[0].encode('utf-8') + " %d" % word[1] + "\n")
        file1.write(word[0].encode('utf-8') + "\n")

    file.close()
    return

main()

