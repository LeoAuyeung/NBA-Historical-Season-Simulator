from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pandas as pd
import pickle

import matplotlib.pyplot as plt
import seaborn as sns

import os

from datetime import datetime

from sklearn.feature_selection import SelectKBest, VarianceThreshold
from sklearn.feature_selection import f_classif

home_path = os.getcwd()

def random_forest(dataframe):
    print(dataframe)
     # Features currently present within CSV data file: W_PCT,REB,TOV,PLUS_MINUS,OFF_RATING,DEF_RATING,TS_PCT
     # Total features
    features = ['W_PCT','MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','TOV','STL','BLK','BLKA',
        'PF','PFD','PTS','PLUS_MINUS','E_OFF_RATING','OFF_RATING','E_DEF_RATING','DEF_RATING','E_NET_RATING','NET_RATING','AST_PCT','AST_TO',
        'AST_RATIO','OREB_PCT','DREB_PCT','REB_PCT','TM_TOV_PCT','EFG_PCT','TS_PCT','E_PACE','PACE','PACE_PER40','POSS','PIE',]
    
    # Top 20 select KBest
    features = ['W_PCT','FGM','FG_PCT','DREB','AST',
    'BLKA','PTS','PLUS_MINUS','E_OFF_RATING','OFF_RATING',
    'E_DEF_RATING','DEF_RATING','E_NET_RATING','NET_RATING','AST_TO',
        'AST_RATIO','EFG_PCT','TS_PCT','PIE', 'FG3_PCT']
    
    # Feature set 1
    features = ['W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']
    # Feature set 2
    features = ['W_PCT','NET_RATING','PIE','PLUS_MINUS', 'DEF_RATING', 'TS_PCT', 'PTS']

    # ==================== START store necessary variables ====================


    # feature_data holds all features of W_PCT,REB,TOV,PLUS_MINUS,OFF_RATING,DEF_RATING,TS_PCT,
    feature_data = dataframe[features]

    # actual_result_data holds actual result of the games which we can then check our prediction with
    actual_result_data = dataframe.Result

    bestfeatures = SelectKBest(score_func=f_classif, k=10)
    fit = bestfeatures.fit(feature_data,actual_result_data)
    dfscores = pd.DataFrame(fit.scores_)
    dfcolumns = pd.DataFrame(feature_data.columns)
    #concat two dataframes for better visualization 
    featureScores = pd.concat([dfcolumns,dfscores],axis=1)
    featureScores.columns = ['Specs','Score']  #naming the dataframe columns
    print(featureScores.nlargest(10,'Score'))  #print 20 best features

    # Call sklearn.model_selection's train_test_split function: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    # Split arrays or matrices into random train and test subsets
    X_train, X_test, Y_train, Y_test = train_test_split(feature_data, actual_result_data, test_size=0.3, shuffle=True)

    # ==================== END store necessary variables ====================

    
    sel_variance_threshold = VarianceThreshold() 
    X_train_remove_variance = sel_variance_threshold.fit_transform(X_train)
    print(X_train_remove_variance.shape)


    # ==================== START applying random forest ====================
    # Create a Gaussian Classifier
    random_forest_result = RandomForestClassifier(n_estimators=100)

    # Train the model using the training sets
    random_forest_result.fit(X_train,Y_train)

    # Predict class labels for samples in X
    Y_pred = random_forest_result.predict(X_test)
    
    # Call sklearn's metric's confusion_matrix function: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
    # Compute confusion matrix to evaluate the accuracy of a classification
    confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)
    
    # ==================== END applying random forest ====================


    # ==================== Print model accuracy information ====================
    print('\nFeature Importance: \n')
    print(random_forest_result.feature_importances_)

    print('\n----------------------------------')

    # Printing accuracy, precision, and recall based on metrics data
    print("Accuracy: ", metrics.accuracy_score(Y_test, Y_pred))
    print("Precision: ", metrics.precision_score(Y_test, Y_pred))
    print("Recall: ", metrics.recall_score(Y_test, Y_pred))

    print('----------------------------------\n')

    # Print confusion matrix
    print('Confusion Matrix:')
    print(confusion_matrix)
    
    # Create an array with features and their correspodning importance values
    feature_imp = pd.Series(random_forest_result.feature_importances_,index=features).sort_values(ascending=False)
    
    # Creating a bar plot
    sns.barplot(x=feature_imp, y=feature_imp.index)

    # Add labels to your graph
    plt.xlabel('Feature Importance Score')
    plt.ylabel('Features')
    plt.title("Visualizing Important Features")
    plt.show()

    return random_forest_result



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
    feature_coefficients = []
    for i in range(len(features)):  # Prints each feature next to its corresponding coefficient in the model

        # Get feature name and corresponding coefficients
        log_reg_coefficients = log_reg_result.coef_
        curr_feature = features[i]
        curr_coefficient = log_reg_coefficients[0][i]

        feature_coefficients.append(curr_coefficient)

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

    # Create an array with features and their correspodning coefficient values
    feature_coefficients = pd.Series(feature_coefficients,index=features).sort_values(ascending=False)

    # Creating a bar plot
    sns.barplot(x=feature_coefficients, y=feature_coefficients.index)

    # Add labels to graph
    plt.xlabel('Feature Coefficient')
    plt.ylabel('Features')
    plt.title("Visualizing Feature Coefficients")
    # plt.show()

    return log_reg_result
    
# Create new training model and save after training
def create_model(name="random_forest_model"):
    now = datetime.now()
    now_str = now.strftime("%Y%m%d")

    filename = f'{name}_{now_str}.pkl'

    # Set directory to Data
    os.chdir(home_path + '/Data')

    all_games_dataframe = pd.read_csv(home_path + '/Data/MoreInfoData/COMBINEDgamesWithMoreInfo2010-15.csv')

    # Train logistic regression model based on the dataframe given by CSV
    # logistic_regression_model = logistic_regression(all_games_dataframe)
    random_forest_model = random_forest(all_games_dataframe)

    # Set directory to SavedModels
    os.chdir(home_path + '/SavedModels')

    # Save Model
    with open(filename, 'wb') as file:
        pickle.dump(random_forest_model, file)

if __name__ == "__main__":
    create_model()
