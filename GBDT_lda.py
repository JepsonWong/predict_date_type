#!/usr/bin/python
#coding:utf-8

#本程序可以用于计算每一个特征（在特征矩阵中）所占比重的分值计算

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import lda

#the vocab
file_vocab = open("data\\vectoritems_lda_3_new.txt", "r")
vocab = (file_vocab.read().decode("utf-8").split("\n"))[0:-1]
print len(vocab)

gbdt = GradientBoostingClassifier(
    init=None,
    learning_rate=0.1,
    loss='deviance',
    max_depth=3,
    max_features=None,
    max_leaf_nodes=None,
    min_samples_leaf=1,
    min_samples_split=2,
    min_weight_fraction_leaf=0.0,
    n_estimators=100,
    random_state=None,
    subsample=1.0,
    verbose=0,
    warm_start=False)

#在使用这个方法的时候要注意，他会把整个文件都读进去，而vector.py会有一行标签，建议手动删除
X = np.genfromtxt("data\\source_wzp_lda_1.txt",skip_header=1,dtype = np.int)
y = np.genfromtxt("data\\target_wzp.txt",skip_header=1,dtype = np.int)

print X.shape
print y.shape

gbdt.fit(X, y)

score = gbdt.feature_importances_
print gbdt.feature_importances_.shape
print score

m = []
w = []
for i in range(len(score)):
    if score[i] <= 0:
        m.append(False)
    else:
        m.append(True)
        w.append(vocab[i])
print len(m)
print len(w)

#new_feature = gbdt.apply(X)
#print X.shape
#print new_feature.shape

#var = (gbdt.feature_importances_>0).shape
#print var
#new_train_data = train_data[:, gbdt.feature_importances_>0]

file_gbdt_lda = open("data\\gbdt_lda.txt","w")
for i in range(len(vocab)):
    print vocab[i]
    file_gbdt_lda.write(vocab[i].encode("utf-8") + "\t" + "%lf"%(score[i]))
    file_gbdt_lda.write("\n")
file_gbdt_lda.close()

file_gbdt_lda1 = open("data\\gbdt_lda1.txt","w")
word_sorted = np.array(vocab)[np.argsort(score)]
score = sorted(score, reverse=False)

for i in range(len(word_sorted)):
    file_gbdt_lda1.write(word_sorted[i].encode("utf-8")+"\t"+"%lf"%(score[i]))
    file_gbdt_lda1.write("\n")
file_gbdt_lda1.close()

new_X = X[:, np.array(m)]
print new_X.shape

#lda
print "lda!!!"
#指定11个主题，1000次迭代
model = lda.LDA(random_state=1, n_topics=11, n_iter=1000)
model.fit(new_X)

#主题-单词（topic-word）分布
topic_word = model.topic_word_
print("type(topic_word): {}".format(type(topic_word)))
print("shape: {}".format(topic_word.shape))

#获取每个topic下权重最高的10个单词
n = 10
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(w)[np.argsort(topic_dist)][:-(n+1):-1]
    print("topic {}\n- {}".format(i, ('-'.join(topic_words)).encode("utf-8")))

#文档主题(Document-Topic)分布：
doc_topic = model.doc_topic_
print("type(doc_topic): {}".format(type(doc_topic)))
print("shape: {}".format(doc_topic.shape))

#一篇文章对应一行，每行的和为1
#输入前10篇文章最可能的Topic
for n in range(20):
    topic_most_pr = doc_topic[n].argmax()
    print("doc: {} topic: {}".format(n, topic_most_pr))



