from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn import preprocessing
from sklearn.pipeline import Pipeline


import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
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
stats = []
stats1 = []
stats2 = []
stats3 = []

#Read Data
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


#knn
clf=KNeighborsClassifier(n_neighbors=7,n_jobs=-1) #best exper for KNN
pipeline = Pipeline([
    ('vect', vectorizer),
    ('tfidf', transformer),
    ('svd',svd),
    ('clf', clf)
])

stats1 = compute_and_print()



#randomforest
clf=RandomForestClassifier(n_estimators=50,n_jobs=-1)
pipeline = Pipeline([
    ('vect', vectorizer),
    ('tfidf', transformer),
    ('svd',svd),
    ('clf', clf)
])

stats2 = compute_and_print()



#logistic regression
clf=LogisticRegression()
pipeline = Pipeline([
    ('vect', vectorizer),
    ('tfidf', transformer),
    ('svd',svd),
    ('clf', clf)
])


stats3 = compute_and_print()

csv_out = open('EvaluationsMetricAccuracy', 'wb')
clwriter = csv.writer(csv_out)

for i in range(1,11):
	stats.append('Fold'+str(i) )

fieldnames = ['Accuracy','KNN','RandomForests','LogisticRegression']
rows = zip(stats, stats1, stats2,stats3)
clwriter.writerow(fieldnames)
clwriter.writerows(rows)
csv_out.close()
