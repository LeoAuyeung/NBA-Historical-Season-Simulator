from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics, datasets

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle
import os
from datetime import datetime


home_path = os.getcwd()

os.chdir(home_path + '/Data/MoreInfoData/')
all_games_dataframe = pd.read_csv('COMBINEDgamesWithMoreInfo2010-15.csv')

features = ['W_PCT','NET_RATING','PLUS_MINUS','E_NET_RATING','PIE','E_OFF_RATING','PTS','OFF_RATING','TS_PCT','E_DEF_RATING']

feature_data = all_games_dataframe[features]
actual_result_data = all_games_dataframe.Result

x_train, x_test, y_train, y_test = train_test_split(feature_data, actual_result_data, test_size=0.3, random_state=42)

rfc=RandomForestClassifier(random_state=42)

param_grid = { 
    'n_estimators': [200, 500],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [4,5,6,7,8],
    'criterion' :['gini', 'entropy']
}

CV_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv= 5)
CV_rfc.fit(x_train, y_train)


print(CV_rfc.best_params_)

# from sklearn.model_selection import RandomizedSearchCV
# # Number of trees in random forest
# n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# # Number of features to consider at every split
# max_features = ['auto', 'sqrt']
# # Maximum number of levels in tree
# max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
# max_depth.append(None)
# # Minimum number of samples required to split a node
# min_samples_split = [2, 5, 10]
# # Minimum number of samples required at each leaf node
# min_samples_leaf = [1, 2, 4]
# # Method of selecting samples for training each tree
# bootstrap = [True, False]
# # Create the random grid
# random_grid = {'n_estimators': n_estimators,
#                'max_features': max_features,
#                'max_depth': max_depth,
#                'min_samples_split': min_samples_split,
#                'min_samples_leaf': min_samples_leaf,
#                'bootstrap': bootstrap}
# pprint(random_grid)


def random_forest(dataframe):
     # Features currently present within CSV data file: W_PCT,REB,TOV,PLUS_MINUS,OFF_RATING,DEF_RATING,TS_PCT
     # Total features
    # features = ['W_PCT','MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','TOV','STL','BLK','BLKA',
    #     'PF','PFD','PTS','PLUS_MINUS','E_OFF_RATING','OFF_RATING','E_DEF_RATING','DEF_RATING','E_NET_RATING','NET_RATING','AST_PCT','AST_TO',
    #     'AST_RATIO','OREB_PCT','DREB_PCT','REB_PCT','TM_TOV_PCT','EFG_PCT','TS_PCT','E_PACE','PACE','PACE_PER40','POSS','PIE',]
    
    # Original Feature Set
    features = ['W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']

    # Top 10 feature importance
    # features = ['W_PCT','NET_RATING','PLUS_MINUS','PIE','E_NET_RATING','DEF_RATING','E_OFF_RATING','OFF_RATING','PTS', 'TS_PCT']

    # Top 10 K-best 
    features = ['W_PCT','NET_RATING','PLUS_MINUS','E_NET_RATING','PIE','E_OFF_RATING','PTS','OFF_RATING','TS_PCT','E_DEF_RATING']

    # ==================== START store necessary variables ====================

    # feature_data holds all features of W_PCT,REB,TOV,PLUS_MINUS,OFF_RATING,DEF_RATING,TS_PCT,
    feature_data = dataframe[features]

    # actual_result_data holds actual result of the games which we can then check our prediction with
    actual_result_data = dataframe.Result

    # Select 10 best features.
    # best_features = SelectKBest(score_func=f_classif, k=10)
    # fit = best_features.fit(feature_data,actual_result_data)
    # dfscores = pd.DataFrame(fit.scores_)
    # dfcolumns = pd.DataFrame(feature_data.columns)

    # Concat two dataframes for better visualization 
    # featureScores = pd.concat([dfcolumns,dfscores],axis=1)
    # featureScores.columns = ['Specs','Score']
    # print(featureScores.nlargest(10,'Score'))

    # Call sklearn.model_selection's train_test_split function: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    # Split arrays or matrices into random train and test subsets
    X_train, X_test, Y_train, Y_test = train_test_split(feature_data, actual_result_data, test_size=0.25, shuffle=True)

    # ==================== END store necessary variables ====================

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
    # print('\nFeature Importance: \n')
    # print(random_forest_result.feature_importances_)

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
    # plt.xlabel('Feature Importance Score')
    # plt.ylabel('Features')
    # plt.title("Visualizing Important Features")
    # plt.show()

    return random_forest_result