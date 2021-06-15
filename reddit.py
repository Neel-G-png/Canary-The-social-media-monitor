import praw
import requests
import urllib.request
from threading import Thread
import time
import pandas as pd
import winsound


reddit = praw.Reddit(client_id = '####################',
                     client_secret = '####################',
                     user_agent = '####################',
                     username = '####################',
                     password = '####################')

''' Change the data using pandas '''



class operations:
    sub_file = open("submission_list.txt",'a',1)
    com_file = open("comment_list.txt",'a',1)
    stop_sub_thread = False
    stop_com_thread = False
    def old_comment(self,url):
        #self.sub_url = url
        submission = reddit.submission(url=url)
        comments = submission.comments.list()
        for comment in comments:
            self.com_file.write(f"\nOLD COMMENT = {comment.body}")

    def stream_submission_comments(self,subreddit):
        print("thread 2 started")
        for comment in subreddit.stream.comments():#skip_existing = True):
            with open("submission_list.txt",'r') as f:
                sub_ids = f.readlines()
                com_id = comment.link_id+"\n"
                if com_id in sub_ids: #add all comments containing the keywords (or keyword in com.body:)
                    print("----- COM ADDED -----")
                    self.com_file.write("---------- NEW COM ----------")
                    self.com_file.write(f"\nID = {comment.link_id}")
                    self.com_file.write(f"\nCOMMENT = {comment.body}")
                if self.stop_com_thread == True:
                    break

    def stream_submissions(self,subreddit,find):
        print("thread 1 started")
        find = find.upper()
        i = 0
        for submission in subreddit.stream.submissions():
            title = submission.title.upper()
            sub_text = submission.selftext.upper()
            if find in title or find in sub_text:
                i+=1
                print(f"\n---------- NEW POST {i}----------")
                print(f"ID    = https://www.reddit.com/{submission.permalink}")
                print(f"title = {submission.title}")
                self.sub_file.write(f"{submission.name}\n")
                beep()
            if self.stop_sub_thread == True:
                break

def beep():
    frequency = 2500  # Set Frequency To 2500 Hertz
    duration = 150  # Set Duration To 1000 ms == 1 second
    winsound.Beep(frequency, duration)

if __name__ == "__main__":
    subreddit = reddit.subreddit('all')
    search_for = "book"
    red_obj = operations()
    T1 = Thread(target=red_obj.stream_submissions,args=(subreddit,search_for,))
    T2 = Thread(target=red_obj.stream_submission_comments,args=(subreddit,))
    try:
        T1.start()
        T2.start()
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        print("\n\t------- KEYBOARD INTERRUPT SUCCESSFUL -------")
        red_obj.stop_sub_thread = True
        red_obj.stop_com_thread = True

"""
    Create: Flask API for POST: To create data of the reddit
    Read: Flask API for GET (List/Individual): Fetch data from React
"""