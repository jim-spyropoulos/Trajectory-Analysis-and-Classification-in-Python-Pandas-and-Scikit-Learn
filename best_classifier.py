from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn import metrics

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import csv
#k-fold cross validation
from sklearn.cross_validation import KFold
#accuracy
from sklearn.metrics import accuracy_score


# my method
from sklearn.ensemble import VotingClassifier


def compute_and_print(): #prints all results
	stats = []
	for i, (train_index, test_index) in enumerate(kf):
		#10-fold cross validation (9 samples for training, 1 for testing)
		X_train1, X_test = X_train[train_index], X_train[test_index]
		Y_train1, Y_test = Y_train[train_index], Y_train[test_index]
		probas_ = pipeline.fit(X_train1,Y_train1).predict(X_test)
		stats.append(accuracy_score(Y_test, probas_))
	return stats


'''			preprocessing:
apart from CountVectorizer and TfidfTransformer TruncatedSVD of 300 elements and random state 42'''

df=pd.read_csv("grids.csv")
#print df

le = preprocessing.LabelEncoder()
le.fit(df["TripId"])
Y_train=le.transform(df["TripId"])
X_train1=df['Grids']



X_train=np.array(X_train1)

vectorizer=CountVectorizer()
transformer=TfidfTransformer()
svd=TruncatedSVD(n_components=300, random_state=42)
kf = KFold(len(X_train), n_folds=10)

#Our best method
#			voting classifier of 3 classifiers
'''1 best version of KNN
2 simple RandomForestClassifier
3 Best RandomForestClassifier'''

#My method---Voting Classifier
clf1 = RandomForestClassifier(n_estimators=40,n_jobs=-1)
clf2 = RandomForestClassifier(n_estimators=50,n_jobs=-1)
clf3 = KNeighborsClassifier(n_neighbors=7,n_jobs=-1)
clf = VotingClassifier(estimators=[('rf1',clf1),('rf2',clf2),('knn',clf3)], voting='hard')
pipeline = Pipeline([
    ('vect', vectorizer),
    ('tfidf', transformer),
    ('svd',svd),
    ('clf', clf)
])

print compute_and_print()
