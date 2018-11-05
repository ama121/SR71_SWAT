
# coding: utf-8

# In[44]:


import pandas as pd
import numpy as np
import re
import os.path
import sys
from os import path
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import imp


# In[45]:


GaussianNBModel = GaussianNB()
KneighboursModel_5 = make_pipeline(
    KNeighborsClassifier(n_neighbors=5)
)
KneighboursModel_15 = make_pipeline(
    KNeighborsClassifier(n_neighbors=25)
)
KneighboursModelWithScaler_5 = make_pipeline(
    StandardScaler(),
    KNeighborsClassifier(n_neighbors=5)
)
KneighboursModelWithScaler_15 = make_pipeline(
    StandardScaler(),
    KNeighborsClassifier(n_neighbors=15)
)
SVCModelRBF = SVC(kernel='rbf', C=5, gamma=5)

SVCModelLinear = SVC(kernel='linear', C=1e-2)

SVCModelWithScalerRBF = make_pipeline(
    StandardScaler(),
    PCA(2100),
    SVC(kernel='rbf', C=5, gamma=5)
)
SVCModelWithScalerLinear = make_pipeline(
    StandardScaler(),
    PCA(2100),
    SVC(kernel='linear', C=1e-2)
)
NeuralModel = MLPClassifier(solver='lbfgs',
                            hidden_layer_sizes=(5, 4),
                            activation='identity',
                            random_state=0
                            )
NeuralModel = MLPClassifier(alpha = 0.7, max_iter=400) 


# In[46]:


def PrintResults(Xtrain, ytrain, xtest, ytest):
    models = [GaussianNBModel,
              KneighboursModel_5,
              KneighboursModel_15,
              KneighboursModelWithScaler_5,
              KneighboursModelWithScaler_15,
              SVCModelRBF,
              SVCModelLinear,
              SVCModelWithScalerRBF,
              SVCModelWithScalerLinear,
              NeuralModel
              ]
    # fit each model
    for i, m in enumerate(models):
        m.fit(Xtrain, ytrain)
    modelName = [' GaussianNBModel',
                 '  KneighboursModel_5',
                 '  KneighboursModel_15',
                 '  KneighboursModelWithScaler_5',
                 '  KneighboursModelWithScaler_15',
                 '   SVCModelRBF',
                 '   SVCModelLinear',
                 '   SVCModelWithScalerRBF',
                 '   SVCModelWithScalerLinear',
                 '    NeuralModel'
                 ]
    # print the score for each model
    for i, m in enumerate(models):
        temp = m.score(xtest, ytest)
        print(modelName[i] + "'s score:" + str(temp))
        
def removeNameTag(i):
    Reg = '(@\s*\w+)'
    m = re.sub(Reg,'', i)
    if m:
        return m 
    else:
        return None


# In[61]:


TestText = sys.argv[1]
def predict(text):
    df = pd.read_csv("/Users/abhi/Downloads/all/train.csv", encoding='cp1252')

    Sentiment  = df["Sentiment"]
    SentimentText = df["SentimentText"]

    count_vect = CountVectorizer()
    SentimentText_Counts = count_vect.fit_transform(SentimentText)

    tfidf_transformer = TfidfTransformer()
    SentimentText_Counts = tfidf_transformer.fit_transform(SentimentText_Counts)

    SentimentText = df["SentimentText"].apply(removeNameTag).str.lstrip().str.rstrip()
    clf = MultinomialNB().fit(SentimentText_Counts, Sentiment)
        #X_train_SentimentText, X_test_SentimentText, y_train_Sentiment, y_test_Sentiment = train_test_split(SentimentText_Counts, Sentiment)
        #clf.score(X_test_SentimentText, y_test_Sentiment)
    #joblib.dump(clf, '/Users/Unchained_Erbo/Downloads/all/model.joblib') 
    docs_new = [text]
    dummyTest = count_vect.transform(docs_new)
    dummyTest_tfidf = tfidf_transformer.transform(dummyTest)
    predicted = clf.predict(dummyTest_tfidf)

    return predicted[0]
print(predict(TestText))


# In[18]:


#NeuralModel.fit(X_train_SentimentText, y_train_Sentiment)


# In[23]:


#NeuralModel.score(X_test_SentimentText, y_test_Sentiment)

