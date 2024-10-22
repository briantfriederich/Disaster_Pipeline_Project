import sys
from sqlalchemy import create_engine
import sqlite3
import nltk
nltk.download(['punkt', 'wordnet', 'averaged_perceptron_tagger'])

import re
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
import sqlite3
import pickle


def load_data(database_filepath):
    engine = create_engine('sqlite:///data/DisasterResponse.db')
    df = pd.read_sql_table(database_filepath, engine)
    category_names = ['related', 'request', 'offer', 'aid_related', 'medical_help',
           'medical_products', 'search_and_rescue', 'security', 'military',
           'child_alone', 'water', 'food', 'shelter', 'clothing', 'money',
           'missing_people', 'refugees', 'death', 'other_aid',
           'infrastructure_related', 'transport', 'buildings', 'electricity',
           'tools', 'hospitals', 'shops', 'aid_centers',
           'other_infrastructure', 'weather_related', 'floods', 'storm',
           'fire', 'earthquake', 'cold', 'other_weather', 'direct_report']
    X = df['message']
    Y = df[category_names]
    
    return X, Y, category_names


def tokenize(text):
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model():
    model = Pipeline([
    ('vect', CountVectorizer(tokenizer=tokenize)),
    ('tfidf', TfidfTransformer()),
    ('clf', MultiOutputClassifier(RandomForestClassifier(), n_jobs=-1))
    ])    
    
    parameters = {
        'vect__stop_words': (None, 'english'),
        'vect__max_df': (0.5, 0.75, 1.0),
        'vect__min_df': (1, 5, 10),
        'vect__ngram_range': ((1, 2), (1,3)),
        'tfidf__use_idf': (True, False),
        'clf__estimator__max_depth': (10, None)
    }

    cv = GridSearchCV(model, param_grid=parameters, verbose=5)

    return cv

def display_results(model, Y_test, Y_pred):
    """
    This model prints out the classification report by tweet in the testing set.
    
    ARGS:
        model (model): the model being assessed
        y_test (arr): vector of true labels for the category in question
        y_pred (arr): vector of predicted labels for category in question, based on the model
    """
    
    transpose_Y_pred = Y_pred.T
    counter = 0
    for column in Y_test.columns:
        print(column)
        print(classification_report(transpose_Y_pred[counter], Y_test[column]))
        counter += 1

def evaluate_model(model, X_test, Y_test, category_names):
    print("Optimized Parameters:", model.best_params_)
    Y_pred = model.predict(X_test)
    print("Estimator Performance:")
    display_results(model, Y_test, Y_pred)
    


def save_model(model, model_filepath):
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()