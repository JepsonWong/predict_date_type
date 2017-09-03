#!/usr/bin/python
#coding:utf-8

import jieba.posseg as psg

text = u"我和王非去北京大学玩"
seg = psg.cut(text)
print type(seg)
for ele in seg:
    if ele.flag == 'nr' or ele.flag == 'ns' or ele.flag == 'nt' or ele.flag == 'nz':
        print ele.word, ele.flag

#nr 人名
#ns 地名
#nt 机构团体
#nz 其他专名


