# !/usr/bin/python
# coding:utf-8

import MySQLdb

# connect datebase
db = MySQLdb.connect(host="127.0.0.1", user="root", db="test", charset='utf8')
cursor = db.cursor()

file_info = open("data\\t_case_info.txt","w")

def read_content(id):
    global file_info
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
        file_info.write("%d"%caseid + "\t" + "%s\n"%var)
        print caseid
        print var

def main():
    for userid in range(858663):
        read_content(userid)

main()
file_info.close()
