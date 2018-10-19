import sys
import re
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    """
    This function loads the data from two CSVs and concatenates them together on the message id number.
    
    ARGS:
        messages_filepath (str): the filepath to the messages csv
        categories_filepath (str): the filepath to the categories csv
        
    RETURNS:
        df (dataframe)
    """
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = pd.merge(messages, categories, how="inner", on="id")
    return df
    

def clean_data(df):
    """
    This function cleans the dataframe by expanding the categories column into new, one-hot encoded columns,
        dropping the original column, concatenating the expanded columns onto the original dataframe, and 
        dropping duplicate messages.
        
    ARGS:
        df (pandas dataframe)
    
    RETURNS:
        df (dataframe)
    """
    categories = df["categories"].str.split(";", expand = True)
    row = categories.iloc[0]
    category_colnames = [re.sub(r'\-[0-1]', '', i) for i in row]
    categories.columns = category_colnames
    for column in categories:
        categories[column] = [i[-1] for i in categories[column]]
        categories[column] = [int(i) for i in categories[column]]
    df = df.drop(["categories"], axis = 1)
    df = pd.concat([df, categories], axis = 1)
    df = df.drop_duplicates("original")
    return df


def save_data(df, database_filename):
    """
    This function saves the data to a sqlite database
    
    ARGS:
        df (dataframe)
        database_filename (str): the filename to which we will save the dataframe in sqlite
        
    RETURNS:
        None
    """
    print("Database filename is: {}".format(database_filename))
    engine = create_engine('sqlite:///data/DisasterResponse.db')
    df.to_sql(database_filename, engine, index=False)  


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()