# Disaster Response Pipeline Project
This project, as part of Udacity's [Data Scientist nanodegree program](https://www.udacity.com/course/data-scientist-nanodegree--nd025), had me design an ETL pipeline, create an optimized model through gridsearch, then export my model to a web dashboard along with two charts through Plotly to show the struvture of the underlying data.

### Prerequisites:
* re
* numpy
* pandas
* sqlalchemy
* sqlite3
* nltk
* sklearn
* pickle
* json
* plotly
* flask

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

### Acknowledgements:
Thank you to Udacity and Figure Eight for their instuctions and data in getting this project off the ground
