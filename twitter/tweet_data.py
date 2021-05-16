import tweepy
import sys
import json

consumer_key="####################"
consumer_secret="####################"
access_token="####################"
access_token_secret="####################"


auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

if (not api):
    print("Authentication failed!")
    sys.exit(-1)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self,status):
        if status.lang == 'en':
            link = "https://twitter.com/twitter/statuses/"+status.id_str
            print("\n TWEET : ",status.text)
            print("USERNAME : ",status.user.screen_name)
            print("LINK : ",link)
            savefile = open('td.csv','w',encoding = 'utf-8')
            savefile.write(status.text) 
    
    # def on_data(self,data):
    #     dict_data = json.loads(data)
    #     print("\n TWEET : ",dict_data['text'] )#status.text)
    #     savefile = open('td.csv','a',encoding = 'utf-8')
    #     savefile.write(dict_data['text']) 
    def on_error(self,status_code):
        print(status_code)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=["neel","dell","valorant"])