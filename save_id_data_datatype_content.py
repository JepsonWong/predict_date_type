#!/usr/bin/python
#coding:utf-8

import re
'''
import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="10246888", db="test", charset='utf8')
cursor = db.cursor()

def read_content(id):
    sql = "SELECT id, judgement_content FROM t_case_info WHERE id = %d" % id
    cursor.execute(sql)
    db.commit()
    list = cursor.fetchall()
    for var in list:
        caseid = var[0]
        print caseid
        var = var[1]
        if var == None:
            continue
        var = var.encode('utf-8')
        sentences = var.split("#P#")
        for sentence in sentences:
            pass
    pass

def main():
    for userid in range(100):
        read_content(userid)
'''
def istime(str):
    #判断该语句是否为包含时间信息的语句（不包含生日）
    str = str.decode('utf-8')
    if re.search(u"([0-9]+年)([0-9]+月)?([0-9]+日)?[^生]", str):
        indexbegin = str.find(re.search(u"([0-9]+年)([0-9]+月)?([0-9]+日)?", str).group())
        index = str.find(re.search(u"([0-9]+年)([0-9]+月)?([0-9]+日)?", str).group()) + len(re.search(u"([0-9]+年)([0-9]+月)?([0-9]+日)?", str).group())
        if not str[index:index+6] == u"出生" and not str[index:index+3] == u"生" and not str[indexbegin-6:indexbegin] == u"生于":
            return True
    return False

def time_split(str):
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
            print newdate
            print s
    return


def extract(str):
    list = re.split("\n", str)
    for sentence in list:
        if istime(sentence):
            if not re.search("[a-z]{2,}", sentence):
                time_split(sentence)
    return

file = open("data\\info.txt", "r")
while True:
    line = file.readline()
    if not line:
        break
    extract(line)