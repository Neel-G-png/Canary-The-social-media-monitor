''' flask imports '''
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from werkzeug.security import safe_str_cmp
from flask_jwt import JWT, jwt_required, current_identity
from flask import Flask, render_template, request, jsonify

''' mysql imports '''
import mysql.connector

''' machine learning '''
import math 
import joblib
import numpy as np
import pandas as pd
import text2emotion as te
from VADdet import analyze
from scipy.sparse import hstack
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from multiprocessing import Process, Value

''' miscelenous imports '''
import re
import praw
import time
import datetime
from threading import Thread
from wordcloud import WordCloud, STOPWORDS



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
CORS(app, support_credentials=True)


# socketIo = SocketIO(app, cors_allowed_origins="*")
app.debug = False

app.host='localhost'
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "####",
    database = "neel",
)

reddit = praw.Reddit(client_id = '####',
                     client_secret = '####',
                     user_agent = '####',
                     username = '####',
                     password = '####')

# @socketIo.on("getTime")
# def getTime():
#     for i in range(0,5):
#         print("TIMEEEEE @@@",i)
#         time.sleep(3)
#         emit("getTime", i, broadcast=True)
#     return None

class machine_learning():
    path = "files/new_Train_data.csv"
    data = pd.read_csv(path)
    red_model = joblib.load("models/mlp_hour.joblib")
    list_red = []
    high_low_line = []
    senti_line = []
    senti_pie = {'Angry':0,'Fear':0,'Happy':0,'Sad':0,'Surprise':0}
    username = ""
    
    yt_model = joblib.load("models/new_RFC_yt.joblib")
    yt_scaler = joblib.load("models/scaler_yt.joblib")

    tw_model = joblib.load("models/RFC_tw.joblib")
    tw_scaler = joblib.load("models/scaler_tw.joblib")

    def __init__(self):
        data_removed = self.data.drop(['redditor','type','text','proc_text','proc_title','genre','absolute_words_ratio','neg_log_prob_aw_ratio'],axis = 1)
        data_removed = data_removed.dropna(subset = ['title','subreddit','datetime','valence','arousal','dominance','hour'])
        train_x ,y = data_removed.drop('score',axis = 1), data_removed[['score']]
        self.tfidf_subreddit = TfidfVectorizer(ngram_range=(1, 1), max_features=None)
        subreddit_sparse = self.tfidf_subreddit.fit_transform(train_x['subreddit'])
        #changing ngram range 
        self.tfidf_title = TfidfVectorizer(ngram_range=(2, 5), max_features=None)
        title_sparse = self.tfidf_title.fit_transform(train_x['title'])
        hour = train_x[['hour']]
        valence = train_x[['valence']]
        arousal = train_x[['arousal']]
        dominance = train_x[['dominance']]
        self.scaler_rd = StandardScaler()
        scaled_date = self.scaler_rd.fit_transform(hour)
        list_red = []
        high_low_line = []

    def calc_highlow_red(self,username):
        cursor_for_model = mydb.cursor()
        cursor_for_model.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
        sql = "select sub_id,sub_title,sub_date,site,sub_url from reddit_data where u_id like %s"
        user_id = "%,"+str(username)+",%"
        val = (user_id,)

        cursor_for_model.execute(sql,val)
        red_data = cursor_for_model.fetchall()
        
        for row in red_data:
            red_dic = {}
            mode = "mean"
            subreddit = str(row[3])
            time = row[2].hour
            title = str(row[1])
            V,A,D = analyze(title,mode)
            # V = 5.06
            # A = 4.21
            # D = 5.18
            V/=10
            A/=10
            D/=10
            sub_sparse = self.tfidf_subreddit.transform([subreddit])
            tit_sparse = self.tfidf_title.transform([title])
            time_sparse = self.scaler_rd.transform([[time]])
            vad_sparse = np.hstack([time_sparse,[[V]],[[A]],[[D]]])
            pred_sparse = hstack([tit_sparse,sub_sparse,vad_sparse])
            result = self.red_model.predict(pred_sparse)
            # emotion : 
            # print(f"RESULT :{math.floor(result[0])}")
            red_dic['title'] = title
            red_dic['outreach'] = math.floor(result[0])
            date = str(row[2]).split(' ')
            red_dic['link'] = row[4]
            red_dic['site'] = "Reddit"
            red_dic['date'] = date[0]
            # print(row[5].date())
            # exit()
            self.list_red.append(red_dic)
        # print("\nLIST OF RESULTS : ",self.list_red)
        cursor_for_model.close()
        # print(red_data)

    def calc_highlow_yt(self,username):
        cur_for_yt = mydb.cursor()
        cur_for_yt.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
        sql = "select sub_count,categoryId,hours,minutes,seconds,vid_id,comment,pub_time from yt_data where co_uid like %s limit 1,15"
        user_id = "%,"+str(username)+",%"
        # user_id = ",neelg"
        val = (user_id,)
        cur_for_yt.execute(sql,val)
        yt_data = cur_for_yt.fetchall()
        i = 0
        for row in yt_data:
            yt_dic = {}
            feed = [row[0],row[1],row[2],row[3],row[4]]
            scaled_val = self.yt_scaler.transform([feed])
            views = self.yt_model.predict(scaled_val)
            yt_dic['title'] = row[6]
            yt_dic['outreach'] = math.floor(views[0])
            yt_dic['link'] = "https://www.youtube.com/watch?v="+str(row[5])
            yt_dic['site'] = "Youtube"

            date = row[7].split('T')
            
            yt_dic['date'] = date[0]
            # print(row[7].date())
            self.list_red.append(yt_dic)
            i+=1
            print(f"from yt : {i}",end = "\r")
            # break
        cur_for_yt.close()
        # print("\nLIST OF RESULTS : ",self.list_red)
        # return self.list_red

    def calc_highlow_tw(self,username):
        cur_for_tw = mydb.cursor()
        cur_for_tw.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
        sql = "select follower_count,friend_count,listed_count,verification_status,tweet,link,tweeted_at from twitter_data where tweet_for_user like %s"
        user_id = "%,"+str(username)+",%"
        # user_id = ",neelg"
        val = (user_id,)
        cur_for_tw.execute(sql,val)
        tw_data = cur_for_tw.fetchall()
        for row in tw_data:
            tw_dic = {}
            feed = [row[0],row[1],row[2],row[3]]
            scaled_val = self.tw_scaler.transform([feed])
            pred_retweet = self.tw_model.predict(scaled_val)
            tw_dic['title'] = row[4]
            tw_dic['link'] = row[5]
            tw_dic['outreach'] = math.floor(pred_retweet[0])
            tw_dic['site'] = "Twitter"

            date = str(row[6]).split(" ")

            tw_dic['date'] = date[0]
            self.list_red.append(tw_dic)
        cur_for_tw.close()
        # return self.list_red
    
    def add_senti(self):
        # i= 0
        # print(len(self.list_red))
        # return self.list_red
        for item in self.list_red:
            title = item['title']
            sentiment = te.get_emotion(title)
            item['sentiment'] = sentiment
            # i+=1
            print(f"from senti :",end = "\r")
        return self.list_red

    def high_low_date(self):
        list_date = []
        orignal_list = self.list_red.copy()
        for item in self.list_red:
            list_date.append(item['date'])
        unique_dates = set(list_date)
        print("UNI DATES : ", unique_dates)
        for date in unique_dates:
            high = 0
            low = 0
            highlow = {}
            for item in orignal_list:
                if item['date'] == date:
                    if item['site'] == "Reddit" and item['outreach'] > 75:
                        high+=1
                    elif item['site'] == "Youtube" and item['outreach'] > 500:
                        high+=1
                    elif item['site'] == "Twitter" and item['outreach'] > 50:
                        high+=1
                    else:
                        low+=1
            highlow['date'] = date
            highlow['high'] = high
            highlow['low'] = low
            self.high_low_line.append(highlow)
        return self.high_low_line

    def total_senti(self):
        list_date = []
        orignal_list = self.list_red.copy()
        for item in self.list_red:
            list_date.append(item['date'])
        unique_dates = set(list_date)
        print("UNI DATES : ", unique_dates)
        for date in unique_dates:
            positive = 0
            negative = 0
            neutral = 0
            sent = {}
            for item in orignal_list:
                if item['date'] == date:
                    neg = item['sentiment']['Angry'] + item['sentiment']['Fear'] + item['sentiment']['Sad']
                    pos = item['sentiment']['Happy'] + item['sentiment']['Surprise']
                    if pos > neg:
                        positive+=1
                    elif pos<neg:
                        negative+=1
                    else:
                        neutral+=1
            sent['date'] = date
            sent['positive'] = positive
            sent['negative'] = negative
            sent['neutral'] = neutral
            self.senti_line.append(sent)
        return self.senti_line
    
    def sentiment_pie(self):
        # total = {'Angry':0,'Fear':0,'Happy':0,'Sad':0,'Surprise':0}
        returning_data = []
        correl = {0:'Angry',1:'Fear',2:'Happy',3:'Sad',4:'Surprise'}
        for item in self.list_red:
            array = [item['sentiment']['Angry'],item['sentiment']['Fear'],item['sentiment']['Happy'],item['sentiment']['Sad'],item['sentiment']['Surprise']]
            if max(array) != 0:
                ind = array.index(max(array))
                self.senti_pie[correl[ind]]+=1
        for item in self.senti_pie.keys():
            rd = {}
            rd['name'] = item
            rd['value'] = self.senti_pie[item]
            returning_data.append(rd)
        return returning_data

    def total_mentions(self):
        for item in self.high_low_line:
            total = {}
            # combined = 0
            total['name'] = item['date']
            total['total'] = item['high'] + item['low']
            # total[item['date']] = item['high'] + item['low']
            self.total_mention_line.append(total)
        return self.total_mention_line

    def wordcloud_gen(self):
        comment_words = []
        stopwords = set(STOPWORDS)
        wordcloud = {}
        without_sw = []
        for item in self.list_red:
            text = re.sub(r"[^A-Za-z0-9_, ]+", "",item['title'])
            tokens = text.split()
            for i in range(len(tokens)):
                if tokens[i].lower() not in stopwords:
                    without_sw.append(tokens[i].lower())
        
        for word in without_sw:
            if word not in wordcloud:
                wordcloud[word] = 0 
            wordcloud[word] += 1
        for item in wordcloud:
            individual = {}
            if wordcloud[item]>1:
                individual['text'] = item
                individual['value'] = wordcloud[item]
                comment_words.append(individual)
        
        return comment_words

ml_obj = machine_learning()

class data_collection():
    product_keys = {}
    thread_quit = False
    keys = []
    reddit_data_dict = {
    'sub_id': "",
    'sub_title': "",
    'sub_body': "",
    'sub_date': datetime.datetime.now(),
    'sub_url': "",
    }

    def get_keys(self):
        print("\n\t ############ STARTING GET KEYS ############")
        keywords = ""
        cursor1= mydb.cursor()
        cursor1.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
        cursor1.execute("select username,keywords from user_data")# where user_id = '%s'",val)
        users_keywords = cursor1.fetchall()
        for row in users_keywords:
            self.product_keys[row[0]] = row[1]
            keywords = keywords + ", "+str(row[1])
        keywords = str(keywords)
        print(self.product_keys)
        keywords = re.sub(r'[^A-Za-z0-9_, ]+','',keywords)
        self.keys = keywords.split(',')
        self.keys = list(dict.fromkeys(self.keys))
        if '' in self.keys:
            self.keys.remove('')
        for i,key in enumerate(self.keys):
            self.keys[i] = key.strip()
        # print(self.keys)
        cursor1.close()
        print("\n\t ############ ENDING GET KEYS ############")

    def get_redditt_data(self):
        print("\n\t ############ STARTING REDDIT ############")
        subreddit = reddit.subreddit('all')
        self.get_keys()    ##############################################################changed
        # product_keys = get_keys()
        # print(product_keys)
        search_for = [x.upper() for x in self.keys]

        for submission in subreddit.stream.submissions():
            cursor = mydb.cursor()
            
            # i+=1
            # global product_keys
            # global keys
            search_for = [x.upper() for x in self.keys]
            title = submission.title.upper()
            sub_text = submission.selftext.upper()
            full_text = title+sub_text
            
            # if find in full_text:#title or find in sub_text:
            present = [key for key in search_for if(key in full_text)]
            # print("TEST")
            if len(present)>0:
                
                post_users = ""
                print(present)
                for p in present:
                    for user in self.product_keys:
                        if p in self.product_keys[user].upper():
                            post_users = post_users+"," + str(user)
                # i+=1
                self.reddit_data_dict['sub_id'] = str(submission.name)
                self.reddit_data_dict['sub_title'] = str(submission.title)
                self.reddit_data_dict['sub_body'] = str(submission.selftext)
                self.reddit_data_dict['sub_date'] = datetime.datetime.fromtimestamp(submission.created)
                self.reddit_data_dict['sub_url'] = f"https://www.reddit.com/{submission.permalink}"
                reddit_data = clean(self.reddit_data_dict)
                # print("\t TITLE !!!! = ",reddit_data['sub_title']) 
                sub = submission.subreddit
                print("\tr/",sub.display_name)          
                print("\t url !!!! = ",reddit_data['sub_url'])
                # post_users = str.lstrip(',')
                print("\t users !!!! = ",post_users[1:])
                post_users = post_users + ","
                print("\n PRODUCT KEYS : ",self.product_keys)
                sql = "insert into reddit_data (sub_id,sub_title,sub_body,sub_date,sub_url,u_id,site)\
                    select * from (Select %s,%s,%s,%s,%s,%s,%s) as temp\
                    where not exists (Select sub_id from reddit_data where sub_id = %s) LIMIT 1"
                site = sub.display_name
                val = (reddit_data['sub_id'],reddit_data['sub_title'],reddit_data['sub_body'],reddit_data['sub_date'],reddit_data['sub_url'],post_users,site,reddit_data['sub_id'])
                cursor.execute(sql,val)
                mydb.commit()
            # global thread_quit
            if self.thread_quit == True:
                break
            cursor.close()
            # exit()
    
    def get_comments(self):
        pass

obj = data_collection()

def clean(reddit_data):
    if len(reddit_data['sub_title'])>255:
        reddit_data['sub_title'] = reddit_data['sub_title'][:255]
        reddit_data['sub_title'] = re.sub(r'[^A-Za-z0-9_ ]+','',reddit_data['sub_title'])
    if len(reddit_data['sub_body'])>300:
        reddit_data['sub_body'] = reddit_data['sub_body'][:300]
    return reddit_data

''' Total Buzz '''
@app.route("/buzz", methods=['GET'])
def total_buzz():
    print("######## BUZZ ########")
    cursor_for_user= mydb.cursor()
    user_id = request.args.get('user')
    # user_id = "User(id='2')"
    print("USER ID ERROR : ",user_id)
    main_id = user_id[:-1].split("=")[1]
    main_id = int(main_id.strip("'"))
    # main_id = 13
    sql = "select username from user_data where user_id = %s"
    val = (main_id,)
    cursor_for_user.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
    cursor_for_user.execute(sql,val)
    all_users = cursor_for_user.fetchall()
    print("TYPE MAIN ID : ",type(main_id),"\t MAIN ID : ",main_id)
    # print("user ID :", all_users)
    username = all_users[0][0]
    ml_obj.list_red = []
    ml_obj.calc_highlow_red(username)
    ml_obj.calc_highlow_yt(username)
    ml_obj.calc_highlow_tw(username)
    result = ml_obj.add_senti()
    new_result = sorted(result, key = lambda i: i['outreach'],reverse=True)
    dict = {'items':new_result}
    return jsonify(dict)

''' Total Outreach '''
@app.route("/outreach", methods=['GET'])
def high_low():
    print("######## outreach ########")
    ml_obj.high_low_line = []
    highlow = ml_obj.high_low_date()
    new_result = sorted(highlow, key = lambda i: i['date'])
    dict = {'highlow':new_result}
    return jsonify(dict)

''' Total Sentiment '''
@app.route("/sentiment", methods=['GET'])
def sentiment_analysis():
    print("######## sentiment ########")
    ml_obj.senti_line = []
    ml_obj.senti_pie = {'Angry':0,'Fear':0,'Happy':0,'Sad':0,'Surprise':0}
    result = ml_obj.total_senti()
    pie = ml_obj.sentiment_pie()
    new_result = sorted(result, key = lambda i: i['date'])
    dict = {'line':new_result,'pie':pie}
    return jsonify(dict)

''' total mentions '''
@app.route("/totalMentions", methods=['GET'])
def totmentions():
    print("######## total mentions ########")
    ml_obj.total_mention_line = []
    total = ml_obj.total_mentions()
    new_result = sorted(total, key = lambda i: i['name'])
    dict = {'total_mentions':new_result}
    return jsonify(dict)

''' wordcloud '''
@app.route("/wordcloud", methods=['GET'])
def wordc():
    print("######## Wordcloud ########")
    result = ml_obj.wordcloud_gen()
    dict = {'wordcloud':result}
    return jsonify(dict)

@app.route('/api', methods=['GET'])
def api():
    return{
        'userId':1,
        'tile': 'flask react app',
        'completed':False
    }

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = []
username_table = {}
userid_table = {}
def collect_users():
    print("################FROM COLLECT USER ################")
    users.clear()
    print()
    global username_table
    global userid_table
    userid_table.clear()
    username_table.clear()
    cursor_for_ident= mydb.cursor()
    cursor_for_ident.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
    cursor_for_ident.execute("select user_id,username,password from user_data")
    all_users = cursor_for_ident.fetchall()
    for row in all_users:
        users.append(User(row[0],row[1],row[2]))
    cursor_for_ident.close()
    username_table = {u.username: u for u in users}
    userid_table = {u.id: u for u in users}
    print("USER TABLE", username_table)
    print(users)

# username_table = {u.username: u for u in users}
# userid_table = {u.id: u for u in users}



def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        print("user",user)
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

@app.route('/', methods=['GET','POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def index():
    return 'OK'

jwt = JWT(app, authenticate, identity)

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

@app.route('/signup', methods=['POST'])
def signup():
    cursor_singup= mydb.cursor()
    form = request.json
    username = form['username']
    password = form['password']
    keywords = form['keywords']
    sql = "insert into user_data(username,password,keywords) values(%s,%s,%s)"
    values = (username,password,keywords)
    cursor_singup.execute(sql,values)
    mydb.commit()
    cursor_singup.close()
    collect_users()
    obj.get_keys()
    return 'OK'


# @app.route('/outreach', methods=['GET'])
# def outreach():
#     user_id = request.args.get('user')
#     print("user ID :", user_id)
#     return 'OK'

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  response.headers.add('Access-Control-Allow-Headers','Origin, X-Requested-With, Content-Type, Accept, Authorization, userid')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
    # collect_users()
    # obj.get_keys()
    # T_reddit_data = Thread(target = obj.get_redditt_data)
    # try:
    #     T_reddit_data.start()
    #     app.run()
    #     # while True: time.sleep(100)
    # except(KeyboardInterrupt, SystemExit):
    #     print("\n\t------- KEYBOARD INTERRUPT SUCCESSFUL -------")
    #     obj.thread_quit = True
    #     T_reddit_data.join()
    #     exit()
    
    collect_users()
    # obj.get_keys()
    p_reddit = Process(target=obj.get_redditt_data)
    # p_keys = Process(target = obj.get_keys)
    # p_users = Process(target = collect_users)
    
    p_reddit.start()
    # p_keys.start()
    # p_users.start()
    app.run()
    p_reddit.join()
    # p_keys.join()
    # p_users.join