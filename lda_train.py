#!/usr/bin/python
# coding:utf-8

import numpy as np
import lda

X = np.genfromtxt("data\\source_wzp_lda.txt", skip_header=1, dtype = np.int)

#the vocab
file_vocab = open("data\\vectoritems_lda_1_new.txt", "r")
vocab = (file_vocab.read().decode("utf-8").split("\n"))[0:-1]
print len(vocab)

#指定11个主题，1000次迭代
model = lda.LDA(random_state=1, n_topics=11, n_iter=1000)
model.fit(X)

#主题-单词（topic-word）分布
topic_word = model.topic_word_
print("type(topic_word): {}".format(type(topic_word)))
print("shape: {}".format(topic_word.shape))

#获取每个topic下权重最高的10个单词
n = 10
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
    print("topic {}\n- {}".format(i, ('-'.join(topic_words)).encode("utf-8")))

#文档主题(Document-Topic)分布：
doc_topic = model.doc_topic_
print("type(doc_topic): {}".format(type(doc_topic)))
print("shape: {}".format(doc_topic.shape))

#一篇文章对应一行，每行的和为1
#输入前10篇文章最可能的Topic
for n in range(20):
    '''
    for i in doc_topic[n]:
        print i
        '''
    topic_most_pr = doc_topic[n].argmax()
    print("doc: {} topic: {}".format(n, topic_most_pr))
