#!/usr/bin/python
#coding:utf-8

#把出现次数分别为1,2,3,4,5,6,7,8,9,10次的词频(1-gram、2-gram的词)分别输出到10个文件中去

import jieba
import re

allwords = {}

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
        word_before = ''
        for word in seg_list:
            if word.isdigit():
                continue

            if not allwords.__contains__(word):
                allwords[word] = 1
            else:
                allwords[word] += 1

            if word_before + word == word:
                pass
            elif not allwords.__contains__(word_before + word):
                allwords[word_before + word] = 1
            else:
                allwords[word_before + word] += 1

            word_before = word

    return

def main():
    loadwords(loadsentences())
    allwordsnew = sorted(allwords.iteritems(), key = lambda d:d[1], reverse=True)

    for m in range(10):
        file = open("data\\character_group\\vectoritems_wzp_%d.txt"%m,"w")
        for word in allwordsnew:
            if word[1] == m+1:
                file.write(word[0].encode("utf-8") + " %d"%word[1] + "\n")
        file.close()

    return

main()

