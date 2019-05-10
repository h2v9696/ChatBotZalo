from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from app.clf.transformer import FeatureTransformer
# from transformer import FeatureTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from scipy.stats import randint as sp_randint
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import VotingClassifier
class ClassifierModel(object):
    def __init__(self):
        self.clf = self._init_pipeline()

    @staticmethod
    def _init_pipeline():
        # clfAda = AdaBoostClassifier(SVC(probability=True, kernel='linear'), n_estimators=5, learning_rate=1.0, algorithm='SAMME');
        clfSVC = CalibratedClassifierCV(LinearSVC());
        clfLR = LogisticRegression(solver='sag');
        clfNB = MultinomialNB(fit_prior=True, class_prior=None);
        clfSGD = SGDClassifier(loss='log', penalty='l2', alpha=1e-3, n_iter=5, random_state=None);
        # param_dist = {"max_depth": [3, None],                  #distribution
        #       "n_estimators":[50,100,200,300,400,500],
        #       "max_features": sp_randint(1, 11),
        #       "min_samples_split": sp_randint(2, 11),
        #       "min_samples_leaf": sp_randint(1, 11),
        #       "bootstrap": [True, False],
        #       "criterion": ["gini", "entropy"]}

        pipe_line = Pipeline([
            ("transformer", FeatureTransformer()),
            ("vect", CountVectorizer()),
            ("tfidf", TfidfTransformer()),
            # ('clf', RandomizedSearchCV( estimator=RandomForestClassifier(random_state=0),
            #     param_distributions=param_dist,
            #     cv=3,              #CV
            #     n_iter=1944,          #interation num
            #     scoring="accuracy", #metrics
            #     n_jobs=1,           #num of core
            #     verbose=0,
            #     random_state=1))

            ('clf', VotingClassifier(estimators=[('svc', clfSVC), ('lr', clfLR), ('onb', clfNB), ('sgd', clfSGD)], voting='soft', weights=[4,4,1,1])),
            # ('clf', AdaBoostClassifier(SVC(probability=True, kernel='linear'), n_estimators=5, learning_rate=1.0, algorithm='SAMME')),
            # ('clfSVC', CalibratedClassifierCV(OneVsRestClassifier(LinearSVC(), n_jobs=1))),
            # ('clfLR', OneVsRestClassifier(LogisticRegression(solver='sag'), n_jobs=1)),
            # ('clfONB', OneVsRestClassifier(MultinomialNB(fit_prior=True, class_prior=None)))
            # ("clfNB", MultinomialNB())#model naive bayes
            # ("clfSGD", SGDClassifier(loss='log', penalty='l2', alpha=1e-3, n_iter=5, random_state=None))
        ])

        return pipe_line
