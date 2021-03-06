#!/usr/bin/python

import sys
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn import svm, grid_search
from sklearn import cross_validation

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi',
                'salary',
                'bonus', 
                'long_term_incentive', 
                'deferred_income', 
                'deferral_payments',
                'loan_advances', 
                'other',
                'expenses', 
                'director_fees',
                'total_payments',
                'exercised_stock_options',
                'restricted_stock',
                'restricted_stock_deferred',
                'total_stock_value',
                'to_messages',
                'from_messages',
                'from_this_person_to_poi',
                'from_poi_to_this_person'] 
# You will need to use more features
### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
#Transpond dataframe
data_dict = pd.DataFrame.from_dict(data_dict)
#reorder features
data_dict = data_dict.T
data_dict = data_dict[features_list]
list(data_dict.index.values)
data_dict = data_dict.replace('NaN', np.nan)
data_dict = data_dict.drop(['TOTAL', 'THE TRAVEL AGENCY IN THE PARK','LOCKHART EUGENE E'])
#remove useless (email address)
del data_dict['email_address']
del data_dict['director_fees']
del data_dict['restricted_stock_deferred']

### Task 3: Create new feature(s)
data_dict['proportion_to_poi'] = data_dict['from_this_person_to_poi']/data_dict['from_messages']
data_dict['proportion_from_poi'] = data_dict['from_poi_to_this_person']/data_dict['to_messages']
data_dict = data_dict.replace('inf', 0)
my_dataset = data_dict.T
my_dataset.fillna(value=0, inplace = True)
features_list = features_list + ['proportion_to_poi', 'proportion_from_poi']
features_list = [e for e in features_list if e not in ('email_address', 'director_fees', 'restricted_stock_deferred')]

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

k=8
selector = SelectKBest(f_classif, k)
selector.fit_transform(features, labels)
print("SelectKBest feature scores:")
scores = zip(features_list[1:],selector.scores_)
sorted_scores = sorted(scores, key = lambda x: x[1], reverse=True)
print sorted_scores
features_list = ["poi"] + list(map(lambda x: x[0], sorted_scores))[0:k]
print("Best SelectKBest features:")
print features_list

data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
#from sklearn.naive_bayes import GaussianNB
#clf = GaussianNB()

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
#from sklearn.cross_validation import train_test_split
#features_train, features_test, labels_train, labels_test = \
#    train_test_split(features, labels, test_size=0.3, random_state=42)

clf = svm.SVC(kernel='linear', C=0.001, gamma=0.001)
features_train, features_test, labels_train, labels_test = \
train_test_split(features, labels, test_size=0.3, random_state=42)
clf.fit(features_train, labels_train)
pred = clf.predict(features_test)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)