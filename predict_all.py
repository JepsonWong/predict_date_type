# !/usr/bin/python
# coding:utf-8

from jieba import posseg as psg
import jieba
import numpy as np
import re
from sklearn.externals import joblib

feature = []
feature_number = []
sentences = []

def date2type (str):
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

def type2date(str):
    if str == 1:
        return "立案日期"
    elif str == 2:
        return "撤诉日期"
    elif str == 3:
        return "庭审日期"
    elif str == 4:
        return "借款日期"
    elif str == 5:
        return "偿还日期"
    elif str == 7:
        return "起诉日期"
    elif str == 8:
        return "判决日期"
    elif str == 9:
        return "付息日期"
    elif str == 10:
        return "受理日期"
    elif str == 11:
        return "本息计算截止日"
    else:
        return "其他日期"

def clear_feature_number():
    global feature_number
    for i in range(len(feature_number)-1):
        feature_number[i] = 0

def istime(str):
    # 判断该语句是否为包含时间信息的语句（不包含生日）
    if re.search("([0-9]+年)([0-9]+月)?([0-9]+日)?[^生]", str):
        indexbegin = str.find(re.search("([0-9]+年)([0-9]+月)?([0-9]+日)?", str).group())
        index = str.find(re.search("([0-9]+年)([0-9]+月)?([0-9]+日)?", str).group()) + len(re.search("([0-9]+年)([0-9]+月)?([0-9]+日)?", str).group())
        if not str[index:index+6] == "出生" and not str[index:index+3] == "生" and not str[indexbegin-6:indexbegin] == "生于":
            return True
    return False

def time_split(str):
    # 前后30个汉字直到标点
    global sentences
    str = str.decode('utf-8')################################ 自己输入的也要decode？
    list = re.findall(u"([0-9]+年)([0-9]+月)?([0-9]+日)?", str)
    for date in list:# 返回列表
        newdate = ''
        for d in date:# 返回元组
            newdate += d
        segment = re.findall(u"[^，。]*.{0,30}"+newdate+u".{0,30}[^，。]*", str)
        for s in segment:
            s = s.replace(newdate, "@"+newdate+"@", 2)
            sentences.append(s)
    return

# src为原字符串,sub为寻找的子串,start为开始寻找位置,sublist为所有字串位置。x为另一个子串的位置。
def find_sub_str(src, sub, start, sublist, x):
    index = src.find(sub, start)
    while index != -1:
        sublist.append(index-x)
        index = src.find(sub, index + 1)

def find(src,sub,x):
    # a是原来的字符串，b是复制的字符串。
    a = []
    b = []
    find_sub_str(src, sub, 0, a, x)
    #print a
    for i in a:
        b.append(i)

    for i in xrange(len(a)):
        a[i] = abs(a[i])
    # print a
    a.sort()
    # print a
    # print b
    for i in xrange(len(b)):
        if abs(b[i]) == a[0]:
            return b[i]

def generate_feature(sentence):
    global feature
    global feature_number
    # 对每个日期，形成特征矩阵
    subsentence = re.search(u"[^，。]*@.*@[^，。]*", sentence).group()
    sentence = re.sub("@.*@".decode('utf-8'), "@".decode('utf-8'), sentence)
    feature_number[feature.index('position')] = float(subsentence.find("@")) / len(subsentence)
    sentence = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~#￥%……&*（）《》／-：”“‰]+".decode('utf-8'), "".decode('utf-8'),
                      sentence)
    seg_list = psg.cut(sentence)
    seg_list1 = jieba.cut(sentence)
    word_before = ''
    word_before_actual = ''
    for word in seg_list1:
        if word.isdigit():
            word_before_actual = word_before_actual + word
            continue
        if word in feature:
            # print "word ok"
            feature_number[feature.index(word+'whole')] = 1
            distance = sentence.find(word) - sentence.find("@")
            if distance >= -3 and distance <= 3:
                feature_number[feature.index(word+'3')] = 1
            if distance >= -6 and distance <= 6:
                feature_number[feature.index(word+'6')] = 1
            if subsentence.find(word) >= 0:
                feature_number[feature.index(word)] = 1
        word_seq = word_before + word
        word_seq_actual = word_before_actual + word
        if word_seq in feature:
            # print "word_seq ok"
            if word_seq + 'whole' in feature:
                feature_number[feature.index(word_seq + 'whole')] = 1
            else:
                pass
                print word_seq + 'whole'
            distance = sentence.find(word_seq_actual) - sentence.find("@")
            if distance >= -3 and distance <= 3:
                if word_seq + '3' in feature:
                    feature_number[feature.index(word_seq + '3')] = 1
                else:
                    pass
                    print word_seq + '3'
            if distance >= -6 and distance <= 6:
                if word_seq + '6' in feature:
                    feature_number[feature.index(word_seq + '6')] = 1
                else:
                    pass
                    print word_seq + '6'
            if subsentence.find(word_seq_actual) >= 0:
                if word_seq in feature:
                    feature_number[feature.index(word_seq)] = 1
                else:
                    pass
                    print word_seq

        word_before = word
        word_before_actual = word

    for item in feature[9480:12255]:
        yes0 = False
        yes1 = False
        items = item.split("#")
        word_before = ''
        for word in seg_list1:
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
            #print "combination ok"
            feature_number[feature.index(item)] = 1
        else:
            feature_number[feature.index(item)] = 0

    distances = []
    words = []
    flags = []
    for i in seg_list:
        if (i.word).isdigit():
            continue
        distance = find(sentence, i.word, sentence.find("@"))
        words.append(i.word)
        distances.append(distance)
        flags.append(i.flag)
    words_sorted = np.array(words)[np.argsort(distances)]
    flags_sorted = np.array(flags)[np.argsort(distances)]
    distances.sort()
    for i in xrange(len(distances)):
        if distances[i] == 0:
            if ((i - 1) >= 0 and (i - 2) >= 0 and (i - 3) >= 0 and distances[i - 1] == distances[i - 2]):
                feature_number[feature.index("1" + "%s" % flags_sorted[i - 3])] = 1
                # print words_sorted[i - 3], flags_sorted[i - 3], distances[i - 3]
            else:
                if (i - 2) >= 0:
                    feature_number[feature.index("1" + "%s" % flags_sorted[i - 2])] = 1
                    # print words_sorted[i - 2], flags_sorted[i - 2], distances[i - 2]
            if (i - 1) >= 0:
                feature_number[feature.index("2" + "%s" % flags_sorted[i - 1])] = 1
                # print words_sorted[i - 1], flags_sorted[i - 1], distances[i - 1]
            if (i + 1) < len(distances):
                feature_number[feature.index("3" + "%s" % flags_sorted[i + 1])] = 1
                # print words_sorted[i + 1], flags_sorted[i + 1], distances[i + 1]
            if ((i + 1) < len(distances) and (i + 2) < len(distances) and (i + 3) < len(distances) and distances[
                    i + 1] == distances[i + 2]):
                feature_number[feature.index("4" + "%s" % flags_sorted[i + 3])] = 1
                # print words_sorted[i + 3], flags_sorted[i + 3], distances[i + 3]
            else:
                if (i + 2) < len(distances):
                    feature_number[feature.index("4" + "%s" % flags_sorted[i + 2])] = 1
                    # print words_sorted[i + 2], flags_sorted[i + 2], distances[i + 2]

# feature
vector_wzp = open("data\\vector_wzp.txt","r")
feature1 = vector_wzp.read().decode("utf-8").split("\n")
print  len(feature1)
for i in range(len(feature1)-1):
    feature.append(feature1[i])
    feature_number.append(0)
vector_wzp.close()

vector_wzp_1 = open("data\\vector_wzp_1.txt","r")
feature2 = vector_wzp_1.read().decode("utf-8").split("\n")
print len(feature2)
for i in range(len(feature2)-1):
    m = feature2[i].split(" ")
    feature.append(m[0])
    feature_number.append(0)
vector_wzp_1.close()

vector_wzp_flag = open("data\\vector_wzp_flag.txt","r")
feature3 = vector_wzp_flag.read().decode("utf-8").split("\n")
print len(feature3)
for i in range(len(feature3)-1):
    feature.append(feature3[i])
    feature_number.append(0)
vector_wzp_flag.close()

print len(feature)
print len(feature_number)

strings = []

while(1):
    # input sentence
    string = raw_input("please input your sentence：")
    if string == "no":
        break
    strings.append(string)

for i in strings:
    if istime(i):
        if not re.search("[a-z]{2,}", i):
            print "1"
            print i
            time_split(i)

feature_importances = []
importance = open("data\\feature_importances.txt", "r")
importances = importance.read().split("\n")

X = []
x = []

# test sentences
for i in sentences:
    print "2"
    print i
    # generate feature
    generate_feature(i)

    for m in range(len(importances) - 1):
        if int(importances[m]) == 0:
            pass
        if int(importances[m]) == 1:
            x.append(feature_number[m])

    X.append(x)
    x = []
    clear_feature_number()

if len(sentences) > 0:
    # get model
    clf = joblib.load("train_model.m")
    # X = np.array(X)[:, feature_importances]
    result = clf.predict(X)
    for i in result:
        type2date(i)
else:
    print "no sentence!"
