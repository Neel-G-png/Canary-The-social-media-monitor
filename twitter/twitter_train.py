from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
import joblib

t_data = pd.read_csv("dataset_generated/tweets_for_mlmodel.csv")

data_att = t_data.dropna(axis = 0,how = 'any')
data_att = data_att.sample(frac=1)
final_data = data_att.drop(['id','tweet','tweeted_at','username'],axis = 1)

train_x, train_y = final_data.drop('retweet_count',axis = 1), final_data[['retweet_count']]

scaler = StandardScaler()
scaled_data = scaler.fit_transform(train_x)

tr_x_sparse,te_x_sparse,tr_y,te_y = train_test_split(scaled_data,train_y,test_size = 0.2,random_state = 42)
model = LinearRegression()
        #MLPClassifier(hidden_layer_sizes = (100,50,30,),verbose = True)
        #LinearRegression()
        #RandomForestRegressor(n_estimators = 250,max_depth=20,verbose = True)
model.fit(tr_x_sparse,tr_y)

joblib.dump(model, 'LR_tw.joblib')

pred_y = model.predict(te_x_sparse)

predicted = []
for item in pred_y:
    predicted.append(item[0])

final_dt = {'True Labels':te_y['retweet_count'],
            'Predicted labels':predicted}
final_df = pd.DataFrame(data = final_dt)

print(final_df)