from googleapiclient.discovery import build
import pandas as pd
from youtubesearchpython import *
import time
import re
import mysql.connector

################## setting up  youtube service ##################
API_KEY = "####################"
youtube = build('youtube','v3',developerKey = API_KEY)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "####################",
    database = "####################",
)

class get_yt_data:
    product_keys = {}
    keywords = ""
    keys = []
    idlist = []
    title_list = []

    com_ids = []
    v_id = []
    com_text = []
    likes = []
    v_title = []
    pub_time = []

    nextPage_token = None
    com_counter = 0
    time_check = "2015-05-07T11:05:02Z"

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

        # print(self.keys)

    def get_video_data(self):
        print("IN VID DATA")
        cursor = mydb.cursor()
        sql = "select distinct vid_id from yt_data;"
        cursor.execute(sql)
        vid_id_present = cursor.fetchall()
        # print(vid_id_present)
        vid_id_present = str(vid_id_present)
        # for row in vid_id_present:
        #     print(row[0])
        for key in self.keys:
            VSearch = VideosSearch(key)
            result = VSearch.result()
            # print(key)
            count = 0
            i= 0

            while(count<5):
                # print("test")
                try:
                    check_if_present = "('"
                    # print(f"\n{count+1} ) ",result['result'][i]['id'])
                    check_if_present = check_if_present + str(result['result'][i]['id']) + "',)"
                    if check_if_present not in vid_id_present:
                        self.idlist.append(result['result'][i]['id'])
                        self.title_list.append(result['result'][i]['title'])
                    i+=1
                    count+=1
                except:
                    # i=03
                    # count+=len(result['result'])
                    # print("\n####################### COUNT #######################\n\t",count)
                    VSearch.next()
                    result = VSearch.result()
                    i=0
    def get_com_data(self):
        for i,v in enumerate(self.idlist):
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
                        time_c = item['snippet']['topLevelComment']['snippet']['publishedAt']
                        if time_c>self.time_check:
                            self.v_id.append(v)
                            self.v_title.append(self.title_list[i])
                            self.com_text.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                            self.com_ids.append(item['snippet']['topLevelComment']['id'])
                            self.likes.append(item['snippet']['topLevelComment']['snippet']['likeCount'])
                            # time_c = item['snippet']['topLevelComment']['snippet']['publishedAt']
                            self.pub_time.append(item['snippet']['topLevelComment']['snippet']['publishedAt'])
                            # print(type(item['snippet']['topLevelComment']['snippet']['publishedAt']))
                            com_counter+=1
                        print("Comments downloaded:", com_counter, end="\r")
                except KeyboardInterrupt:
                    print("\n\t------- KEYBOARD INTERRUPT SUCCESSFUL -------")
                    exit()
                except:
                    break

                if self.nextPage_token is None:
                    break
    def store_data(self):
        output_dict = {
            'parent video': self.v_id,
            'video title': self.v_title,
            'published': self.pub_time,
            'comment Id': self.com_ids,
            'comment text': self.com_text,
            'likes': self.likes,
        }

        out_df = pd.DataFrame(output_dict,columns = output_dict.keys())
        out_df.to_csv("comments.csv",index = False)
        print("########### SAVED IN FILE ###########")
    def mysql_store(self):
        cursor= mydb.cursor()
        for i,row in enumerate(self.com_ids):
            sql = "insert into yt_data(com_id,vid_id,comment,likes,vid_title,pub_time) values(%s,%s,%s,%s,%s,%s)"
            val = (self.com_ids[i],self.v_id[i],self.com_text[i][:200],self.likes[i],self.v_title[i],self.pub_time[i])
            cursor.execute(sql,val)
            mydb.commit()

        cursor.close()

'''
################## getting relevant videos ##################
product_keys = {}
keywords = ""
cursor1= mydb.cursor()
cursor1.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
cursor1.execute("select * from product_keys")# where user_id = '%s'",val)
users_keywords = cursor1.fetchall()
for row in users_keywords:
    product_keys[row[0]] = row[1]
    keywords = keywords + ", "+str(row[1])

# keywords = ['neel','earbuds','dell 7559']

keywords = str(keywords)
keywords = re.sub(r'[^A-Za-z0-9_, ]+','',keywords)
keys = keywords.split(',')
keys = list(dict.fromkeys(keys))
if '' in keys:
    keys.remove('')
for i,key in enumerate(keys):
    keys[i] = key.strip()

print(keys)
# key = 'neel'
#,limit = 3)

idlist = []
title_list = []
for key in keys:
    VSearch = VideosSearch(key)
    result = VSearch.result()
    print(key)
    count = 0
    i= 0

    while(count<5):
        try:
            # print(f"\n{count+1} ) ",result['result'][i]['id'])
            idlist.append(result['result'][i]['id'])
            title_list.append(result['result'][i]['title'])
            i+=1
            count+=1
        except:
            # i=03
            # count+=len(result['result'])
            # print("\n####################### COUNT #######################\n\t",count)
            VSearch.next()
            result = VSearch.result()
            i=0

# result = youtube.search().list(part = 'snippet',
#                                q = query,
#                                order = 'relevance',
#                                type = 'video',).execute()#safeSearch = 'moderate',

com_ids = []
v_id = []
com_text = []
likes = []
v_title = []
pub_time = []

nextPage_token = None

com_counter = 0
time_check = "2021-05-07T11:05:02Z"

print("########### STARTING TO COLLECT COMMENT ###########")
start = time.time()
for i,v in enumerate(idlist):
    while True:
        try:
            com_thread = youtube.commentThreads().list(
                part = 'snippet',
                videoId = v,
                maxResults = 100,
                order = 'relevance',
                textFormat = 'plainText',
                pageToken = nextPage_token,).execute()
            nextPage_token = com_thread.get('nextPageToken')
            for item in com_thread['items']:
                time_c = item['snippet']['topLevelComment']['snippet']['publishedAt']
                if time_c>time_check:
                    v_id.append(v)
                    v_title.append(title_list[i])
                    com_text.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                    com_ids.append(item['snippet']['topLevelComment']['id'])
                    likes.append(item['snippet']['topLevelComment']['snippet']['likeCount'])
                    # time_c = item['snippet']['topLevelComment']['snippet']['publishedAt']
                    pub_time.append(item['snippet']['topLevelComment']['snippet']['publishedAt'])
                    # print(type(item['snippet']['topLevelComment']['snippet']['publishedAt']))
                    com_counter+=1
                print("Comments downloaded:", com_counter, end="\r")
        except KeyboardInterrupt:
            print("\n\t------- KEYBOARD INTERRUPT SUCCESSFUL -------")
            exit()
        except:
            break

        if nextPage_token is None:
            break
    
total_time = time.time() - start
print("\nTIME TAKEN : ",total_time)
print("########### COMMENTS COLLECTED ###########")
output_dict = {
    'parent video': v_id,
    'video title': v_title,
    'published': pub_time,
    'comment Id': com_ids,
    'comment text': com_text,
    'likes': likes,
}

out_df = pd.DataFrame(output_dict,columns = output_dict.keys())
out_df.to_csv("comments.csv",index = False)
print("########### SAVED IN FILE ###########")

'''
if __name__ == "__main__":
    yt_obj = get_yt_data()
    yt_obj.get_keys()
    yt_obj.get_video_data()
    yt_obj.get_com_data()
    yt_obj.store_data()
    yt_obj.mysql_store()