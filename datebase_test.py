# !/usr/bin/python
# coding:utf-8 -*-

import MySQLdb

db = MySQLdb.connect(host="127.0.0.1", user="root", db="test", charset='utf8')
cursor = db.cursor()

id = 1

idd = u"yes"

sql = "INSERT IGNORE INTO sss VALUES (%d, '%s')" % (id, idd)
cursor.execute(sql)
db.commit()

