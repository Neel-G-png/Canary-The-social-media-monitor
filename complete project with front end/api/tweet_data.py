import tweepy
import sys
import json
import re
import time
import pandas as pd
import datetime
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "####",
    database = "neel",
)

consumer_key="####
consumer_secret="####"
access_token="####"
access_token_secret="####"


auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

if (not api):
    print("Authentication failed!")
    sys.exit(-1)

class MyStreamListener(tweepy.StreamListener):

    product_keys = {}
    keywords = ""
    keys = []

    id = ""
    link = ""
    tweet = ""
    user_name = ""
    user_follower_count = 0
    friend_count = 0
    listed_count = 0
    verification_status = False
    tweeted_at = datetime.datetime.now()

    date_since = "2021-01-01"
    i = 0
    tweet_text = []
    username = []
    followers_count = []
    fri_count = []
    lis_count = []
    verified = []
    retweet_count = []
    created_at = []
    id_list = []

    def get_keys(self):
        cursor1= mydb.cursor()
        cursor1.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
        cursor1.execute("select username,keywords from user_data")# where user_id = '%s'",val)
        users_keywords = cursor1.fetchall()
        for row in users_keywords:
            self.product_keys[row[0]] = row[1]
            self.keywords = self.keywords + ","+str(row[1])

        # keywords = ['neel','earbuds','dell 7559']
        print(self.product_keys)
        self.keywords = str(self.keywords)
        self.keywords = re.sub(r'[^A-Za-z0-9_, ]+','',self.keywords)
        self.keys = self.keywords.split(',')
        self.keys = list(dict.fromkeys(self.keys))
        if '' in self.keys:
            self.keys.remove('')
        for i,key in enumerate(self.keys):
            self.keys[i] = key.strip().upper()
        # self.keys = ['APPLE IPHONE']
        print(self.keys)

    def on_status(self,status):
        cursor_insert = mydb.cursor()
        if status.lang == 'en':
            tweet_for = ""
            present = []
            print("\n\n############################################")
            # print(status.extended_tweet)
            # exit()
            for present_key in self.keys: 
                # print(x)
                if len(present_key.split(" "))>1:
                    sub_p = present_key.split(" ")
                    print("sub_p : ",sub_p)
                    for p in sub_p:
                        if p in status.text.upper():
                            print("this word : ",p)
                            present.append(present_key)

                if present_key in status.text.upper():
                    present.append(present_key)
            print("text : ",status.text)
            present = set(present)
            print("PRESENT :", present)
            if present:
                for p in present:
                    for user in self.product_keys:
                        if p in self.product_keys[user].upper():
                            tweet_for = tweet_for + "," + str(user)
                tweet_for = tweet_for+","
                print("TWEET FOR : ",tweet_for)
                self.id = status.id_str
                self.link = "https://twitter.com/twitter/statuses/"+status.id_str
                self.tweet = status.text
                self.user_name = status.user.screen_name
                self.user_follower_count = status.user.followers_count
                self.friend_count = status.user.friends_count
                self.listed_count = status.user.listed_count
                self.created_at = status.created_at
                if status.user.verified:
                    self.verification_status = 1
                else:
                    self.verification_status = 0    
                # self.verification_status = status.user.verif)ied
                sql = "insert into twitter_data (id,link,tweet,username,follower_count,friend_count,listed_count,verification_status,tweet_for_user,tweeted_at)\
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (self.id,self.link,self.tweet[:500],self.user_name,self.user_follower_count,self.friend_count,self.listed_count,self.verification_status,tweet_for,self.created_at)
                cursor_insert.execute(sql,val)
                mydb.commit()
        cursor_insert.close()

    def on_error(self,status_code):
        print(status_code)

    def collect_data_for_model(self):
        tweets = tweepy.Cursor(api.search,
                               lang = "en",
                               q = ""+'-filter:retweets',
                               until = "2021-05-29",
                            #    result_type = "popular",
                               count = 100).items()
        
        for tweet in tweets:
            # if  tweet.retweet_count>=70 and tweet.retweet_count<=400:
            
            try :
                if tweet.user.followers_count < 50 and tweet.retweet_count>0:
                    self.tweet_text.append(tweet.text)
                    self.username.append(tweet.user.screen_name)
                    self.followers_count.append(tweet.user.followers_count)
                    self.fri_count.append(tweet.user.friends_count)
                    self.lis_count.append(tweet.user.listed_count)
                    if tweet.user.verified:
                        self.verified.append(1)
                    else:
                        self.verified.append(0)
                    self.retweet_count.append(tweet.retweet_count)
                    self.created_at.append(tweet.created_at)
                    self.id_list.append(tweet.id_str)
                    
                    
                    # print("\n NEW : ",tweet.text)
                    # print(" TIME : ",tweet.created_at)
                    # print(" UNAME : ",tweet.user.screen_name)
                    # print(" FOLCOUNT : ",tweet.user.followers_count)
                    # print(" FRICOUNT : ",tweet.user.friends_count)
                    # print(" LISCOUNT : ",tweet.user.listed_count)
                    # print(" VERIFIED? : ",tweet.user.verified)
                    # print(" RETCOUNT : ",tweet.retweet_count)
                    print("I = ",self.i,end = "\r")
                    self.i+=1
                    if self.i>300:
                        break
            except:
                return
    
    def store_csv(self):
        output_dict = {
            'id':self.id_list,
            'tweet': self.tweet_text,
            'tweeted_at':self.created_at,
            'username': self.username,
            'followers_count': self.followers_count,
            'friends_count': self.fri_count,
            'listed_count': self.lis_count,
            'verified': self.verified,
            'retweet_count':self.retweet_count,
        }
        out_df = pd.DataFrame(output_dict,columns = output_dict.keys())
        out_df.to_csv("tweets_for_mlmodel_mix.csv",index = False)
        print("########### SAVED IN FILE ###########")

myStreamListener = MyStreamListener()
myStreamListener.get_keys()

''' comment after collecting data '''
# myStreamListener.collect_data_for_model()
# myStreamListener.store_csv()

''' uncomment to stream data for project '''
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener,tweet_mode = 'extended')
myStream.filter(track=myStreamListener.keys)
