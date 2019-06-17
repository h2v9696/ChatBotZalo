#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from app.clf.classifier_model import ClassifierModel
from app.clf.read_data import ReadData
# from classifier_model import ClassifierModel
# from read_data import ReadData
from sklearn.externals import joblib
import os
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

SRCDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.join(SRCDIR, 'Data')
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


class TextClassificationPredict(object):
    def __init__(self, msg = '', _isTest = 0):
        self.test = msg
        self.isTest = _isTest # 0 = no test, 1 = test with 1 sentence, 2 = test with test data
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
            domain_model = ClassifierModel()
            clf = domain_model.clf.fit(df_train["feature"], df_train.target)
            print(classification_report(df_train.target, clf.predict(df_train["feature"])))
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
            domain_model = ClassifierModel()
            clf = domain_model.clf.fit(df_train["feature"], df_train.target)
            print(classification_report(df_train.target, clf.predict(df_train["feature"])))
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
            domain_model = ClassifierModel()
            clf = domain_model.clf.fit(df_train["feature"], df_train.target)
            print(classification_report(df_train.target, clf.predict(df_train["feature"])))
            print('===Training data is completed! \n===Dumping model...')
            joblib.dump(clf, SRCDIR + '/clf.attribute')
            print('===Dumping model is completed! ')
        else:
            # Lưu model
            clf = joblib.load(SRCDIR + '/clf.attribute')
        return clf

    def process_model_new(self, model_name):
        print('===Process model', model_name)
        data_test = []
        read = ReadData()
        # Tạo train data domain
        if (not(os.path.exists(SRCDIR + '/clf.' + model_name))):
            all_data = []
            print('===Reading data...')
            data_read = read.read_file(DATADIR + '/' + model_name + '.txt')
            print('/' + model_name + '.txt')
            for data in data_read:
                    feature = {"feature": data[1], "target": data[0]}
                    all_data.append(feature)
            print('===Reading data is completed!')

            df_data = pd.DataFrame(all_data)
            print('===Spliting data...')
            data_train, data_test = train_test_split(df_data, test_size=0.33, random_state=42)
            print('===Splited data shape')
            print(data_train.shape, data_test.shape)
            # init model svm
            domain_model = ClassifierModel()
            print('===Training data...')
            clf = domain_model.clf.fit(data_train["feature"], data_train.target)
            # print('===Train data score')
            # print(classification_report(data_train.target, clf.predict(data_train["feature"])))
            print('===Training data is completed! \n===Dumping model...')
            joblib.dump(clf, SRCDIR + '/clf.' + model_name)
            print('===Dumping model is completed! \n===Testing model...')
            print(classification_report(data_test.target, clf.predict(data_test["feature"])))
            print("Accuracy: ", clf.score(data_test["feature"], data_test["target"]))
            print('===Testing model ' + model_name + ' is completed! ')
            print('=================================================\n')
        else:
            # Lưu model
            clf = joblib.load(SRCDIR + '/clf.' + model_name)

        return clf

    def process_test(self, domain_clf, question_type_clf, attr_clf):
        read = ReadData()
        domain_test_data = []
        question_type_test_data = []
        attr_test_data = []
        print('===Process test')
        # Tạo test data
        data_dir = DATADIR + '/test-data/'
        list_file = os.listdir(data_dir)

        print('===Reading data...')

        data_test = read.read_file(data_dir + 'domain_test.txt')
        print('domain_test.txt')
        for data in data_test:
            feature = {"feature": data[1], "target": data[0]}
            domain_test_data.append(feature)
        data_test = read.read_file(data_dir + 'question_attr_test.txt')
        print('question_attr_test.txt')
        for data in data_test:
            feature = {"feature": data[1], "target": data[0]}
            attr_test_data.append(feature)
        data_test = read.read_file(data_dir + 'question_type_test.txt')
        print('question_type_test.txt')
        for data in data_test:
            feature = {"feature": data[1], "target": data[0]}
            question_type_test_data.append(feature)
        print('===Reading data is completed!')
        df_test_domain = pd.DataFrame(domain_test_data)
        df_test_qt = pd.DataFrame(question_type_test_data)
        df_test_attr = pd.DataFrame(attr_test_data)
        print(classification_report(df_test_domain.target, domain_clf.predict(df_test_domain["feature"])))
        print("Accuracy: ", domain_clf.score(df_test_domain["feature"], df_test_domain["target"]))
        print(classification_report(df_test_qt.target, question_type_clf.predict(df_test_qt["feature"])))
        print("Accuracy: ", question_type_clf.score(df_test_qt["feature"], df_test_qt["target"]))
        print(classification_report(df_test_attr.target, attr_clf.predict(df_test_attr["feature"])))
        print("Accuracy: ", attr_clf.score(df_test_attr["feature"], df_test_attr["target"]))

    def get_train_data(self):
        # [0] = question type; [1] = domain; [2] = attribute
        intent_result = []
        read = ReadData()
        # Tạo test data
        # data_test = read.read_file('product_test.txt')
        test_data = []
        # index_label = 0
        # index_data = 1
        data_dir = ''
        # Old test
        # clf_domain = self.process_model_domain()
        # clf_qtype = self.process_model_question()
        # clf_attri = self.process_model_attri()
        # New function: Train and test
        clf_domain = self.process_model_new('domain')
        clf_qtype = self.process_model_new('q_type')
        clf_attri = self.process_model_new('q_attr')

        if (self.isTest != 2):
            test_data.append({"feature": self.test, "target": ''})
            df_test = pd.DataFrame(test_data)
            # score = clf.score(df_test["feature"], df_test["target"])
            prediction_domain = clf_domain.predict(df_test["feature"])
            # print 'Domain: Độ chính xác {}'.format(accuracy_score(['product'], prediction))
            # Print predicted result
            # print df_train.target.unique()
            prediction_qtype = clf_qtype.predict(df_test["feature"])
            # print prediction_qt
            # print 'Question Type: Độ chính xác {}'.format(accuracy_score(['exists'], prediction))
            # print score
            prediction_attri = clf_attri.predict(df_test["feature"])

            # print classification_report(df_test.target, clf.predict(df_test["feature"]))
            if (self.isTest == 1):
                print("Domain: " + prediction_domain)
                print(round(np.amax(clf_domain.predict_proba(df_test["feature"]))*100, 2))
                # print(round(np.amax(clf_domain.staged_predict_proba(df_test["feature"]))*100, 2))
                print("Question type: " + prediction_qtype)
                print(round(np.amax(clf_qtype.predict_proba(df_test["feature"]))*100, 2))
                print("Attribute: " + prediction_attri)
                print(round(np.amax(clf_attri.predict_proba(df_test["feature"]))*100, 2))
                # self.confirm = input('Test tiếp (Không = 0/Có = 1)? ')
            else:
                intent_result.append(prediction_qtype[0]);
                intent_result.append(prediction_domain[0]);
                intent_result.append(prediction_attri[0]);
                return intent_result
        else:
            self.process_test(clf_domain, clf_qtype, clf_attri)



if __name__ == '__main__':
    tcp = TextClassificationPredict("", 2)
    # tcp.test_clf()
    tcp.get_train_data()
