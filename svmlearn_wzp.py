#!/usr/bin/python
# coding:utf-8

# 本程序采用svm来训练句中的时间特征

from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import GridSearchCV
import numpy

X = []
y = []

global file_txt

def Xarray():
    file = open("data\\source_wzp.txt", "r")
    file.readline()
    i = 0
    while True:
        line = file.readline().replace("\n", "")
        if not line:
            break
        i = i + 1
        current_vector = line.split("\t")
        xtemp = []
        for item in current_vector:
            if item == '':
                break
            xtemp.append(float(item))
        X.append(xtemp)
    print i
    file.close()
    return


def yarray():
    file = open("data\\target_wzp.txt", "r")
    file.readline()
    while True:
        line = file.readline().replace("\n", "")
        if not line:
            break
        y.append(float(line))
    file.close()
    return

def train_model(n,m):
    #m:训练集大小
    #n：从哪开始为训练集
    global file_txt

    train = X[0:n] + X[n+m:]
    target = y[0:n] + y[n+m:]
    test = X[n:n+m]
    act = y[n:n+m]

    file_txt.write("test:"+"%d"%n+" "+"%d"%(n+m)+"\n")

    #主要调节的参数有：C、kernel、degree、gamma、coef0。
    clf = svm.SVC(C=0.6, kernel='linear', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False,
                  tol=0.01, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape=None,
                  random_state=None)
    clf.fit(train, target)
    result = clf.predict(test)

    print result
    print act

    print len(train)
    print len(target)
    print len(test)
    print len(act)

    '''c = numpy.arange(0.01, 10, 0.01)
    param_grid = {'C': c}
    svr = svm.SVC()
    grid = GridSearchCV(svr, param_grid, cv = 5, scoring='accuracy')
    grid.fit(X, y)
    print grid.best_params_'''

    cr = metrics.classification_report(act, result)
    print cr
    # calculate_result(y,result)
    confusion_matrix = metrics.confusion_matrix(act, result)
    print confusion_matrix
    overall_accuracy = metrics.accuracy_score(act, result)
    print overall_accuracy
    file_txt.write("overall_accuracy:" + "%f" % overall_accuracy + "\n")
    pscore = metrics.accuracy_score(act, result)
    rscore = metrics.recall_score(act, result, average='weighted')
    fscore = metrics.f1_score(act, result, average='weighted')
    print 'p:', pscore
    file_txt.write("pscore:" + "%f" % pscore + "\n")
    print 'r:', rscore
    file_txt.write("rscore:" + "%f" % rscore + "\n")
    print 'f:', fscore
    file_txt.write("fscore:" + "%f" % fscore + "\n")

def train_model1():
    #m:训练集大小
    #n：从哪开始为训练集
    global file_txt

    train = X[499:]
    target = y[499:]
    test = X[0:499]
    act = y[0:499]

    clf = svm.SVC(C=0.6, kernel='linear', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False,
                  tol=0.01, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape=None,
                  random_state=None)
    clf.fit(train, target)
    result = clf.predict(test)

    print result
    print act

    print len(train)
    print len(target)
    print len(test)
    print len(act)

    '''c = numpy.arange(0.01, 10, 0.01)
    param_grid = {'C': c}
    svr = svm.SVC()
    grid = GridSearchCV(svr, param_grid, cv = 5, scoring='accuracy')
    grid.fit(X, y)
    print grid.best_params_'''

    cr = metrics.classification_report(act, result)
    print cr
    # calculate_result(y,result)
    confusion_matrix = metrics.confusion_matrix(act, result)
    print confusion_matrix
    overall_accuracy = metrics.accuracy_score(act, result)
    print overall_accuracy
    file_txt.write("overall_accuracy:" + "%f" % overall_accuracy + "\n")
    pscore = metrics.accuracy_score(act, result)
    rscore = metrics.recall_score(act, result, average='weighted')
    fscore = metrics.f1_score(act, result, average='weighted')
    print 'p:', pscore
    file_txt.write("pscore:" + "%f" % pscore + "\n")
    print 'r:', rscore
    file_txt.write("rscore:" + "%f" % rscore + "\n")
    print 'f:', fscore
    file_txt.write("fscore:" + "%f" % fscore + "\n")

    result1 = [0,0,0,0,0,0,0,0,0,0,0,0]
    error = [0,0,0,0,0,0,0,0,0,0,0,0]

    for i in range(499):
        #"i:"+result[i] + " " + act[i]
        file_txt.write("%d:"%i + "%f"%result[i] + " " + "%f"%act[i])

        result1[(int)(act[i])] = result1[(int)(act[i])] + 1
        '''
        if(act[i] == 1):
            result1[1] = result1[1] + 1
        if(act[i] == 2):
            result1[2] = result1[2] + 1
        if(act[i] == 3):
            result1[3] = result1[3] + 1
        if(act[i] == 4):
            result1[4] = result1[4] + 1
        if(act[i] == 5):
            result1[5] = result1[5] + 1
        if(act[i] == 6):
            result1[6] = result1[6] + 1
        if(act[i] == 7):
            result1[7] = result1[7] + 1
        if(act[i] == 8):
            result8 = result8 + 1
        if(act[i] == 9):
            result9 = result9 + 1
        if(act[i] == 10):
            result10 = result10 + 1
        if (act[i] == 11):
            result11 = result11 + 1
        '''

        if(result[i]!=act[i]):
            file_txt.write("    " + "error")
            error[int(act[i])] = error[int(act[i])] + 1
            '''
            if (act[i] == 1):
                error1 = error1 + 1
            if (act[i] == 2):
                error2 = error2 + 1
            if (act[i] == 3):
                error3 = error3 + 1
            if (act[i] == 4):
                error4 = error4 + 1
            if (act[i] == 5):
                error5 = error5 + 1
            if (act[i] == 6):
                error6 = error6 + 1
            if (act[i] == 7):
                error7 = error7 + 1
            if (act[i] == 8):
                error8 = error8 + 1
            if (act[i] == 9):
                error9 = error9 + 1
            if (act[i] == 10):
                error10 = error10 + 1
            if (act[i] == 11):
                error11 = error11 + 1
            '''
        file_txt.write("\n")
    precision = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(12):
        if(i == 0):
            continue
        if(result1[i] != 0):
            precision[i] = (float)(result1[i] - error[i]) / result1[i]
            print precision[i]
        file_txt.write("%d"%i+":"+"%d"%(result1[i]-error[i])+" "+"%d"%result1[i]+" "+"%f"%precision[i]+"\n")

def train_model2(n,m):
    #m:训练集大小
    #n：从哪开始为训练集
    global file_txt

    train = X[0:n] + X[n+m:]
    target = y[0:n] + y[n+m:]
    test = X[n:n+m]
    act = y[n:n+m]

    clf = svm.SVC(C=0.6, kernel='linear', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False,
                  tol=0.01, cache_size=200, class_weight=None, verbose=False, max_iter=-1, decision_function_shape=None,
                  random_state=None)
    clf.fit(train, target)
    result = clf.predict(test)

    print result
    print act

    print len(train)
    print len(target)
    print len(test)
    print len(act)

    cr = metrics.classification_report(act, result)
    print cr
    # calculate_result(y,result)
    confusion_matrix = metrics.confusion_matrix(act, result)
    print confusion_matrix
    overall_accuracy = metrics.accuracy_score(act, result)
    print overall_accuracy
    file_txt.write("overall_accuracy:" + "%f" % overall_accuracy + "\n")
    pscore = metrics.accuracy_score(act, result)
    rscore = metrics.recall_score(act, result, average='weighted')
    fscore = metrics.f1_score(act, result, average='weighted')
    print 'p:', pscore
    file_txt.write("pscore:" + "%f" % pscore + "\n")
    print 'r:', rscore
    file_txt.write("rscore:" + "%f" % rscore + "\n")
    print 'f:', fscore
    file_txt.write("fscore:" + "%f" % fscore + "\n")

    result1 = [0,0,0,0,0,0,0,0,0,0,0,0]
    error = [0,0,0,0,0,0,0,0,0,0,0,0]

    for i in range(499):
        #"i:"+result[i] + " " + act[i]
        file_txt.write("%d:"%i + "%f"%result[i] + " " + "%f"%act[i])

        result1[(int)(act[i])] = result1[(int)(act[i])] + 1

        if(result[i]!=act[i]):
            file_txt.write("    " + "error")
            error[int(act[i])] = error[int(act[i])] + 1

        file_txt.write("\n")
    precision = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(12):
        if(i == 0):
            continue
        if(result1[i] != 0):
            precision[i] = (float)(result1[i] - error[i]) / result1[i]
            print precision[i]
        file_txt.write("%d"%i+":"+"%d"%(result1[i]-error[i])+" "+"%d"%result1[i]+" "+"%f"%precision[i]+"\n")

def main():
    Xarray()
    yarray()

    global file_txt
    file_txt = open("data\\result0_499.txt", "w")
    '''
    for i in range(9):
        i = i *300
        train_model(i,399)
    '''

    train_model1()
    file_txt.close()

    '''
    for i in range(1,7):
        file_txt = open("data\\result"+"%d"%(i*400)+"_"+"%d"%(i*400+499)+".txt", "w")
        i = i * 400
        train_model2(i,499)
        file_txt.close()
    '''
    return


main()