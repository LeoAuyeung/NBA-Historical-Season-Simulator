from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pandas as pd
import pickle

import os

from datetime import datetime

home_path = os.getcwd()

def logistic_regression(dataframe):

    # Features currently present within CSV data file: W_PCT,REB,TOV,PLUS_MINUS,OFF_RATING,DEF_RATING,TS_PCT
    features = ['W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']

    # ==================== START store necessary variables ====================

    # feature_data holds all features of W_PCT,REB,TOV,PLUS_MINUS,OFF_RATING,DEF_RATING,TS_PCT,
    feature_data = dataframe[features]

    # actual_result_data holds actual result of the games which we can then check our prediction with
    actual_result_data = dataframe.Result

    # Call sklearn.model_selection's train_test_split function: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    # Split arrays or matrices into random train and test subsets
    X_train, X_test, Y_train, Y_test = train_test_split(feature_data, actual_result_data, test_size=0.25, shuffle=True)

    # ==================== END store necessary variables ====================


    # ==================== START applying logistic regression ====================

    # Call sklearn.linear_model's Logistic Regression function: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
    log_reg_result = LogisticRegression()

    # Fit the model according to the given training data.
    log_reg_result.fit(X_train, Y_train)

    # Predict class labels for samples in X
    Y_pred = log_reg_result.predict(X_test)

    # Call sklearn's metric's confusion_matrix function: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
    # Compute confusion matrix to evaluate the accuracy of a classification
    confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)

    # ==================== END applying logistic regression ====================


    # ==================== Print model accuracy information ====================
    print('\nCoefficient Information: \n')

    # Loop through each feature
    for i in range(len(features)):  # Prints each feature next to its corresponding coefficient in the model

        # Get feature name and corresponding coefficients
        log_reg_coefficients = log_reg_result.coef_
        curr_feature = features[i]
        curr_coefficient = log_reg_coefficients[0][i]

        # Print them
        print(curr_feature + ': ' + str(curr_coefficient))

    print('\n----------------------------------')

    # Printing accuracy, precision, and recall based on metrics data
    print("Accuracy: ", metrics.accuracy_score(Y_test, Y_pred))
    print("Precision: ", metrics.precision_score(Y_test, Y_pred))
    print("Recall: ", metrics.recall_score(Y_test, Y_pred))

    print('----------------------------------\n')

    # Print confusion matrix
    print('Confusion Matrix:')
    print(confusion_matrix)

    return log_reg_result
    
# Create new training model and save after training
def create_model(name="model"):
    now = datetime.now()
    now_str = now.strftime("%Y%m%d")

    filename = f'{name}_{now_str}.pkl'

    # Set directory to Data
    os.chdir(home_path + '/Data')

    all_games_dataframe = pd.read_csv('COMBINEDgamesWithInfo2016-19.csv')

    # Train logistic regression model based on the dataframe given by CSV
    logistic_regression_model = logistic_regression(all_games_dataframe)

    # Set directory to SavedModels
    os.chdir(home_path + '/SavedModels')

    # Save Model
    with open(filename, 'wb') as file:
        pickle.dump(logistic_regression_model, file)

if __name__ == "__main__":
    create_model()