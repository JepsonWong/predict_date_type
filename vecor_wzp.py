#!/usr/bin/python
#coding:utf-8

#日期类型：1.立案日期 2.撤诉日期 3.庭审日期 4.借款日期 5.偿还日期 6.其他日期 7.起诉日期 8.判决日期 9.付息日期 10.受理日期 11.本息计算截至日

import re
import jieba
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

stopwords = {"的", "了"}
vector = {}

def buildvector():
    #从已经提取好的vectoritem文件中将这些特征提取到vector{}中
    file = open("data\\vectoritems_wzp_10.txt", "r")
    allwords = file.read().decode('utf-8')
    allwords = allwords.split("\n")

    vector['position'] = 0

    #print len(allwords)
    #这里会有一个问题，allwords切分的时候，会多出一个空格，可能是最后\n后面的空格也被切分了
    for i in xrange(len(allwords)-1):
        allwords[i] = allwords[i].split(' ')[0]
        if stopwords.__contains__(allwords[i]):
            continue
        vector[allwords[i] + '3'] = 0
        vector[allwords[i] + '6'] = 0
        vector[allwords[i]] = 0
        vector[allwords[i] + 'whole'] = 0

    '''
    for word in allwords:
        word = word.split(' ')[0]
        if stopwords.__contains__(word):
            continue
        vector[word+'3'] = 0
        vector[word+'6'] = 0
        vector[word] = 0
        vector[word+'whole'] = 0
    '''
    return

def cleanvector():
    for item in vector:
        vector[item] = 0
    return

def datatype(str):
    if str == "立案日期":
        return 1
    elif str == "撤诉日期":
        return 2
    elif str == "庭审日期":
        return 3
    elif str == "借款日期":
        return 4
    elif str == "偿还日期":
        return 5
    elif str == "起诉日期":
        return 7
    elif str == "判决日期":
        return 8
    elif str == "付息日期":
        return 9
    elif str == "受理日期":
        return 10
    elif str == "本息计算截止日":
        return 11
    else:
        return 6

def parse(sentence):
    #将句子分词并加入vector{}
    sentence = sentence.decode('utf-8')
    subsentence = re.search(u"[^，。]*@.*@[^，。]*", sentence).group()
    sentence = re.sub("@.*@".decode('utf-8'), "@".decode('utf-8'), sentence)

    vector['position'] = float(subsentence.find("@")) / len(subsentence)

    sentence = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~#￥%……&*（）《》／-：”“‰]+".decode('utf-8'), "".decode('utf-8'),
                      sentence)
    seg_list = jieba.cut(sentence)
    word_before = ''
    word_before_actual = ''
    for word in seg_list:
        if word.isdigit():
            word_before_actual = word_before_actual + word
            continue
        if vector.__contains__(word):
            vector[word+'whole'] = 1
            distance = sentence.find(word) - sentence.find("@")
            if distance >= -3 and distance <= 3:
                vector[word+'3'] = 1
            if distance >= -6 and distance <= 6:
                vector[word+'6'] = 1
            if subsentence.find(word) >= 0:
                vector[word] = 1

        word_seq = word_before + word
        word_seq_actual = word_before_actual + word
        '''
        if vector.__contains__(word_seq):
            if vector.__contains__(word_seq + 'whole'):
                vector[word_seq + 'whole'] = 1
            else:
                pass
                #print word_seq + 'whole'
            distance = sentence.find(word_seq) - sentence.find("@")
            if distance >= -3 and distance <= 3:
                if vector.__contains__(word_seq + '3'):
                    vector[word_seq + '3'] = 1
                else:
                    pass
                    print word_before
                    print word
                    #print word_seq + '3'
            if distance >= -6 and distance <= 6:
                if vector.__contains__(word_seq + '6'):
                    vector[word_seq + '6'] = 1
                else:
                    pass
                    #print word_seq + '6'
            if subsentence.find(word_seq) >= 0:
                if vector.__contains__(word_seq):
                    vector[word_seq] = 1
                else:
                    pass
                    #print word_seq
        '''
        if vector.__contains__(word_seq):
            if vector.__contains__(word_seq + 'whole'):
                vector[word_seq + 'whole'] = 1
            else:
                pass
                print word_seq + 'whole'
            distance = sentence.find(word_seq_actual) - sentence.find("@")
            if distance >= -3 and distance <= 3:
                if vector.__contains__(word_seq + '3'):
                    vector[word_seq + '3'] = 1
                else:
                    pass
                    print word_seq + '3'
            if distance >= -6 and distance <= 6:
                if vector.__contains__(word_seq + '6'):
                    vector[word_seq + '6'] = 1
                else:
                    pass
                    print word_seq + '6'
            if subsentence.find(word_seq_actual) >= 0:
                if vector.__contains__(word_seq):
                    vector[word_seq] = 1
                else:
                    pass
                    print word_seq

        word_before = word
        word_before_actual = word
    return

def main():
    #从sentences.txt文件中读取标记好的句子，格式为“句子\t标签”
    #将特征矩阵提取到vector.txt
    #将标签矩阵提取到target.txt
    vectorfile = open("data\\source_wzp.txt", "w")
    targetfile = open("data\\target_wzp.txt", "w")
    sentencefile = open("data\\sentences.txt".decode('utf-8'), "r")

    fileone = open("data\\vector_wzp.txt", "w")

    buildvector()

    for word in vector:
        fileone.write(word.encode('utf-8') + "\n")

    fileone.close()


    for item in vector:
        vectorfile.write("%s\t".encode('utf-8') % item)
    targetfile.write("日期类型".encode('utf-8') + "\n")
    vectorfile.write("\n")

    sentence = sentencefile.read()
    sentences = sentence.split("\n")
    #print len(sentences)

    for sentence in sentences:
        sentence = sentence.split("\t")
        parse(sentence[0])

        for item in vector:
            vectorfile.write("%f\t" % (vector[item]))
        targetfile.write("%d" % (datatype(sentence[1])) + "\n")
        vectorfile.write("\n")
        cleanvector()
    vectorfile.close()
    sentencefile.close()
    targetfile.close()
    return

main()

