from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
import joblib


dataframe = pd.read_csv("{yt dataset from the link}")

# remove na rows
data_att = dataframe.dropna(axis=0,how='any')
data_clean = data_att.drop('length' , axis = 1)

train_x, tr_y = data_clean.drop('like',axis=1) , data_att[['like']]
scaler = StandardScaler()
sparse = scaler.fit_transform(train_x)
joblib.dump(scaler, 'scaler_yt.joblib')
train_x_sparse , test_x_sparse , train_y,test_y = train_test_split(sparse,tr_y,test_size = 0.2 , random_state = 42)

# model = RandomForestRegressor(n_estimators = 250,max_depth=20,verbose = True)
model_lr = MLPClassifier(hidden_layer_sizes = (100,50,30,),verbose = True)
           #LinearRegression()
           #MLPClassifier(hidden_layer_sizes = (35,25,10,),verbose = True)
model_lr.fit(train_x_sparse,train_y)
y = model_lr.predict(test_x_sparse)
# pred_y = []
# for item in y:
#     pred_y.append(item[0])
final_dt = {'True Labels':test_y['like'],
            'Predicted labels':y}
final_df = pd.DataFrame(data = final_dt)

print(final_df)

print("Result :",model_lr.score(y, test_y['likes']))

