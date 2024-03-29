# %%
import pandas as pd
from sklearn import preprocessing
from sklearn.discriminant_analysis import StandardScaler
import numpy as np
import warnings
warnings.filterwarnings("ignore")
# attach the column names to the dataset
feature=["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot",
          "num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells",
          "num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
          "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count", 
          "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
          "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"]



# KDDTrain+_2.csv & KDDTest+_2.csv are the datafiles without the last column about the difficulty score
# these have already been removed.

train='KDDTrain+.txt'
test='KDDTest+.txt'

df=pd.read_csv(train,names=feature)

df_test=pd.read_csv(test,names=feature)


# shape, this gives the dimensions of the dataset
print('Dimensions of the Training set:',df.shape)
print('Dimensions of the Test set:',df_test.shape)


df.drop(['difficulty'],axis=1,inplace=True)
df_test.drop(['difficulty'],axis=1,inplace=True)


print('Label distribution Training set:')
print(df['label'].value_counts())
print()
print('Label distribution Test set:')
print(df_test['label'].value_counts())


# colums that are categorical and not binary yet: protocol_type (column 2), service (column 3), flag (column 4).
# explore categorical features
print('Training set:')
for col_name in df.columns:
    if df[col_name].dtypes == 'object' :
        unique_cat = len(df[col_name].unique())
        print("Feature '{col_name}' has {unique_cat} categories".format(col_name=col_name, unique_cat=unique_cat))

#see how distributed the feature service is, it is evenly distributed and therefore we need to make dummies for all.
print()
print('Distribution of categories in service:')
print(df['service'].value_counts().sort_values(ascending=False).head())

# Test set
print('Test set:')
for col_name in df_test.columns:
    if df_test[col_name].dtypes == 'object' :
        unique_cat = len(df_test[col_name].unique())
        print("Feature '{col_name}' has {unique_cat} categories".format(col_name=col_name, unique_cat=unique_cat))


from sklearn.preprocessing import LabelEncoder,OneHotEncoder
categorical_columns=['protocol_type', 'service', 'flag']
# insert code to get a list of categorical columns into a variable, categorical_columns
categorical_columns=['protocol_type', 'service', 'flag'] 
 # Get the categorical values into a 2D numpy array
df_categorical_values = df[categorical_columns]
testdf_categorical_values = df_test[categorical_columns]
df_categorical_values.head()


# protocol type
unique_protocol=sorted(df.protocol_type.unique())
string1 = 'Protocol_type_'
unique_protocol2=[string1 + x for x in unique_protocol]
# service
unique_service=sorted(df.service.unique())
string2 = 'service_'
unique_service2=[string2 + x for x in unique_service]
# flag
unique_flag=sorted(df.flag.unique())
string3 = 'flag_'
unique_flag2=[string3 + x for x in unique_flag]
# put together
dumcols=unique_protocol2 + unique_service2 + unique_flag2
print(dumcols)

#do same for test set
unique_service_test=sorted(df_test.service.unique())
unique_service2_test=[string2 + x for x in unique_service_test]
testdumcols=unique_protocol2 + unique_service2_test + unique_flag2


df_categorical_values_enc=df_categorical_values.apply(LabelEncoder().fit_transform)
print(df_categorical_values_enc.head())
# test set
testdf_categorical_values_enc=testdf_categorical_values.apply(LabelEncoder().fit_transform)



enc = OneHotEncoder()
df_categorical_values_encenc = enc.fit_transform(df_categorical_values_enc)
df_cat_data = pd.DataFrame(df_categorical_values_encenc.toarray(),columns=dumcols)
# test set
testdf_categorical_values_encenc = enc.fit_transform(testdf_categorical_values_enc)
testdf_cat_data = pd.DataFrame(testdf_categorical_values_encenc.toarray(),columns=testdumcols)

df_cat_data.head()


trainservice=df['service'].tolist()
testservice= df_test['service'].tolist()
difference=list(set(trainservice) - set(testservice))
string = 'service_'
difference=[string + x for x in difference]
difference


for col in difference:
    testdf_cat_data[col] = 0

testdf_cat_data.shape



newdf=df.join(df_cat_data)
newdf.drop('flag', axis=1, inplace=True)
newdf.drop('protocol_type', axis=1, inplace=True)
newdf.drop('service', axis=1, inplace=True)
# test data
newdf_test=df_test.join(testdf_cat_data)
newdf_test.drop('flag', axis=1, inplace=True)
newdf_test.drop('protocol_type', axis=1, inplace=True)
newdf_test.drop('service', axis=1, inplace=True)
print(newdf.shape)
print(newdf_test.shape)

# take label column
labeldf=newdf['label']
labeldf_test=newdf_test['label']
# change the label column
newlabeldf=labeldf.replace({ 'normal' : 0, 'neptune' : 1 ,'back': 1, 'land': 1, 'pod': 1, 'smurf': 1, 'teardrop': 1,'mailbomb': 1, 'apache2': 1, 'processtable': 1, 'udpstorm': 1, 'worm': 1,
                           'ipsweep' : 2,'nmap' : 2,'portsweep' : 2,'satan' : 2,'mscan' : 2,'saint' : 2
                           ,'ftp_write': 3,'guess_passwd': 3,'imap': 3,'multihop': 3,'phf': 3,'spy': 3,'warezclient': 3,'warezmaster': 3,'sendmail': 3,'named': 3,'snmpgetattack': 3,'snmpguess': 3,'xlock': 3,'xsnoop': 3,'httptunnel': 3,
                           'buffer_overflow': 4,'loadmodule': 4,'perl': 4,'rootkit': 4,'ps': 4,'sqlattack': 4,'xterm': 4})
newlabeldf_test=labeldf_test.replace({ 'normal' : 0, 'neptune' : 1 ,'back': 1, 'land': 1, 'pod': 1, 'smurf': 1, 'teardrop': 1,'mailbomb': 1, 'apache2': 1, 'processtable': 1, 'udpstorm': 1, 'worm': 1,
                           'ipsweep' : 2,'nmap' : 2,'portsweep' : 2,'satan' : 2,'mscan' : 2,'saint' : 2
                           ,'ftp_write': 3,'guess_passwd': 3,'imap': 3,'multihop': 3,'phf': 3,'spy': 3,'warezclient': 3,'warezmaster': 3,'sendmail': 3,'named': 3,'snmpgetattack': 3,'snmpguess': 3,'xlock': 3,'xsnoop': 3,'httptunnel': 3,
                           'buffer_overflow': 4,'loadmodule': 4,'perl': 4,'rootkit': 4,'ps': 4,'sqlattack': 4,'xterm': 4})
# put the new label column back
newdf['label'] = newlabeldf
newdf_test['label'] = newlabeldf_test
print(newdf['label'].head())

# creating a dataframe with multi-class labels (Dos,Probe,R2L,U2R,normal)
multi_data = newdf.copy()
multi_label = pd.DataFrame(multi_data.label)

multi_data_test=newdf_test.copy()
multi_label_test = pd.DataFrame(multi_data_test.label)

# using standard scaler for normalizing
std_scaler = StandardScaler()
def standardization(df,col):
    for i in col:
        arr = df[i]
        arr = np.array(arr)
        df[i] = std_scaler.fit_transform(arr.reshape(len(arr),1))
    return df

numeric_col = multi_data.select_dtypes(include='number').columns
data = standardization(multi_data,numeric_col)
numeric_col_test = multi_data_test.select_dtypes(include='number').columns
data_test = standardization(multi_data_test,numeric_col_test)

# label encoding (0,1,2,3,4) multi-class labels (Dos,normal,Probe,R2L,U2R)
le2 = preprocessing.LabelEncoder()
le2_test = preprocessing.LabelEncoder()
enc_label = multi_label.apply(le2.fit_transform)
enc_label_test = multi_label_test.apply(le2_test.fit_transform)
multi_data = multi_data.copy()
multi_data_test = multi_data_test.copy()

multi_data['intrusion'] = enc_label
multi_data_test['intrusion'] = enc_label_test

# Specify the name of the output text file
output_file_name = "Wilcoxon_NSL_test.txt"
with open(output_file_name, "w") as f: print('---------------------------------------------------------------------------------', file = f)
###################################################
###################################################
###################################################
###################################################
#y_mul = multi_data['intrusion']
multi_data
multi_data_test


multi_data.drop(labels= [ 'label'], axis=1, inplace=True)
multi_data = multi_data.sample(frac = 0.333)
multi_data_test.drop(labels= [ 'label'], axis=1, inplace=True)
# multi_data_test=multi_data_test.sample(frac = 0.003)
# feature = [
#             'dst_host_same_srv_rate',
#             'dst_host_srv_count',
#             'dst_host_same_src_port_rate',
#             'logged_in',
#             'dst_host_serror_rate',
#             'count',
#             'srv_count',
#             'dst_host_rerror_rate',
#             'label'
#             ]
# multi_data_test = multi_data_test.sample(frac=0.0001)
# multi_data_test = multi_data_test[feature]
# df_test = df_test.sample(frac=0.1)

y_train_multi= multi_data[['intrusion']]
X_train_multi= multi_data.drop(labels=['intrusion'], axis=1)

y = y_train_multi
X = X_train_multi

print("X len is", len(X))
print("y len is", len(y))
# print('X_train has shape:',X_train_multi.shape,'\ny_train has shape:',y_train_multi.shape)

# y_test_multi= multi_data_test[['intrusion']]
# X_test_multi= multi_data_test.drop(labels=['intrusion'], axis=1)

# print('X_test has shape:',X_test_multi.shape,'\ny_test has shape:',y_test_multi.shape)



# from collections import Counter

# label_counts = Counter(y_train_multi['intrusion'])
# print(label_counts)



# from sklearn.preprocessing import LabelBinarizer

# y_train_multi = LabelBinarizer().fit_transform(y_train_multi)
# y_train_multi

# y_test_multi = LabelBinarizer().fit_transform(y_test_multi)
# y_test_multi


# Y_train=y_train_multi.copy()
# X_train=X_train_multi.copy()

# Y_test=y_test_multi.copy()
# X_test=X_test_multi.copy()


# %%
feature_selection = [
                    'dst_host_same_srv_rate',
                    'dst_host_srv_count',
                    'dst_host_same_src_port_rate',
                    'logged_in',
                    'dst_host_serror_rate',
                    'count',
                    'srv_count',
                    'dst_host_rerror_rate'
                    # 'Label'
                    ]

# single_class_train = np.argmax(y_train_multi, axis=1)
# single_class_test = np.argmax(y_test_multi, axis=1)

# X_train = X_train.assign(label = single_class_train)
# X_test = X_test.assign(label = single_class_test)



# X_train = X_train.sample(frac = 0.3)
# X_test = X_test.sample(frac = 0.3)

# Y_train = X_train.pop('label')
# Y_test = X_test.pop('label')

# X_train = X_train[feature_selection]
# X_test = X_test[feature_selection]

# %%
#Model Parameters RF
from sklearn.ensemble import RandomForestClassifier
max_depth = 5
n_estimators = 5
min_samples_split = 2

print('---------------------------------------------------------------------------------')
print('Defining the RF model')
print('---------------------------------------------------------------------------------')
print('')

rf = RandomForestClassifier(max_depth = max_depth,  n_estimators = n_estimators, min_samples_split = min_samples_split, n_jobs = -1)

# model = clf.fit(X, y)

# %%
#Model Parameters SVM
from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import SGDClassifier

max_iter=10
loss='hinge'
gamma=0.1


rbf_feature = RBFSampler(gamma=gamma, random_state=1)
X_features = rbf_feature.fit_transform(X)
svm = SGDClassifier(max_iter=max_iter,loss=loss)
# clf.fit(X_features, y_train)
# clf.score(X_features, y_train)


# %%
#Model Parameters ADA
from sklearn.ensemble import AdaBoostClassifier
n_estimators=30
learning_rate=0.5

ada = AdaBoostClassifier(n_estimators=n_estimators,learning_rate=learning_rate)


# %%

# #Model Parameters DNN
# import tensorflow as tf
# dropout_rate = 0.01
# nodes = 70
# out_layer = 7
# optimizer='adam'
# loss='sparse_categorical_crossentropy'
# epochs=5
# batch_size=2*256


# print('---------------------------------------------------------------------------------')
# print('Defining the DNN model')
# print('---------------------------------------------------------------------------------')
# print('')


# num_columns = X_train.shape[1]

# dnn = tf.keras.Sequential()

# # Input layer
# dnn.add(tf.keras.Input(shape=(num_columns,)))

# # Dense layers with dropout
# dnn.add(tf.keras.layers.Dense(nodes))
# dnn.add(tf.keras.layers.Dropout(dropout_rate))

# dnn.add(tf.keras.layers.Dense(nodes))
# dnn.add(tf.keras.layers.Dropout(dropout_rate))

# dnn.add(tf.keras.layers.Dense(nodes))
# dnn.add(tf.keras.layers.Dropout(dropout_rate))

# dnn.add(tf.keras.layers.Dense(nodes))
# dnn.add(tf.keras.layers.Dropout(dropout_rate))

# dnn.add(tf.keras.layers.Dense(nodes))
# dnn.add(tf.keras.layers.Dropout(dropout_rate))

# # Output layer
# dnn.add(tf.keras.layers.Dense(out_layer))



# dnn.compile(optimizer=optimizer, loss=loss)

# dnn.summary()

import tensorflow as tf
from scikeras.wrappers import KerasClassifier, KerasRegressor

def getModel(optimizer):


    num_columns = X_train.shape[1]

    dnn = tf.keras.Sequential()

    # Input layer
    dnn.add(tf.keras.Input(shape=(num_columns,)))

    # Dense layers with dropout
    dnn.add(tf.keras.layers.Dense(nodes))
    dnn.add(tf.keras.layers.Dropout(dropout_rate))

    dnn.add(tf.keras.layers.Dense(nodes))
    dnn.add(tf.keras.layers.Dropout(dropout_rate))

    dnn.add(tf.keras.layers.Dense(nodes))
    dnn.add(tf.keras.layers.Dropout(dropout_rate))

    dnn.add(tf.keras.layers.Dense(nodes))
    dnn.add(tf.keras.layers.Dropout(dropout_rate))

    dnn.add(tf.keras.layers.Dense(nodes))
    dnn.add(tf.keras.layers.Dropout(dropout_rate))

    # Output layer
    dnn.add(tf.keras.layers.Dense(out_layer))



    dnn.compile(optimizer=optimizer, loss=loss)

    return dnn


#Model Parameters DNN
dropout_rate = 0.01
nodes = 70
out_layer = 7
optimizer='adam'
loss='sparse_categorical_crossentropy'
epochs=5
batch_size=2*256
# optimizer = ['Adam']
epochs = [5]


param_grid = dict(epochs=epochs, optimizer=optimizer)
dnn_Kmodel = KerasClassifier(build_fn=getModel, verbose=1)

# %%
#Model Parameters KNN
from sklearn.neighbors import KNeighborsClassifier
n_neighbors=5

knn_clf=KNeighborsClassifier(n_neighbors=n_neighbors)

# %%
#Model Parameters LGBM
from lightgbm import LGBMClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score
n_split= 3
n_repeat= 15

lgbm = LGBMClassifier(max_depth = 5, num_leaves = 10, early_stopping_rounds=10)
# cv = RepeatedStratifiedKFold(n_splits=n_split, n_repeats=n_repeat)
# n_scores = cross_val_score(lgbm, X, y, scoring='accuracy', cv=cv, n_jobs=-1, error_score='raise')
# fit the model on the whole dataset
# lgbm = LGBMClassifier()



# %%
#Model Parameters MLP
from sklearn.neural_network import MLPClassifier
max_iter=25
# MLP = MLPClassifier(random_state=1, max_iter=max_iter).fit(X_train, y_train)
MLP = MLPClassifier(random_state=42, max_iter=max_iter)


# %%
from sklearn.tree import DecisionTreeClassifier
# Create a Decision Tree Classifier
DT = DecisionTreeClassifier(random_state=42)

from sklearn.ensemble import BaggingClassifier
# # Define the base classifier (Decision Tree in this case)
base_classifier = DT

# Define the BaggingClassifier
bag_DT = BaggingClassifier(base_classifier, n_estimators=10, random_state=42)


from sklearn.linear_model import LogisticRegression
#Logistic Regression
LR = LogisticRegression()
#catboost
import catboost
CAT = catboost.CatBoostClassifier(iterations=100, depth=6, learning_rate=0.1, loss_function='MultiClass', custom_metric='Accuracy')


# import xgboost as xgb
# # Create a DMatrix for XGBoost
# dtrain = xgb.DMatrix(X_train, label=y_train)
# dtest = xgb.DMatrix(X_test, label=y_test)
# # Set XGBoost parameters
# params = {
#     'objective': 'multi:softmax',  # for multi-class classification
#     'num_class': 5,  # specify the number of classes
#     'max_depth': 3,
#     'learning_rate': 0.1,
#     'eval_metric': 'mlogloss'  # metric for multi-class classification
# }

# # Train the XGBoost model
# num_round = 100
# XGB = xgb.train(params, dtrain, num_round)
# # Make predictions on the test set
# preds_xgb = XGB.predict(dtest)
# # preds_xgb_prob = xgb_00.predict_proba(dtest)


# Get class probabilities
# Assuming binary classification, get the probability for the positive class (class 1)
# preds_xgb_margin = XGB.predict(dtest, output_margin=True)
# preds_xgb_prob = 1 / (1 + np.exp(-preds_xgb_margin))

print (y)
# y , yL = pd.factorize(y)



# %%

# %%
from scipy.stats import wilcoxon
from sklearn.datasets import load_iris
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.model_selection import cross_val_score, KFold

# Prepare models and select your CV method
# model1 = ExtraTreesClassifier()
# model2 = RandomForestClassifier()
model1 = svm
model2 = rf
model3 = ada
model4 = dnn_Kmodel
model5 = lgbm
model6 = MLP
model7 = knn_clf
model8 = LR
model9 = DT
model10 = CAT
# model11 = XGB

model12 = bag_DT
# model13 = bag_RF
# model14 = bag_ADA
# model15 = bag_CAT
# model16 = bag_LGBM
# model17 = bag_KNN
# model18 = bag_COMB
# model19 = bag_MLP
# model20 = bag_SVM
# model21 = bag_LR           

name_models = [
                'SVM',
                'RF',
                'DNN',
                'LGBM',
                'MLP',
                'KNN',
                'LR',
                'DT',
                'CAT',
                # 'XGB',
                'bag_DT',
                'ADA'
                # 'bag_RF',
                # 'bag_ADA',
                # 'bag_CAT',
                # 'bag_LGBM',
                # 'bag_KNN',
                # 'bag_COMB',
                # 'bag_MLP',
                # 'bag_SVM',
                # 'bag_LR'            
               ]

actual_models = [
                svm,
                rf,
                dnn_Kmodel,
                lgbm,
                MLP,
                knn_clf,
                LR,
                DT,
                CAT,
                # XGB
                bag_DT,
                ada

]

folds = 10

kf = KFold(n_splits=folds, random_state=None)


# %%
import numpy as np
def crosstrain(model):
    results_model = cross_val_score(model, X, y, cv=kf) 
    return results_model

def wilcox(model1_str,results_model1,model2_str,results_model2):
    # results_model1 = cross_val_score(model_1, X, y, cv=kf) #SVM
    # results_model2 = cross_val_score(model_2, X, y, cv=kf) # RF

    # %%
    # Calculate p value
    #SVM and RF
    with open(output_file_name, "a") as f:print(model1_str +" and " + model2_str,file = f)
    stat, p = wilcoxon(results_model1, results_model2, zero_method='zsplit'); p
    median_model1 = np.median(results_model1)
    median_model2 = np.median(results_model2)
    with open(output_file_name, "a") as f:print("p value: ", p , file = f)
    if p < 0.05:
        if median_model1 > median_model2:
            print(model1_str + " is better.")
            with open(output_file_name, "a") as f:print(model1_str +" is better.", file = f)
        elif median_model1 < median_model2:
            print(model2_str +" is better.")
            with open(output_file_name, "a") as f:print(model2_str +" is better.", file = f)
        else:
            print("Models are statistically different but have the same median.")
            with open(output_file_name, "a") as f:print("Models are statistically different but have the same median.", file = f)
    else:
        print("No statistically significant difference.")
        with open(output_file_name, "a") as f:print("No statistically significant difference.", file = f)
    return None

# %%
# for i in range(0,len(name_models)):
#     for j in range (i,len(name_models)):
#         if i != j:
#             print (name_models [i],' and ',name_models[j])

# %%
# for i in range(0,len(name_models)):
#     for j in range (i,len(name_models)):
#         if i != j:
#             print (name_models [i],' and ',name_models[j])
#             model_name1 = name_models [i]
#             model_name2 = name_models [j]
#             actual_model1 = actual_models [i]
#             actual_model2 = actual_models [j]
#             wilcox(model_name1,actual_model1,model_name2,actual_model2)
results = []
for j in range (0,len(name_models)):
    results.append(crosstrain(actual_models[j]))
    print(name_models[j], "done")

# single_name =  'LGBM'
# single_model = lgbm 
# for j in range (0,len(name_models)):
#     if single_name != name_models[j]:
#         print (single_name,' and ',name_models[j])
#         model_name1 = single_name
#         model_name2 = name_models [j]
#         actual_model1 = single_model
#         actual_model2 = actual_models [j]
#         wilcox(model_name1,actual_model1,model_name2,actual_model2)
    
#xgb as corner case
    

# import xgboost as xgb
# # Create a DMatrix for XGBoost
# dtrain = xgb.DMatrix(X_train, label=y_train)
# dtest = xgb.DMatrix(X_test, label=y_test)
# # Set XGBoost parameters
# params = {
#     'objective': 'multi:softmax',  # for multi-class classification
#     'num_class': 5,  # specify the number of classes
#     'max_depth': 3,
#     'learning_rate': 0.1,
#     'eval_metric': 'mlogloss'  # metric for multi-class classification
# }

# # Train the XGBoost model
# num_round = 100
# XGB = xgb.train(params, dtrain, num_round)
# # Make predictions on the test set
# preds_xgb = XGB.predict(dtest)
    
import xgboost as xgb
from sklearn.model_selection import cross_val_score, KFold

# Define your XGBoost model
model = xgb.XGBClassifier(objective='multi:softmax', max_depth=3, learning_rate=0.1)
# Define your cross-validation strategy
kf = KFold(n_splits=folds, shuffle=True, random_state=42)

# Define the parameters for early stopping
early_stopping_rounds = 10  # Stop if the score doesn't improve for 10 consecutive rounds

# Perform cross-validation with early stopping
result_xgb = cross_val_score(model, X, y, cv=kf, 
                             fit_params={"early_stopping_rounds": early_stopping_rounds, 
                                         "eval_metric": "logloss", 
                                         "eval_set": [(X, y)]})

# Split your data into features (X) and labels (y)
# Replace X and y with your actual data

# Define your cross-validation strategy
# kf = KFold(n_splits=10, shuffle=True, random_state=42)

# Perform cross-validation
# result_xgb = cross_val_score(model, X, y, cv=kf)
name_models.append('XGB')
results.append(result_xgb)
print('XGB done')



print("print results")
for i in range(0,len(name_models)):
    for j in range (i,len(name_models)):
        if i != j:
            print (name_models [i],' and ',name_models[j])
            model_name1 = name_models [i]
            model_name2 = name_models [j]
            actual_model1 = results [i]
            actual_model2 = results [j]
            wilcox(model_name1,actual_model1,model_name2,actual_model2)


for i in range(0,len(name_models)):
    print(name_models[i],results[i])