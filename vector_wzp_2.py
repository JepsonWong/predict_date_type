#!/usr/bin/python
#coding:utf-8

#用组合特征构建句子的特征矩阵。
#将特征矩阵提取到source_wzp_3.txt,然后PMI筛选特征

import re
import jieba
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

vector = {}

def buildvector():
    #从已经提取好的vectoritems_combination文件中将这些特征提取到vector{}中
    file = open("data\\vectoritems_combination_3.txt", "r")
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
    sentence = sentence.decode('utf-8')
    sentence = re.sub("@.*@".decode('utf-8'), "@".decode('utf-8'), sentence)
    sentence = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~#￥%……&*（）《》／-：”“‰]+".decode('utf-8'), "".decode('utf-8'),
                      sentence)

    for item in vector:
        yes0 = False
        yes1 = False
        items = item.split("#")

        seg_list = jieba.cut(sentence)
        word_before = ''
        for word in seg_list:
            if word.isdigit():
                continue
            word_seq = word_before+word
            if(items[0] == word or items[0] == word_seq):
                yes0 = True
            else:
                pass
            if(items[1] == word or items[1] == word_seq):
                yes1 = True
            else:
                pass
            word_before = word
        if(yes1 == True and yes0 == True):
            print "ok"
            vector[item] = 1
        else:
            vector[item] = 0
    '''
    seg_list = jieba.cut(sentence)
    word_before = ''
    for word in seg_list:
        if word.isdigit():
            continue
        if vector.__contains__(word):
            vector[word] = 1

        word_seq = word_before + word
        if vector.__contains__(word_seq):
            vector[word_seq] = 1
        word_before = word
    '''
    return

def main():
    #从sentences.txt文件中读取标记好的句子，格式为“句子\t标签”
    #将特征矩阵提取到source_wzp_3.txt
    vectorfile = open("data\\source_wzp_3.txt", "w")
    sentencefile = open("data\\sentences.txt".decode('utf-8'), "r")

    fileone = open("data\\vector_wzp_1.txt", "w")

    buildvector()

    for word in vector:
        fileone.write(word.encode('utf-8') + " %d" % vector[word] + "\n")
    fileone.close()

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

    vectorfile.close()
    sentencefile.close()
    return

main()