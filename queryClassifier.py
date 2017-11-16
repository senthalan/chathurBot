import pandas as pd
from sklearn.cross_validation import train_test_split  # For K-fold cross validation
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier

# Generic function for making a classification model and accessing performance:
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from configReader import read_config
from seq2seq import seq2seq_predict

predictor_var = ['model', 'brand', 'onlineStore', 'memory', 'price', 'comparator', 'order_by', 'order',
                 'limit']
model_logistic_regression = LogisticRegression()
model_decision_tree_classifier = DecisionTreeClassifier()
model_gaussian_nb = GaussianNB()
model_svc = SVC()
model_mlp_classifier = MLPClassifier(solver='lbfgs', hidden_layer_sizes=[100], max_iter=2000, activation='logistic')

query_template = {
    10: u"{entity_key} = {entity_value}",
    11: u"{entity_key} <= {entity_value}",
    12: u"{entity_bet_key} BETWEEN {entity_bet_one} AND {entity_bet_two}",
    13: u"{entity_key} >= {entity_value}",
    18: u"{entity_key} = {entity_value}  ORDER BY {order_by} DESC LIMIT 1",
    19: u"{entity_key} = {entity_value}  ORDER BY {order_by} ASC LIMIT 1",

    20: u"{entity_key} = {entity_value} AND {entity_key_two} = {entity_value_two}",
    21: u"{entity_key} <= {entity_value}  AND {entity_key_two} = {entity_value_two}",
    22: u" {entity_key_two} = {entity_value_two} AND {entity_bet_key} BETWEEN {entity_bet_one} AND {entity_bet_two}",
    23: u"{entity_key} >= {entity_value}  AND {entity_key_two} = {entity_value_two}",
    28: u"{entity_key} = {entity_value}  AND {entity_key_two} = {entity_value_two}  ORDER BY {order_by} DESC LIMIT 1",
    29: u"{entity_key} = {entity_value}  AND {entity_key_two} = {entity_value_two} ORDER BY {order_by} ASC LIMIT 1",

    30: u"{entity_key} = {entity_value} AND {entity_key_two} = {entity_value_two} AND {entity_key_three} = {entity_value_three}",
    31: u"{entity_key} <= {entity_value}  AND {entity_key_two} = {entity_value_two}  AND {entity_key_three} = {entity_value_three}",
    32: u" {entity_key_two} = {entity_value_two} AND {entity_key_three} = {entity_value_three} AND {entity_bet_key} BETWEEN {entity_bet_one} AND {entity_bet_two}",
    33: u"{entity_key} >= {entity_value}  AND {entity_key_two} = {entity_value_two}  AND {entity_key_three} = {entity_value_three}",
    38: u"{entity_key} = {entity_value}  AND {entity_key_two} = {entity_value_two}  AND {entity_key_three} = {entity_value_three} ORDER BY {order_by} DESC LIMIT 1",
    39: u"{entity_key} = {entity_value}  AND {entity_key_two} = {entity_value_two}  AND {entity_key_three} = {entity_value_three} ORDER BY {order_by} ASC LIMIT 1",
}
table_name = read_config("tableName")


def classification_model(model, data, predictors, outcome):
    train, test, train_labels, test_labels = train_test_split(data[predictors],
                                                              data[outcome],
                                                              test_size=0.33,
                                                              random_state=42)
    # Fit the model:
    model.fit(train, train_labels)

    # Make predictions
    preds = model.predict(test)
    # print "accuracy", accuracy_score(test_labels, preds)
    score = precision_recall_fscore_support(test_labels, preds, average='macro')
    # print "precision", score[0]
    # print "recall", score[1]
    # print "fscore", score[2]
    # print


def train():
    df = pd.read_csv("data/classification.csv")  # Reading the dataset in a dataframe using Pandas
    outcome_var = 'where'

    # print 'LogisticRegression : '
    classification_model(model_logistic_regression, df, predictor_var, outcome_var)
    # print 'DecisionTreeClassifier : '
    classification_model(model_decision_tree_classifier, df, predictor_var, outcome_var)
    # print 'GaussianNB : '
    classification_model(model_gaussian_nb, df, predictor_var, outcome_var)
    # print 'SVC : '
    classification_model(model_svc, df, predictor_var, outcome_var)
    # print 'MLPClassifier : '
    classification_model(model_mlp_classifier, df, predictor_var, outcome_var)


def predit_query(intent, entities_list, extremum, comparator, order_by, order, limit):
    X = []
    keys = entities_list.keys()
    between_value = {}
    between_key = {}
    print entities_list
    for entity in predictor_var:
        if entity == 'comparator':
            break
        if entity in entities_list:
            if len(entities_list.get(entity)) == 0:
                X.append(0)
                continue
            X.append(1)
            if len(entities_list.get(entity)) > 1:
                between_key = entity
                between_value = entities_list.get(entity)
                del entities_list[entity]
        else:
            X.append(0)
    # comparator
    if comparator == '<=':
        X.append(1)
    elif comparator == 'between':
        X.append(2)
    elif comparator == '>=':
        X.append(3)
    else:
        X.append(0)
    # order by
    if order_by == '':
        X.append(0)
    else:
        X.append(1)
    # order
    if order == 'DESC':
        X.append(1)
    elif order == 'ASE':
        X.append(2)
    else:
        X.append(0)
    # limit
    if limit == '':
        X.append(0)
    else:
        X.append(1)

    prediction = model_mlp_classifier.predict([X])[0]
    if prediction in query_template.keys():
        predicted_query = query_template[prediction]
    else:
        return ''
    print "predicted query ", predicted_query

    if (order_by != ''):
        template = u"SELECT {function}({column_name}) FROM {table_name} where {where_expression}"
    else:
        template = u"SELECT DISTINCT {function}({column_name}) FROM {table_name} where {where_expression}"

    entity_key = ''
    entity_value = ''
    entity_key_two = ''
    entity_value_two = ''
    entity_key_three = ''
    entity_value_three = ''
    is_prime_set = False
    is_sec_set = False
    for key in entities_list.keys():
        value = entities_list.get(key)
        if len(value) == 0:
            continue
        if prediction == 11 or prediction == 21 or prediction == 31 or prediction == 13 or prediction == 23 or prediction == 33:
            if (key == "price") or (key == "memory"):
                entity_key = key
                entity_value = str(value[0])
                del entities_list[key]
                is_prime_set = True
    for key in entities_list.keys():
        value = entities_list.get(key)
        if len(value) == 0:
            continue
        if not is_prime_set:
            entity_key = key
            entity_value = "\"" + value[0] + "\""
            is_prime_set = True
        elif not is_sec_set:
            entity_key_two = key
            entity_value_two = "\"" + value[0] + "\""
            is_sec_set = True
        else:
            entity_key_three = key
            entity_value_three = "\"" + value[0] + "\""

    # value = entities_list.pop()[0].split()
    # predicted_query.format(entity_key_two=key, entity_value_two="\"" + value + "\"")
    # value = entities_list.pop()[0].split()
    # predicted_query.format(entity_key_three=key, entity_value_three="\"" + value + "\"")

    if prediction == 12 or prediction == 22 or prediction == 32:
        if (len(between_value ) != 2):
            return "NULL"
        where_part = predicted_query.format(entity_key=entity_key, entity_value=entity_value, entity_key_two=entity_key_two,
                           entity_value_two=entity_value_two, entity_key_three=entity_key_three,
                           entity_value_three=entity_value_three,
                           entity_bet_key=between_key, entity_bet_one=str(between_value[0]),
                           entity_bet_two=str(between_value[1]))
    elif prediction == 18 or prediction == 19 or prediction == 29 or prediction == 38 or prediction == 39:
        where_part = predicted_query.format(entity_key=entity_key, entity_value=entity_value, entity_key_two=entity_key_two,
                           entity_value_two=entity_value_two, entity_key_three=entity_key_three,
                           entity_value_three=entity_value_three,
                           order_by=order_by, order=order)
    else:
        where_part = predicted_query.format(entity_key=entity_key, entity_value=entity_value, entity_key_two=entity_key_two,
                           entity_value_two=entity_value_two, entity_key_three=entity_key_three,
                           entity_value_three=entity_value_three)
    select = intent.lower()

    final_query = template.format(function=extremum, column_name=select, table_name=table_name,
                                    where_expression=where_part)
    return final_query