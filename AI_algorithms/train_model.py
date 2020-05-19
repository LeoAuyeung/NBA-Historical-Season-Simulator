from sklearn.model_selection import train_test_split
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

from sklearn.feature_selection import SelectKBest, f_classif

home_path = os.getcwd()


#k nearest neighbors
def knn(dataframe):

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


	# ==================== START applying k nearest neighbors ====================

	#Call KNeighborsClassifier from https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
	neighbors = 2
	knn_result = KNeighborsClassifier(n_neighbors=neighbors)
	print('n_neighbors = ', neighbors)

	# Fit the model according to the given training data.
	knn_result.fit(X_train, Y_train);

	# Predict class labels for samples in X
	Y_pred = knn_result.predict(X_test)

	# Call sklearn's metric's confusion_matrix function: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
	# Compute confusion matrix to evaluate the accuracy of a classification
	confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)

	# ==================== END applying k nearest neighbors ====================


	# ==================== Print model accuracy information ====================
	# Printing accuracy, precision, and recall based on metrics data
	print("Accuracy: ", metrics.accuracy_score(Y_test, Y_pred))
	print("Precision: ", metrics.precision_score(Y_test, Y_pred))
	print("Recall: ", metrics.recall_score(Y_test, Y_pred))

	print('----------------------------------\n')

	# Print confusion matrix
	print('Confusion Matrix:')
	print(confusion_matrix)

	return knn_result
   
def random_forest(dataframe):
     # Features currently present within CSV data file: W_PCT,REB,TOV,PLUS_MINUS,OFF_RATING,DEF_RATING,TS_PCT
     # Total features
    # features = ['W_PCT','MIN','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','TOV','STL','BLK','BLKA',
    #     'PF','PFD','PTS','PLUS_MINUS','E_OFF_RATING','OFF_RATING','E_DEF_RATING','DEF_RATING','E_NET_RATING','NET_RATING','AST_PCT','AST_TO',
    #     'AST_RATIO','OREB_PCT','DREB_PCT','REB_PCT','TM_TOV_PCT','EFG_PCT','TS_PCT','E_PACE','PACE','PACE_PER40','POSS','PIE',]
    
    # Original Feature Set
    # features = ['W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']

    # Top 10 feature importance
    # features = ['W_PCT','NET_RATING','PLUS_MINUS','PIE','E_NET_RATING','DEF_RATING','E_OFF_RATING','OFF_RATING','PTS', 'TS_PCT']

    # Top 10 K-best
    features = ['W_PCT','NET_RATING','PLUS_MINUS','E_NET_RATING','PIE','E_OFF_RATING','PTS','OFF_RATING','TS_PCT','E_DEF_RATING']

    # ==================== START store necessary variables ====================

    # feature_data holds all features of W_PCT,REB,TOV,PLUS_MINUS,OFF_RATING,DEF_RATING,TS_PCT,
    feature_data = dataframe[features]

    # actual_result_data holds actual result of the games which we can then check our prediction with
    actual_result_data = dataframe.Result

    # # Select 10 best features.
    # best_features = SelectKBest(score_func=f_classif, k=20)
    # fit = best_features.fit(feature_data,actual_result_data)
    # dfscores = pd.DataFrame(fit.scores_)
    # dfcolumns = pd.DataFrame(feature_data.columns)

    # # Concat two dataframes for better visualization 
    # featureScores = pd.concat([dfcolumns,dfscores],axis=1)
    # featureScores.columns = ['Specs','Score']
    # print(featureScores.nlargest(20,'Score'))

    # Call sklearn.model_selection's train_test_split function: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
    # Split arrays or matrices into random train and test subsets
    X_train, X_test, Y_train, Y_test = train_test_split(feature_data, actual_result_data, test_size=0.3, shuffle=True)

    # ==================== END store necessary variables ====================

    # ==================== START applying random forest ====================
    # Create a Gaussian Classifier
    random_forest_result = RandomForestClassifier(n_estimators=500, criterion='gini', max_depth=4, max_features='auto')

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

def decision_tree(dataframe):
	 # Features currently present within CSV data file: W_PCT,REB,TOV,PLUS_MINUS,OFF_RATING,DEF_RATING,TS_PCT
	features = ['W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']

	# feature_data holds all features of W_PCT,REB,TOV,PLUS_MINUS,OFF_RATING,DEF_RATING,TS_PCT,
	feature_data = dataframe[features]

	# actual_result_data holds actual result of the games which we can then check our prediction with
	actual_result_data = dataframe.Result

	# Call sklearn.model_selection's train_test_split function: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
	# Split arrays or matrices into random train and test subsets
	X_train, X_test, Y_train, Y_test = train_test_split(feature_data, actual_result_data, test_size=0.25, shuffle=True)

	# Call sklearn.linear_model's Logistic Regression function: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
	decision_tree_result = DecisionTreeClassifier()

	# Fit the model according to the given training data.
	decision_tree_result.fit(X_train, Y_train)

	# Predict class labels for samples in X
	Y_pred = decision_tree_result.predict(X_test)

	# Call sklearn's metric's confusion_matrix function: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
	# Compute confusion matrix to evaluate the accuracy of a classification
	confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)

	print('\n----------------------------------')

	# Printing accuracy, precision, and recall based on metrics data
	print("Accuracy: ", metrics.accuracy_score(Y_test, Y_pred))
	print("Precision: ", metrics.precision_score(Y_test, Y_pred))
	print("Recall: ", metrics.recall_score(Y_test, Y_pred))

	print('----------------------------------\n')

	# Print confusion matrix
	print('Confusion Matrix:')
	print(confusion_matrix)

	return decision_tree_result

def gaussian_nb(dataframe):

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


    # ==================== START applying Gaussian NB ====================

    # Call sklearn.naive_bayes's GaussianNB function: https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html
    result = GaussianNB()

    # Fit the model according to the given training data.
    result.fit(X_train, Y_train)

    # Predict class labels for samples in X
    Y_pred = result.predict(X_test)

    # Call sklearn's metric's confusion_matrix function: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
    # Compute confusion matrix to evaluate the accuracy of a classification
    confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)

    # ==================== END applying Gaussian NB ====================


    # ==================== Print model accuracy information ====================
    print('\Sigma (variance) Information: \n')

    # Loop through each feature
    for i in range(len(features)):  # Prints each feature next to its corresponding coefficient in the model

        # Get feature name and corresponding sigmas
        sigmas = result.sigma_
        curr_feature = features[i]
        curr_coefficient = sigmas[0][i]

        # Print them
        print(curr_feature + ': ' + str(curr_coefficient))

    print('\n----------------------------------')

    print('\Theta (mean) Information: \n')

    # Loop through each feature
    for i in range(len(features)):  # Prints each feature next to its corresponding coefficient in the model

        # Get feature name and corresponding thetas
        thetas = result.theta_
        curr_feature = features[i]
        curr_coefficient = thetas[0][i]

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

    return result

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

def majority_vote(dataframe):
	features = ['W_PCT', 'REB', 'TOV', 'PLUS_MINUS', 'OFF_RATING', 'DEF_RATING', 'TS_PCT']

	# feature_data holds all features of W_PCT,REB,TOV,PLUS_MINUS,OFF_RATING,DEF_RATING,TS_PCT,
	feature_data = dataframe[features]

	# actual_result_data holds actual result of the games which we can then check our prediction with
	actual_result_data = dataframe.Result

	# Call sklearn.model_selection's train_test_split function: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
	# Split arrays or matrices into random train and test subsets
	X_train, X_test, Y_train, Y_test = train_test_split(feature_data, actual_result_data, test_size=0.25, shuffle=True)

	clf1 = LogisticRegression(multi_class='multinomial', random_state=1)
	clf2 = RandomForestClassifier(n_estimators=50, random_state=1)
	clf3 = GaussianNB()

	eclf1 = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='hard')

	eclf1 = eclf1.fit(X_train, Y_train)

	Y_pred = eclf1.predict(X_test)

	confusion_matrix = metrics.confusion_matrix(Y_test, Y_pred)

	print('\n----------------------------------')

	# Printing accuracy, precision, and recall based on metrics data
	print("Accuracy: ", metrics.accuracy_score(Y_test, Y_pred))
	print("Precision: ", metrics.precision_score(Y_test, Y_pred))
	print("Recall: ", metrics.recall_score(Y_test, Y_pred))

	print('----------------------------------\n')

	# Print confusion matrix
	print('Confusion Matrix:')
	print(confusion_matrix)

	return eclf1

def create_model_helper(df, model_name):
	if model_name == "log_reg":
		model = logistic_regression(df)
	elif model_name == "knn":
		model = knn(df)
	elif model_name == "random_forest":
		model = random_forest(df)
	elif model_name == "dTree":
		model = decision_tree(df)
	elif model_name == "gaussian_nb":
		model = gaussian_nb(df)
	elif model_name == "majority":
		model = majority_vote(df)

	return model

# Create new training model and save after training
def create_model(name="model"):
	now = datetime.now()
	now_str = now.strftime("%Y%m%d%H%M%S")

	model_names = ["log_reg", "knn", "random_forest", "dTree", "gaussian_nb", "majority"]
	model_name=model_names[2]

	filename = f'{name}_{model_name}_{now_str}.pkl'

	# Set directory to Data
<<<<<<< HEAD
	os.chdir(home_path + '/Data/IncompleteData/')
	all_games_dataframe = pd.read_csv('COMBINEDgamesWithMoreInfo2010-15.csv')
=======
	os.chdir(home_path + '/Data/MoreInfoData/')
	all_games_dataframe = pd.read_csv('NEWgamesWithMoreInfo2010-15.csv')
>>>>>>> c8c2a32a5d1ea6ba8215df3100183e7a32a9ebb9

	model = create_model_helper(all_games_dataframe, model_name)

	# Set directory to SavedModels
	os.chdir(home_path + '/SavedModels')

	# Save Model
	with open(filename, 'wb') as file:
		pickle.dump(model, file)

if __name__ == "__main__":
	create_model()