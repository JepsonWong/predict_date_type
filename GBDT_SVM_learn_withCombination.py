#!/usr/bin/python
#coding:utf-8

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn import svm

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

print "read data start!"
#在使用这个方法的时候要注意，他会把整个文件都读进去，而vector.py会有一行标签，建议手动删除
X1 = np.genfromtxt("data\\source_wzp.txt",skip_header=1,dtype = np.float32)
X2 = np.genfromtxt("data\\source_wzp_3.txt",skip_header=1,dtype = np.float32)
y = np.genfromtxt("data\\target_wzp.txt",skip_header=1,dtype = np.float32)

X = np.hstack((X1,X2))

print X.shape
print y.shape
print "read success!"

print "fit start!"
gbdt.fit(X, y)
print "fit success!"

score = gbdt.feature_importances_
print gbdt.feature_importances_
print gbdt.feature_importances_.shape
print gbdt.feature_importances_>0

#选择importance>0的特征
X_new = X[:, gbdt.feature_importances_>0]
print X_new.shape

#主要调节的参数有：C、kernel、degree、gamma、coef0
clf = svm.SVC(C=0.6, kernel='linear', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False,
                  tol=0.01, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape=None,
                  random_state=None)

scores = cross_val_score(clf, X_new, y, cv=3)
print scores.mean()
print scores
