#!/usr/bin/python
#coding:utf-8

#用组合特征构建句子的特征矩阵。
#将特征矩阵提取到source_wzp_4.txt,然后PMI筛选特征

import re
import jieba
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

vector = {}
word_list = []
word_list_combination = []

def buildvector():
    #从已经提取好的vectoritems_combination文件中将这些特征提取到vector{}中
    file = open("data\\vectoritems_combination_2.txt", "r")
    allwords = file.read().decode('utf-8')
    allwords = allwords.split("\n")

    #这里会有一个问题，allwords切分的时候，会多出一个空格，可能是最后\n后面的空格也被切分了
    for i in xrange(len(allwords)-1):
        vector[allwords[i]] = 0
    return

def cleanvector():
    for item in vector:
        vector[item] = 0
    return

def parse(sentence):
    #将句子分词并加入vector{}
    global vector
    global word_list
    global word_list_combination
    sentence = sentence.decode('utf-8')
    sentence = re.sub("@.*@".decode('utf-8'), "@".decode('utf-8'), sentence)
    sentence = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~#￥%……&*（）《》／-：”“‰]+".decode('utf-8'), "".decode('utf-8'),
                      sentence)

    seg_list1 = jieba.cut(sentence)
    word_before = ''
    for word in seg_list1:
        if word.isdigit():
            continue
        word_seq = word_before + word
        if(word not in word_list):
            word_list.append(word)
        if(word not in word_list):
            word_list.append(word_seq)
        word_before = word

    for i in range(len(word_list)-1):
        for j in range(i+1,len(word_list)):
            w = word_list[i]+"#"+word_list[j]
            if(w not in word_list_combination):
                word_list_combination.append(w)

    i = 0
    for item in vector:
        if(item in word_list_combination):
            vector[item] = 1
            i = i + 1
        else:
            vector[item] = 0
    print i
    return

def main():
    #从sentences.txt文件中读取标记好的句子，格式为“句子\t标签”
    #将特征矩阵提取到source_wzp_3.txt
    vectorfile = open("data\\source_wzp_4.txt", "w")
    sentencefile = open("data\\sentences.txt".decode('utf-8'), "r")

    buildvector()

    for item in vector:
        vectorfile.write("%s\t".encode('utf-8') % item)
    vectorfile.write("\n")

    print len(vector)

    sentence = sentencefile.read()
    sentences = sentence.split("\n")

    for sentence in sentences:
        sentence = sentence.split("\t")
        parse(sentence[0])

        print len(vector)

        for item in vector:
            vectorfile.write("%f\t" % (vector[item]))
        vectorfile.write("\n")
        cleanvector()
        word_list[:] = []
        word_list_combination[:] = []


    vectorfile.close()
    sentencefile.close()
    return

main()