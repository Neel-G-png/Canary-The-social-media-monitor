from googleapiclient.discovery import build
import pandas as pd
from youtubesearchpython import *
import time
import re
import mysql.connector

################## setting up  youtube service ##################
API_KEY = "##################################"
youtube = build('youtube','v3',developerKey = API_KEY)


################## local mysql connection ##################
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "##################################",
    database = "neel",
)

class get_yt_data:
    product_keys = {}
    keywords = ""
    keys = []
    present_idlist = {}
    new_idlist = {}
    title_list = []

    com_ids = []
    v_id = []
    com_text = []
    likes = []
    v_title = []
    pub_time = []

    no_result = False
    nextPage_token = None
    com_counter = 0


    ################## get keywords to search on youtube from local database table ##################
    def get_keys(self):
        cursor1= mydb.cursor()
        cursor1.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
        cursor1.execute("select * from product_keys")# where user_id = '%s'",val)
        users_keywords = cursor1.fetchall()
        for row in users_keywords:
            self.product_keys[row[0]] = row[1]
            self.keywords = self.keywords + ", "+str(row[1])

        # keywords = ['neel','earbuds','dell 7559']

        self.keywords = str(self.keywords)
        self.keywords = re.sub(r'[^A-Za-z0-9_, ]+','',self.keywords)
        self.keys = self.keywords.split(',')
        self.keys = list(dict.fromkeys(self.keys))
        if '' in self.keys:
            self.keys.remove('')
        for i,self.key in enumerate(self.keys):
            self.keys[i] = self.key.strip()


    def get_video_data(self):
        print("IN VID DATA")
        cursor = mydb.cursor()
        sql = "select distinct vid_id,vid_title from yt_data;"
        cursor.execute(sql)
        vid_id_present = cursor.fetchall()
        # print(vid_id_present)

        ################## for adding only new videos in table  ##################
        for row in vid_id_present:
            print(row[0])
            self.present_idlist[row[0]] = row[1]
            self.new_idlist[row[0]] = row[1]
        # keys = ["apple airtags,gpro"]
        print("\nID list before : ",self.present_idlist.keys())
        
        ################## iterating over every key and fingding the top 5 video title and ID ##################
        for key in self.keys:
            VSearch = VideosSearch(key)
            result = VSearch.result()
            print(key)
            count = 0
            i= 0

            while(count<5):
                
                try:
                    if result['result'][i]['id'] not in self.present_idlist.keys():
                        self.new_idlist[result['result'][i]['id']] = result['result'][i]['title']   # dict for easy saving
                    
                    i+=1
                    count+=1
                except:
                    ################## try catch block to access results of "next page" ##################
                    if len(result['result']) == 0 and i == 0:
                        self.no_result = True
                        break
                    VSearch.next()
                    result = VSearch.result()
                    i=0
        print("\nID list after : ",self.new_idlist.keys())
    def get_com_data(self):
        print("from comment data")
        ################## getting all the top comments of the respective videos ##################
        cursor1 = mydb.cursor()
        for i,v in enumerate(self.new_idlist.keys()):
            ################## check if video already exists in the database if yes only add comments that are newer than the last time you ran this code ##################
            if v in self.present_idlist.keys():
                sql = "select max(pub_time) from yt_data where vid_id = %s"
                # val = (v,)
                cursor1.execute(sql,(v,))
                max_time = cursor1.fetchall()
                print("MAX time = ",max_time[0][0])
            while True:
                try:
                    com_thread = youtube.commentThreads().list(
                        part = 'snippet',
                        videoId = v,
                        maxResults = 100,
                        order = 'relevance',
                        textFormat = 'plainText',
                        pageToken = self.nextPage_token,).execute()
                    self.nextPage_token = com_thread.get('nextPageToken')

                    for item in com_thread['items']:
        ################## check if video already exists in the database if yes only add comments that are newer than the last time you ran this code ##################
                        if v in self.present_idlist.keys() and item['snippet']['topLevelComment']['snippet']['publishedAt']>max_time[0][0]:
                            self.v_id.append(v)
                            self.v_title.append(self.new_idlist[v])
                            self.com_text.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                            self.com_ids.append(item['snippet']['topLevelComment']['id'])
                            self.likes.append(item['snippet']['topLevelComment']['snippet']['likeCount'])
                            self.pub_time.append(item['snippet']['topLevelComment']['snippet']['publishedAt'])
                            self.com_counter+=1
                            print("Comments downloaded:", self.com_counter, end="\r")
                        elif v not in self.present_idlist.keys():
                            self.v_id.append(v)
                            self.v_title.append(self.new_idlist[v])
                            self.com_text.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                            self.com_ids.append(item['snippet']['topLevelComment']['id'])
                            self.likes.append(item['snippet']['topLevelComment']['snippet']['likeCount'])
                            self.pub_time.append(item['snippet']['topLevelComment']['snippet']['publishedAt'])
                            self.com_counter+=1
                            print("Comments downloaded:", self.com_counter, end="\r")
                except KeyboardInterrupt:
                    print("\n\t------- KEYBOARD INTERRUPT SUCCESSFUL -------")
                    exit()
                except:
                    break

                if self.nextPage_token is None:
                    break
    def store_data(self):
        ################## storing data in a csv file ##################
        output_dict = {
            'parent video': self.v_id,
            'video title': self.v_title,
            'published': self.pub_time,
            'comment Id': self.com_ids,
            'comment text': self.com_text,
            'likes': self.likes,
        }

        out_df = pd.DataFrame(output_dict,columns = output_dict.keys())
        out_df.to_csv("comments_test.csv",index = False)
        print("########### SAVED IN FILE ###########")
    def mysql_store(self):
        ################## storing data in the local mysql database ##################
        cursor= mydb.cursor()
        for i,row in enumerate(self.com_ids):
            sql = "insert into yt_data(com_id,vid_id,comment,likes,vid_title,pub_time) values(%s,%s,%s,%s,%s,%s)"
            val = (self.com_ids[i],self.v_id[i],self.com_text[i][:200],self.likes[i],self.v_title[i],self.pub_time[i])
            cursor.execute(sql,val)
            mydb.commit()

        cursor.close()
 
if __name__ == "__main__":
    yt_obj = get_yt_data()
    yt_obj.get_keys()
    yt_obj.get_video_data()
    yt_obj.get_com_data()
    yt_obj.store_data()
    yt_obj.mysql_store()