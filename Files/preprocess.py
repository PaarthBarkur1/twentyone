import numpy as np
import pandas as pd
from sklearn import preprocessing

# Handling missing data using-
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer

# Scaling and Teansforming using- 
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
 
# Handling non-numeric data using-
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder 

# Feature engineering-
# We will do it by finding co-realation between the independent features by using-
from itertools import combinations
from sklearn.preprocessing import PolynomialFeatures

# Dimensionality reduction using- 
from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA

# Feature selection-
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
# For data imbalance we just need to give a note that note that the data is having some imbalance after the training.

# from main import *
from pycaret.classification import *
from pycaret.regression import *
# from pycaret.clustering import *
# from pycaret.nlp import *
import os

class Preprocess:     
    def manual_preprocess(model_type,raw_data_address,target_variable,parameters):
        """
        parameters will have all the custom preprocessing that the user wants to do.
        Such as:
        
            df = raw_data_address (string)               (The address of the data stored in the database.)
            drop_col_name=drop_col_name (string)         (The columns that the user wants to drop.)
            impution_type = impution_type (string)       (The method of imputation that the users selects to do the imputation in the whole data set. Which includes: Mean, Media, Most frequent and KNN imputation )
            na_value = na_value (string)                 (The notation which has been used to denote the Nan or Null values in the perticular dataset.)
            encoding_type=encoding_type (string)         (The method the user selects to do the encoding on the selected cloumn)
            encode_col_name=encode_col_name (string)     (The column selected by the user to do the encoding.)
            scaling_type = scaling_type (string)         ()
            scaling_col_name=scaling_col_name (string)   ()
            target_col_name = target_col_name (string)   ()
            
        """
        
        """
        This function is for preprocessing the data when the user selects manual preprocessing.
    
        Extended description of function:-
        Parameters:
            model_type (string): The selection of the user for the model_type eg-classification/regression/clustering etc.
            raw_data_address (string): As the user uploads the raw dataset it will be saved in the database, this is the address of that saved dataset.
            target_variable (string): The user will select the target cloumn/variable and that target variable name have to be passed to the setup() in pycaret as patameter.
            manual_preprocess_config_address(string): All the preprocessing configs passed by the user will be stored in a file and we extract the data from that file.
        
        Returns:
            clean_data_address(string):
                     
        """
        df = raw_data_address
        drop_col_name=drop_col_name
        impution_type = impution_type
        impute_na_value = impute_na_value
        encoding_type=encoding_type
        encode_col_name=encode_col_name
        scaling_type = scaling_type
        scaling_col_name=scaling_col_name
        Remove_outlier = True/False
        target_col_name = target_col_name
        
        # drop columns
        if(drop_col_name[0]!="none"):
            df=df.drop(drop_col_name, axis = 1)

        #### Handling missing data
        # imputation
        if(impution_type[0]!="none"):
            df_value = df.values
            if impution_type=='mean':
                imputer = SimpleImputer(missing_value = np.NaN, strategy = 'mean')
                imputer.fit(df)
                imputed_data_value = imputer.transform(df)
                imputed_df = pd.DataFrame(imputed_data_value)

            elif impution_type=='median':
                imputer = SimpleImputer(missing_values=np.NaN, strategy = 'median')
                imputer.fit(df)
                imputed_data_value = imputer.transform(df)
                imputed_df = pd.DataFrame(imputed_data_value)
 
            elif impution_type=='most_frequent':
                imputer = SimpleImputer(missing_values=np.NaN, strategy = 'most_frequent')
                imputer.fit(df)
                imputed_data_value = imputer.transform(df)
                imputed_df = pd.DataFrame(imputed_data_value)

            elif impution_type=='knn':
                imputer = KNNImputer(n_neighbors = 4, weights = "uniform",missing_values = np.NaN)
                imputer.fit(df)
                imputed_data_value = imputer.transform(df)
                imputed_df = pd.DataFrame(imputed_data_value)
                
            elif impution_type=='Constant':
                imputer = SimpleImputer(missing_value = np.NaN, strategy = 'constant', fill_value = impute_na_value )
                imputer.fit(df)
                imputed_data_value = imputer.transform(df)
                imputed_df = pd.DataFrame(imputed_data_value)

        #feature scaling
        if(scaling_col_name[0]!="none"):
            if scaling_type == "normalization":
                x = df[scaling_col_name].values
                scaleing = MinMaxScaler()
                x_scaled = scaleing.fit_transform(x)
                df[scaling_col_name]= x_scaled

            elif scaling_type == 'standarization':
                x = df[scaling_col_name].values
                scaleing = StandardScaler()
                x_scaled = scaleing.fit_transform(x)
                df[scaling_col_name]= x_scaled
            
        #### handling catogarical data
        # encoding
        if(encode_col_name[0] != "none"):
            if encoding_type == "Label Encodeing":
                le = LabelEncoder()
                x_encoded = le.fit_transform(df[encode_col_name])
                features = x_encoded.columns
                for feature in features:
                    df.drop([feature],axis=1,inplace=True)
                    df=pd.concat([df,x_encoded[feature]],axis=1)
            elif encoding_type == "One-Hot Encoding":
                ohe = OneHotEncoder(categories = encode_col_name, sparse = False, drop = "Frist")
                x = ohe.fit_transform(df[encode_col_name])
                x_encoded = pd.DataFrame(x)
                features = x_encoded.columns
                for feature in features:
                    df.drop([feature],axis=1,inplace=True)
                    df=pd.concat([df,x_encoded[feature]],axis=1) 

        # Feature engineering & Feature Selection
        ### Outlier detection & Removel
        ### Outlier detection and removal using 3 standard deviation
        if Remove_outlier == True:
            df.outlier_col_name.mean()
            df.outlier_col_name.std()
            upper_limit = df.outlier_col_name.mean() + 3*df.outlier_col_name.std()
            lower_limit = df.outlier_col_name.mean() -3*df.outlier_col_name.std()
            df = df[(df.outlier_col_name<upper_limit) & (df.outlier_col_name>lower_limit)]
            
        # Here we are droping the feature if the column is having no variance.
        # If all the rows are having the same value the feature importance of that column is not significant for the prediction. 
        if feature_selection_type != "none":
            if feature_selection_type == "Variance Threshold":
                var_thres=VarianceThreshold(threshold=0)
                var_thres.fit(df)
                constant_columns = [column for column in df.columns if column not in df.columns[var_thres.get_support()]]
                df = df.drop(constant_columns,axis=1)
            
            if feature_selection_type == "Correlation":
                cor = df.corr()
                # with the following function we can select highly correlated features
                # it will remove the first feature that is correlated with anything other feature
                def correlation(dataset, threshold):
                    col_corr = set()  # Set of all the names of correlated columns
                    corr_matrix = dataset.corr()
                    for i in range(len(corr_matrix.columns)):
                        for j in range(i):
                            if abs(corr_matrix.iloc[i, j]) > threshold: # we are interested in absolute coeff value
                                colname = corr_matrix.columns[i]  # getting the name of column
                                col_corr.add(colname)
                    return col_corr
                corr_features = correlation(df, 0.8)
                df = df.drop(corr_features,axis=1)

                
        clean_data_address = os.getcwd()+"/clean_data.csv"
        return clean_data_address
        
#-------------------------------------------------------------------------------------------------------------------------------------------------------#
    def auto_preprocess(model_type,raw_data_address,target_variable):
        """
        This function is for preprocessing the data when the user selects auto preprocessing.
    
        Extended description of function:-
        Parameters:
            model_type (string):          (The selection of the user for the model_type eg-classification/regression/clustering etc.)
            raw_data_address (string):    (As the user uploads the raw dataset it will be saved in the database, this is the address of that saved dataset.)
            target_variable (string):     (The user will select the target cloumn/variable and that target variable name have to be passed to the setup() in pycaret as patameter.)
            
        Returns:
            clean_data_address(string): 
        """
        
        if model_type == "classification":
            clf1 = setup(data = raw_data_address, target = target_variable,silent=True, profile= True)
        
        elif model_type == "regression":
            reg1 = setup(data = raw_data_address, target = target_variable,silent=True, profile= True)

        # elif model_type == "clustering":            
        #     clu1 = setup(data = raw_data_address,silent=True, profile= True)

        # elif model_type == "nlp":            
        #     nlp1 = setup(data = raw_data_address, target = target_variable,silent=True, profile= True)
        
        X_train = get_config('X_train')        
        
        X_train.to_csv('clean_data.csv', index=False)
        
        clean_data_address = os.getcwd()+"/clean_data.csv"
        return clean_data_address
        
    #--------------------------------------------------------------------------------------------------------------------------#

    ##### This is the code which we can use if we want to go the the manual preprocessing with the implemention of pycaret.#####
     
    #--------------------------------------------------------------------------------------------------------------------------#

        # if model_type == "classification":
        #     clf1 = setup(data = raw_data_address, target = target_variable,silent=True, profile= True,manual_preprocess_config_address)
        
        # elif model_type == "regression":
        #     reg1 = setup(data = raw_data_address, target = target_variable,silent=True, profile= True,manual_preprocess_config_address)

        # # elif model_type == "clustering":            
        # #     clu1 = setup(data = raw_data_address,silent=True, profile= True,manual_preprocess_config_address)

        # # elif model_type == "nlp":            
        # #     nlp1 = setup(data = raw_data_address, target = target_variable,silent=True, profile= True,manual_preprocess_config_address)

        # X_train = get_config('X_train')
        
        # X_train.to_csv('clean_data.csv', index=False)
        
        # clean_data_address = os.getcwd()+"/clean_data.csv"
        # return clean_data_address


 #--------------------------------------------------------------------------------------------------------------------------#

##### Below is the documentation for my own refference Which contains all the preprocessing and feature engineering and feture
##### selection methods which I am planing to implement in this project

#---------------------------------------------------------------------------------------------------------------------------#

        
"""

#### Handling missing data
# - Models can not handle missing data
# - Simplest solution 
#   - Remove observation/features that have missing data.
# - But, removing missing data can introduce a lot of issuse
#   - Data is randomly missing potentially lose a lot of your data
#   - If Data is non-randomly missing, in addition to lossing data, we are also introdusing biases in our data.
#   - Usually this is a poor solution.
# - As alternative solution is to use impution.
#   - Replacing missing values with another values.
#   - We can use mean, median or the value with highest frequency.
# - We use KNN imputation which may be helpful in some case.


#### Dealing with data types.
# - We have 3 types of datatypes here i.e. Numeric, Categorical, Ordinal.
# - But the Ml models can only handle numeric features.
# - So we will convert the categorical and ordinal data into numeric.



## More data Exploration

 ### Outlier detection
 - An outliers are some values in the features which is not comparative with rest of the dataset, i.e. its value is either exceptionly high or low. So it also effects the all over decision of the model.
 - There are many methods for dealing with outlier, but we will use only two:
   - Tukey IQR
   - Kernel density estimation.
   - Use some custom function

    ### Outlier detection & Removel
    - Outlier detection and removal using 3 standard deviation


### Outlier detection using Tukey IQR (InterQuartile Range)
### Outlier detection using Kernel density estimation.
- Non-parametric way to estimate the probablity density function of a given feature.
- Can be advantageous compared to extreme value detection(i.e. Tukey IQR)
  - Capures outliers in bimodal distributions.

### Distribution of features.
- A histogram can be used to visualising the distribution of values for a given feature.
- x-axis represents value bins and y-axis represents the frequency of an observation falling into the bin.
- It is also intresting to look at distributions broken up by outcome categories.

## Feature engineering
##### As feature engineering is best done if the domain knowledge is applied. But as our aim is to do it do it without the human interaction of the user we need to look some alternative ways of doing it.
#### We will look for interaction amongst the features i.e. co-realation between the independent features.
- A simple two-way interaction is represented as:
  - X3 = X1*X2 where X3 is the interaction between X1 and X2.
- Can add interaction terms as additional new features to our model, usefull for model id the impact of two or more features on the outcome is non-additive for example:-
  - Interaction between Education and political ideology, Overcome concern about climate change.
  - While an increase in education amongst liberls or moderates increase the consern and amoungst the conservatives has the opposite effect.
  - The education-political ideology interaction captures more then the two features alone.
- The interaction amongst dummy variables belonging to the same categorical features are always zero. 
- Although it is very easy to calculate two way interactions amongst all the features it is very computationaly expensive .
  - 10 features have 45 two-way interaction terms.
  - 50 features have 1225 two-way interaction terms.
  - 100 features have 4950 two-way interaction terms.
  - Recommended understanding your data and domain if possible and selectively choosing interaction terms.


## Dimensionality reduction.
#### Dimensionality is referred to the attributes, features or independent variables of the data-set.
#### For dimensionality reduction we need to reduce the no. of features in the data-set while keeping all the important information in the data.
- We need to do dimensionality reduction because:-
  - Less no. of dimension in the data leads to lesser training time and lesser computation power, This problem is also called the **curse of dimensionality** which can be avoided by dimensionality reduction.
  - Dimensionality reduction is way to reduce the complexity of a model and avoid over fitting. 
  - It is very useful at the time of data visualisation.
  - We can also do factor analysis with it.
  - It also removes the noise from the data.
  - One more problem it deals with i.e.  **multicollineratity** , It occurs in the regression when multiple features are correlated with each other.
  - Image compression can also be performed with the help of PCA  by considering the pixels of the image as dimensions of the data .
  - We can transform the non-linear data into linear data and separate it linearly, this can by performed with the help of Kernel PCA.
- During this process we may loose around 1-15% of original data, Are we in the condition of loosing the data.
- Anyways we are going to save a copy of the original data.

## Dimensionality Reduction methods-
#### Only to keep the most important data.
- Backward elimination
- Forward elimination
- Random forests

#### To find a combination of new features.
- Linear methods
  - PCA(**Principal Component Analysis** )
  - FA(**Factor Analysis**)
  - LDA(**Linear Discriminant Analysis**)
  - Truncated SVD( **Truncated Singular Value Decomposition**)
- Linear methods(Manifold learning)
  - Kernal PCA
  - t-SNE( **t -distribution Stochastic Neighbor Embedding**)
  - MDS(**Multi Dimensional Scaling**)
  - Isomap(**Isometric Mapping**)

## We can do dimensionality reduction using:-
 - PCA(**Principal component analysis** )
  - PCA is a technique that transforms a dataset of many features into principal components that summarize the variance that underlies the data.
  - Each principal components is calculated by finding the linear combination of features that maximize variance while also ensuring zero correlation with the previously  calculated principal components.
- Use cases for modelling- 
  - One of the most common dimensionality reduction techniques.
  - Use if there  are too many features or of observation/feature ratio is poor.
  - Also,  potentially good option if there are a lot of highly correlated variables in your dataset
- One disadvantage of PCA is that it makes the data interpretation harder.

# Feature Selection
### Feature selection for supervised models using SelectKBest
- Feature selection is a technique where we choose those features in our data that contribute most to the target variable. In other words we choose the best predictors for the target variable.
- Reduces Over fitting: Less redundant data means less possibility of making decisions based on redundant data/noise.
- Improves Accuracy: Less misleading data means modelling accuracy improves.
- Reduces Training Time: Less data means that algorithms train faster.

### Finding the optimal features:
- We have many features which may look like it is important but many times they have not such significant effect on the prediction, and some time it can also have negative impact.
- For this problem we have a class RFECV in sklearn which is used for feature selection.
- REFCV stands for Recursive Feature Elimination with Cross-Validation.


###Dealing with data imbalance-
- At the end we just need to give a note that note that the data is having some imbalance after the training.


"""
