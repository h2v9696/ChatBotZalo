#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
# from app.clf.svm_model import SVMModel
# from app.clf.read_data import ReadData
from svm_model import SVMModel
from read_data import ReadData
from sklearn.externals import joblib
import os
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
SRCDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.join(SRCDIR, 'Data')
# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)
# warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


class TextClassificationPredict(object):
    def __init__(self, msg = '', _isTest = False):
        self.test = msg
        self.isTest = _isTest
        self.confirm = 1

    def test_clf(self):
        while True:
            self.test = input("Nhập câu cần test: ")
            self.get_train_data()
            # if (self.confirm == '0'):
                # break

    def process_model_domain(self):
        read = ReadData()
        print('===Process domain model')
        # Tạo train data domain
        if (not(os.path.exists(SRCDIR + '/clf.domain'))):
            data_dir = DATADIR + '/domain/'
            list_file = os.listdir(data_dir)
            train_data = []
            print('===Reading data...')
            for file in list_file:
                print(file)
                data_train = read.read_file(data_dir + file)
                for data in data_train:
                    feature = {"feature": data[1], "target": data[0]}
                    train_data.append(feature)
            print('===Reading data is completed! \n===Training data...')

            df_train = pd.DataFrame(train_data)
            # init model svm
            domain_model = SVMModel()
            clf = domain_model.clf.fit(df_train["feature"], df_train.target)
            print('===Training data is completed! \n===Dumping model...')
            joblib.dump(clf, SRCDIR + '/clf.domain')
            print('===Dumping model is completed! ')
        else:
            # Lưu model
            clf = joblib.load(SRCDIR + '/clf.domain')
        return clf

    def process_model_question(self):
        print('===Process question type model')

        read = ReadData()
        # Tạo train data domain
        if (not(os.path.exists(SRCDIR + '/clf.question_type'))):
            data_dir = DATADIR + '/question_type/'
            list_file = os.listdir(data_dir)
            train_data = []
            print('===Reading data...')
            for file in list_file:
                print(file)
                data_train = read.read_file(data_dir + file)
                for data in data_train:
                    feature = {"feature": data[1], "target": data[0]}
                    train_data.append(feature)
            print('===Reading data is completed! \n===Training data...')

            df_train = pd.DataFrame(train_data)
            # init model svm
            domain_model = SVMModel()
            clf = domain_model.clf.fit(df_train["feature"], df_train.target)
            print('===Training data is completed! \n===Dumping model...')
            joblib.dump(clf, SRCDIR + '/clf.question_type')
            print('===Dumping model is completed! ')
        else:
            # Lưu model
            clf = joblib.load(SRCDIR + '/clf.question_type')
        return clf
    def process_model_attri(self):
        print('===Process attribute model')

        read = ReadData()
        # Tạo train data domain
        if (not(os.path.exists(SRCDIR + '/clf.attribute'))):
            data_dir = DATADIR + '/question_attribute/'
            list_file = os.listdir(data_dir)
            train_data = []
            print('===Reading data...')
            for file in list_file:
                print(file)
                data_train = read.read_file(data_dir + file)
                for data in data_train:
                    feature = {"feature": data[1], "target": data[0]}
                    train_data.append(feature)
            print('===Reading data is completed! \n===Training data...')

            df_train = pd.DataFrame(train_data)
            # init model svm
            domain_model = SVMModel()
            clf = domain_model.clf.fit(df_train["feature"], df_train.target)
            print('===Training data is completed! \n===Dumping model...')
            joblib.dump(clf, SRCDIR + '/clf.attribute')
            print('===Dumping model is completed! ')
        else:
            # Lưu model
            clf = joblib.load(SRCDIR + '/clf.attribute')
        return clf

    def get_train_data(self):
        # [0] = question type; [1] = domain; [2] = attribute
        intent_result = []
        read = ReadData()
        # Tạo test data
        # data_test = read.read_file('product_test.txt')
        test_data = []
        index_label = 0
        index_data = 1
        data_dir = ''

        test_data.append({"feature": self.test, "target": ''})
        df_test = pd.DataFrame(test_data)

        clf_domain = self.process_model_domain()
        clf_qtype = self.process_model_question()
        clf_attri = self.process_model_attri()

        # score = clf.score(df_test["feature"], df_test["target"])

        prediction_domain = clf_domain.predict(df_test["feature"])
        # print 'Domain: Độ chính xác {}'.format(accuracy_score(['product'], prediction))
        # Print predicted result
        # print df_train.target.unique()
        prediction_qtype = clf_qtype.predict(df_test["feature"])
        # print prediction_qt
        # print 'Question Type: Độ chính xác {}'.format(accuracy_score(['exists'], prediction))
        # print score
        # print clf_domain.predict_proba(df_test["feature"])
        # print clf_qtype.predict_proba(df_test["feature"])
        prediction_attri = clf_attri.predict(df_test["feature"])

        # print classification_report(df_test.target, clf.predict(df_test["feature"]))
        if (self.isTest):
            print(prediction_qtype)
            print(prediction_domain)
            print(prediction_attri)
            # self.confirm = input('Test tiếp (Không = 0/Có = 1)? ')
        else:
            intent_result.append(prediction_qtype[0]);
            intent_result.append(prediction_domain[0]);
            intent_result.append(prediction_attri[0]);
            return intent_result

if __name__ == '__main__':
    tcp = TextClassificationPredict("", True)
    tcp.test_clf()
    # tcp.get_train_data()
