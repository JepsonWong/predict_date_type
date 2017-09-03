#!/usr/bin/python
#coding:utf-8

#日期类型：1.立案日期 2.撤诉日期 3.庭审日期 4.借款日期 5.偿还日期 6.其他日期 7.起诉日期 8.判决日期 9.付息日期 10.受理日期 11.本息计算截至日

#构建句子的特征矩阵，不包括距离特征。将特征矩阵提取到source_wzp_lda.txt,然后PMI筛选特征

import re
import jieba
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

vector = {}

def buildvector():
    #从已经提取好的vectoritem文件中将这些特征提取到vector{}中
    file = open("data\\vectoritems_lda.txt", "r")
    allwords = file.read().decode('utf-8')
    allwords = allwords.split("\n")

    #这里会有一个问题，allwords切分的时候，会多出一个空格，可能是最后\n后面的空格也被切分了
    for i in xrange(len(allwords)-1):
        allwords[i] = allwords[i].split(' ')[0]
        vector[allwords[i]] = 0

    file.close()
    return

def cleanvector():
    for item in vector:
        vector[item] = 0
    return

def parse(sentence):
    #将句子分词并加入vector{}
    sentence = sentence.decode('utf-8')
    subsentence = re.search(u"[^，。]*@.*@[^，。]*", sentence).group()
    sentence = re.sub("@.*@".decode('utf-8'), "@".decode('utf-8'), sentence)

    sentence = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~#￥%……&*（）《》／-：”“‰]+".decode('utf-8'), "".decode('utf-8'),
                      sentence)
    seg_list = jieba.cut(sentence)

    for word in seg_list:
        if word.isdigit():
            continue
        if vector.__contains__(word):
            vector[word] = 1
    return

def main():
    #从sentences.txt文件中读取标记好的句子，格式为“句子\t标签”
    #将特征矩阵提取到source_wzp_lda.txt
    vectorfile = open("data\\source_wzp_lda.txt", "w")
    sentencefile = open("data\\sentences.txt".decode('utf-8'), "r")

    buildvector()

    for item in vector:
        vectorfile.write("%s\t".encode('utf-8') % item)
    vectorfile.write("\n")

    file_new = open("data\\vectoritems_lda_1_new.txt", "w")
    for item in vector:
        file_new.write("%s\n".encode('utf-8') % item)
    file_new.close()

    print len(vector)

    sentence = sentencefile.read()
    sentences = sentence.split("\n")

    for sentence in sentences:
        sentence = sentence.split("\t")
        parse(sentence[0])

        print len(vector)

        for item in vector:
            vectorfile.write("%d\t" % (vector[item]))
        vectorfile.write("\n")
        cleanvector()
    vectorfile.close()
    sentencefile.close()
    return

main()
