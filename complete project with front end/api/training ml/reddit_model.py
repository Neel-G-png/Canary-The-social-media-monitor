import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer 
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge,LinearRegression
from sklearn.metrics import r2_score,accuracy_score
import joblib
import numpy as np
from VADdet import analyze

# path = "files/new_train_test/TrHr_data.csv"
path = "../files/new_train_test/new_Train_data.csv"
# path1 = "../files/new_train_test/calculated_data.csv" 

data = pd.read_csv(path)
calculated = pd.DataFrame(columns=['actual_score','hour_pred'])
# calculated['actual_score'] = []
# calculated['hour_pred'] = []
data_removed = data.drop(['redditor','type','text','proc_text','proc_title','genre','absolute_words_ratio','neg_log_prob_aw_ratio'],axis = 1)

data_removed = data_removed.dropna(subset = ['title','subreddit','datetime','valence','arousal','dominance','hour'])

# train_x ,test_x,train_y,test_y = train_test_split(data_removed.drop('score',axis = 1), data_removed[['score']],test_size = 0.2, random_state = 42)

train_x ,y = data_removed.drop('score',axis = 1), data_removed[['score']]

tfidf_subreddit = TfidfVectorizer(ngram_range=(1, 1), max_features=None)
subreddit_sparse = tfidf_subreddit.fit_transform(train_x['subreddit'])


#changing ngram range 
tfidf_title = TfidfVectorizer(ngram_range=(2, 5), max_features=None)
title_sparse = tfidf_title.fit_transform(train_x['title'])

hour = train_x[['hour']]
valence = train_x[['valence']]
arousal = train_x[['arousal']]
dominance = train_x[['dominance']]

# print("\nTRAIN X : \n",train_x.columns)
# exit()

# stacked_val = hstack([train_x['datetime'],train_x['valence'],train_x['arousal'],train_x['dominance']])
# stacked_val = train_x.drop(['title','subreddit'],axis = 1) 
scaler = StandardScaler()
scaled_date = scaler.fit_transform(hour)
scaled_val = np.hstack([scaled_date,valence,arousal,dominance])
'''
# print("\nDATE SCALED !!\n",scaled_val[28])
train_x_sparse = hstack([title_sparse,subreddit_sparse,scaled_val])
# train_x_sparse , test_x_sparse , train_y,test_y = train_test_split(sparse_data,y,test_size = 0.2 , random_state = 42)
print("\t ############ TRAINING MODEL ############")
# train_y = train_y.astype('int')

ml_model = MLPClassifier(max_iter=45,hidden_layer_sizes = (35,),verbose = True) 
           #Ridge(alpha = 0.0001)
           #MLPClassifier(max_iter=30,hidden_layer_sizes = (25,5,),verbose = True)
           #LinearRegression()
ml_model.fit(train_x_sparse,y.values.ravel())
joblib.dump(ml_model, 'mlp_hour.joblib')

print(ml_model.score(train_x_sparse, y)) 

print("\t ############ TRAINING COMPLETE ############")
# joblib.dump(tfidf_subreddit,"tfidf_subreddit_hour.joblib")
# joblib.dump(tfidf_subreddit,"tfidf_title_hour.joblib")
# joblib.dump(scaler,"scaler_hour.joblib")
# ml_model = joblib.load("savedmodels/lin_joblib_model.joblib")

ml_model = joblib.load("mlp_hour.joblib")


test_data = pd.read_csv("../files/new_train_test/finaltest_data.csv")

test_data_removed = test_data.drop(['redditor','type','text','proc_text','proc_title','genre','absolute_words_ratio','neg_log_prob_aw_ratio'],axis = 1)

test_data_removed = test_data_removed.dropna(subset = ['title','subreddit','datetime','valence','arousal','dominance','hour'])

test_x, test_y = test_data_removed.drop('score',axis = 1), test_data_removed[['score']]

sub_sparse = tfidf_subreddit.transform(test_x['subreddit'])
tit_sparse = tfidf_title.transform(test_x['title'])

# test_stacked_val = test_x.drop(['title','subreddit'],axis = 1)
test_date_time = test_x[['hour']]
test_valence = test_x[['valence']]
test_arousal = test_x[['arousal']]
test_dominance = test_x[['dominance']]
test_date = scaler.transform(test_date_time)
# print(test_date)
test_scaled_val = np.hstack([test_date,test_valence,test_arousal,test_dominance])

test_x_sparse = hstack([tit_sparse, sub_sparse, test_scaled_val])

pred_y = ml_model.predict(test_x_sparse)
print(pred_y)

score = ml_model.score(test_y,pred_y)
print(score)
print(pred_y)
calculated['actual_score'] = test_y['score']
calculated['hour_pred'] = pred_y
calculated.to_csv("../files/new_train_test/calculated_data.csv",index = False)
print("\nDONE SAVING")

# ml_model = joblib.load("savedmodels/mlp_pickle_model12.joblib")

# pred_y1 = ml_model.predict(test_x_sparse)
pred_hour_y = ml_hour_model.predict(sparse_data)

calculated['actual_Data'] = y[['score']]
calculated['pred_hour'] = pred_hour_y
# calculated['actual_Data'] = y[['score']]
print("\nPRED", pred_hour_y)

# calculated.to_csv('files/new_train_test/calculated_data.csv',index = False)
'''

ml_model = joblib.load("mlp_hour.joblib")
hour_clock = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
time = 5
subredddit = ["politics"]
title = "treated us like animals holding pen migrant families el paso shut"
mode = "mean"
V = A = D = 0
V,A,D = analyze(title,mode)
V/=10
A/=10
D/=10

sub_sparse = tfidf_subreddit.transform(subredddit)
tit_sparse = tfidf_title.transform([title])
time_sparse = scaler.transform([[time]])
vad_sparse = np.hstack([time_sparse,[[V]],[[A]],[[D]]])
pred_sparse = hstack([tit_sparse,sub_sparse,vad_sparse])
result = ml_model.predict(pred_sparse)
result = ml_model.predict(pred_sparse)

print(result)
for hour in hour_clock:
    if hour != time:
        time_sparse = scaler.transform([[hour]])
        vad_sparse = np.hstack([time_sparse,[[V]],[[A]],[[D]]])
        pred_sparse = hstack([tit_sparse,sub_sparse,vad_sparse])
        test_res = ml_model.predict(pred_sparse)
        # if test_res>result:
        print(f"\nYOU WOULD GET {test_res} UPVOTES IF YOU POSTED AT {hour}")