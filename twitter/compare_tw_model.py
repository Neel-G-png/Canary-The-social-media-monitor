from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
import joblib


t_data = pd.read_csv("tweets_for_mlmodel.csv")

data_att = t_data.dropna(axis = 0,how = 'any')
data_att = data_att.sample(frac=1)
final_data = data_att.drop(['id','tweet','tweeted_at','username'],axis = 1)

train_x, train_y = final_data.drop('retweet_count',axis = 1), final_data[['retweet_count']]

scaler = StandardScaler()
scaled_data = scaler.fit_transform(train_x)

tr_x_sparse,te_x_sparse,tr_y,te_y = train_test_split(scaled_data,train_y,test_size = 0.2,random_state = 42)


model_lr = joblib.load("LR_tw.joblib")
model_rf = joblib.load("RFC_tw.joblib")
model_mlp = joblib.load("MLPC_tw.joblib")
# scaler = joblib.load("scaler.joblib")

pred_y = model_lr.predict(te_x_sparse)
lr_pred = []
for item in pred_y:
    lr_pred.append(item[0])

rf_pred = model_rf.predict(te_x_sparse)
mlp_pred = model_mlp.predict(te_x_sparse)

compared_data = {
    'orignal_value' : te_y['retweet_count'],
    'Linear_Regression' : lr_pred,
    'RandomForest' : rf_pred,
    'MLP' : mlp_pred,
}

compared = pd.DataFrame(data = compared_data)

compared['Linear_Regression'] = compared['Linear_Regression'].apply(np.floor)
compared['RandomForest'] = compared['RandomForest'].apply(np.floor)
compared['MLP'] = compared['MLP'].apply(np.floor)

compared.to_csv("comparing_models.csv",index = False)