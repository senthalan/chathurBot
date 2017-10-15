import pandas as pd
from sklearn.cross_validation import train_test_split  # For K-fold cross validation
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

# Generic function for making a classification model and accessing performance:
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def classification_model(model, data, predictors, outcome):
    train, test, train_labels, test_labels = train_test_split(data[predictors],
                                                              data[outcome],
                                                              test_size=0.33,
                                                              random_state=42)
    # Fit the model:
    model.fit(train, train_labels)

    # Make predictions
    preds = model.predict(test)
    print "accuracy", accuracy_score(test_labels, preds)
    score = precision_recall_fscore_support(test_labels, preds, average='macro')
    print "precision", score[0]
    print "recall", score[1]
    print "fscore", score[2]
    print


df = pd.read_csv("data/classification.csv")  # Reading the dataset in a dataframe using Pandas
# print df
# outcome_var = 'where_text'
outcome_var = 'where'
predictor_var = ['model', 'brand', 'online_store', 'memory', 'price', 'comparator', 'order_by', 'order',
                 'limit']

modelLogisticRegression = LogisticRegression()
modelDecisionTreeClassifier = DecisionTreeClassifier()
modelGaussianNB = GaussianNB()
modelSVC = SVC()
modelMLPClassifier = MLPClassifier(solver='lbfgs', hidden_layer_sizes=[100], max_iter=2000, activation='logistic')


print 'LogisticRegression : '
classification_model(modelLogisticRegression, df, predictor_var, outcome_var)
print 'DecisionTreeClassifier : '
classification_model(modelDecisionTreeClassifier, df, predictor_var, outcome_var)
print 'GaussianNB : '
classification_model(modelGaussianNB, df, predictor_var, outcome_var)
print 'SVC : '
classification_model(modelSVC, df, predictor_var, outcome_var)
print 'MLPClassifier : '
classification_model(modelMLPClassifier, df, predictor_var, outcome_var)
