#!/usr/bin/python
#coding:utf-8

from sklearn import metrics as mr
import numpy as np
import lda

#the vocab
file_vocab = open("data\\vectoritems_lda_3_new.txt", "r")
global vocab
vocab = (file_vocab.read().decode("utf-8").split("\n"))[0:-1]
print len(vocab)

#features is a array
def selectFeature1(features,label):
    global vocab
    print type(features)
    x = []
    s=[]
    print "compute multual begin!"
    for i in range(len(features[0])):
        for j in range(len(features)):
            x.append(features[j][i])#2899 numbers;
        s.append(mr.mutual_info_score(label,x))#10000 numbers
        x[:] = []
    print "compute multual end!"

    print len(s)

    m = []
    w = []
    for i in range(len(s)):
        if s[i]<0.010:
            m.append(False)
        else:
            m.append(True)
            w.append(vocab[i])
    print len(m)

    features = features[:, np.array(m)]

    print features.shape

    ################################
    pmi_lda = open("data\\pmi_lda.txt", "w")
    for i in range(len(vocab)):
        print vocab[i]
        pmi_lda.write(vocab[i].encode("utf-8") + "\t" + "%lf" % (s[i]))
        pmi_lda.write("\n")
    pmi_lda.close()

    pmi_lda1 = open("data\\pmi_lda1.txt", "w")
    word_sorted = np.array(vocab)[np.argsort(s)]
    s = sorted(s, reverse=False)

    for i in range(len(word_sorted)):
        pmi_lda1.write(word_sorted[i].encode("utf-8") + "\t" + "%lf" % (s[i]))
        pmi_lda1.write("\n")
    pmi_lda1.close()

    # lda
    print "lda!!!"
    # 指定11个主题，1000次迭代
    model = lda.LDA(random_state=1, n_topics=11, n_iter=1000)
    model.fit(features)

    # 主题-单词（topic-word）分布
    topic_word = model.topic_word_
    print("type(topic_word): {}".format(type(topic_word)))
    print("shape: {}".format(topic_word.shape))

    # 获取每个topic下权重最高的10个单词
    n = 10
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(w)[np.argsort(topic_dist)][:-(n + 1):-1]
        print("topic {}\n- {}".format(i, ('-'.join(topic_words)).encode("utf-8")))

    # 文档主题(Document-Topic)分布：
    doc_topic = model.doc_topic_
    print("type(doc_topic): {}".format(type(doc_topic)))
    print("shape: {}".format(doc_topic.shape))

    # 一篇文章对应一行，每行的和为1
    # 输入前10篇文章最可能的Topic
    for n in range(20):
        topic_most_pr = doc_topic[n].argmax()
        print("doc: {} topic: {}".format(n, topic_most_pr))

print "read begin!"
y = np.genfromtxt("data\\target_wzp.txt",skip_header=1,dtype = np.int)
print len(y)
X = np.genfromtxt("data\\source_wzp_lda_1.txt",skip_header=1,dtype = np.int)
print X.shape
print "read end!"

selectFeature1(X,y)