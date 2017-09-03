#!/usr/bin/python
#coding:utf-8

#本程序在语句中针对出现的时间信息根据不同的规则提取相应的周围信息

import re

def extract(str):
    list = re.split("\n", str)
    for sentence in list:
        if istime(sentence):
            if not re.search("[a-z]{2,}", sentence):
                time_split_2(sentence)
    return

def time_split_1(str):
    #从后向前找到每一个时间前的逗号作为分割符
    num = 50
    count = 0
    list = re.split("，|：|（|）", str)
    for s in list:
        if re.search("([0-9]+年)([0-9]+月)?([0-9]+日)?", s):
            count += 1
    if count > 1:
        list = re.findall("([0-9]+年)([0-9]+月)?([0-9]+日)?", str)
        length = len(list) - 1
        index = 0
        while length > 1:
            temp = ''
            for word in list[length]:
                temp += word
            index = str.find(temp)
            while not str[index - 3:index] == "，":
                index -= 1
            print str[index:]
            length -= 1
        if index > 0:
            print str[:index]
    else:
        print str

def time_split_2(str):
    #前后30个汉字直到标点
    str = str.decode('utf-8')
    list = re.findall(u"([0-9]+年)([0-9]+月)?([0-9]+日)?", str)
    for date in list:#返回列表
        newdate = ''
        for d in date:#返回元组
            newdate += d
        segment = re.findall(u"[^，。]*.{0,30}"+newdate+u".{0,30}[^，。]*", str)
        for s in segment:
            s = s.replace(newdate, "@"+newdate+"@", 2)
            print s
    return

def time_split_3(str):
    #前后五小句
    str = str.decode('utf-8')
    list = re.findall(u"([0-9]+年)([0-9]+月)?([0-9]+日)?", str)
    for date in list:
        newdate = ''
        for d in date:
            newdate += d
        segment = re.search(u"([^：。；，：“”（）、？《》]*[：。；，：“”（）、？《》]){,5}[^，。]*"+newdate+u"([^：。；，：“”（）、？《》]*[：。；，：“”（）、？《》]){,5}", str).group()
        segment = segment.replace(newdate, "@" + newdate + "@")
        print segment
    return

def istime(str):
    #判断该语句是否为包含时间信息的语句（不包含生日）
    if re.search("([0-9]+年)([0-9]+月)?([0-9]+日)?[^生]", str):
        indexbegin = str.find(re.search("([0-9]+年)([0-9]+月)?([0-9]+日)?", str).group())
        index = str.find(re.search("([0-9]+年)([0-9]+月)?([0-9]+日)?", str).group()) + len(re.search("([0-9]+年)([0-9]+月)?([0-9]+日)?", str).group())
        if not str[index:index+6] == "出生" and not str[index:index+3] == "生" and not str[indexbegin-6:indexbegin] == "生于":
            return True
    return False

def ismoney(str):
    if re.search("[0-9]+(万)?元", str):
        return True
    return False

def main():
    file = open("data\\judgements.txt", "r")
    while True:
        line = file.readline()
        extract(line)
        if not line:
            break
    return


main()