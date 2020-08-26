from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV


import pandas as pd
import numpy as np
feature = ['ItemID','Sentiment','SentimentText']
data=pd.read_csv('C:\\Users\\Rohan\\Desktop\\Sentiment-Analysis\\train.csv' ,sep=',',error_bad_lines=False, names=feature,encoding='latin-1')
data=data.iloc[1:]
pd.set_option('display.max_colwidth', -1)
data.head()

raw_data=data['SentimentText']

import re

def preprocess_text(text):
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','', str(text))
    text = re.sub('RT @[^\s]+','', str(text))
    text = re.sub('@[^\s]+','',str(text))
    text = text.lower().replace("ё", "е")
    text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ',str(text))
    text = re.sub(' +',' ',str(text))
    text=re.sub('#(\w+)','',str(text))
    return text.strip()

text_data = [preprocess_text(t) for t in raw_data]
data['SentimentText']=text_data

text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB())])

tuned_parameters = {
    'vect__ngram_range': [(1, 1), (1, 2), (2, 2)],
    'tfidf__use_idf': (True, False),
    'tfidf__norm': ('l1', 'l2'),
    'clf__alpha': [1, 1e-1, 1e-2]
}




x_train, x_test, y_train, y_test = train_test_split(data['SentimentText'], data['Sentiment'], test_size=0.33, random_state=42)


from sklearn.metrics import classification_report

score = 'f1_macro'
print("# Tuning hyper-parameters for %s" % score)
print()
np.errstate(divide='ignore')
clf = GridSearchCV(text_clf, tuned_parameters, cv=10, scoring=score)
clf.fit(x_train, y_train)

print("Best parameters set found on development set:")
print()
print(clf.best_params_)
print()
print("Grid scores on development set:")
print()
for mean, std, params in zip(clf.cv_results_['mean_test_score'], 
                             clf.cv_results_['std_test_score'], 
                             clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
print()

print("Detailed classification report:")
print()
print("The model is trained on the full development set.")
print("The scores are computed on the full evaluation set.")
print()
print(classification_report(y_test, clf.predict(x_test), digits=4))
print()



import pickle
filename='C:\\Users\\Rohan\\Desktop\\Sentiment-Analysis\\Nclfmodel.sav'
pickle.dump(clf,open(filename,'wb'))