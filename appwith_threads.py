from flask import Flask , jsonify,redirect, request,render_template
from flask_mysqldb import MySQL
# from flask_classfull import FlaskView
import json
import mysql.connector
import time
# from flaskthreads import AppContextThread
from threading import Thread
from multiprocessing import Process, Value
import re
import praw
import datetime

app = Flask(__name__)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "####################",
    database = "neel",
)


# TEXT RANK AALGORITHM

reddit = praw.Reddit(client_id = '####################',
                     client_secret = '####################',
                     user_agent = '####################',
                     username = '####################',
                     password = '####################')

# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '####################'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_DB'] = 'neel'
# app.config['MYSQL_CURCSORCLASS'] = 'DictCursor'
app.config["DEBUG"] = False
# mysql = MySQL(app)


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
        cursor1.execute("select * from product_keys")# where user_id = '%s'",val)
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
        # get_keys()
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
                site = "reddit"
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


@app.route("/end")
def stop_exe():
    """
    to stop the data streaming in order to switch of the server
    
    """
    obj.thread_quit = True
    return "<h1>STOPPED</h1>"

@app.route("/savekeywords",methods = ['POST','GET'])
def savekeywords():
    msg = ""
    # global product_keys
    if request.method == 'POST':
        user = request.form['user']
        keywords = request.form['keywords']
        cursor = mydb.cursor()
        sql = "insert into product_keys(user_id,keywords) values(%s,%s)"
        val = (user,keywords)
        cursor.execute(sql,val)
        mydb.commit()
        obj.get_keys()
        # product_keys = p_k
        msg = "data added"
        return redirect('/showkeywords')
        
    # print()
    return render_template("login.html",msg = msg)

@app.route("/showkeywords")
def product():
    # global product_keys
    cur = mydb.cursor()
    sql = "select * from product_keys;"
    cur.execute(sql)
    results = []
    columns = [column[0] for column in cur.description]
    # print("\n\tROWS",len(cur.fetchall()))
    all_data = cur.fetchall()
    for row in all_data:
        results.append(dict(zip(columns,row)))
    # all_data
    print("\n PRODUCT KEYS : ",obj.product_keys)
    return jsonify(results)

@app.route("/showdata")
def select():
    cur = mydb.cursor()
    cur.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
    sql = "select * from reddit_data"
    cur.execute(sql)
    results = []
    columns = [column[0] for column in cur.description]
    all_data = cur.fetchall()
    for row in all_data:
        results.append(dict(zip(columns,row)))
    cur.close()
    return jsonify(results)


@app.route("/showuserdata")
def specific_data():
    pass

if __name__ == "__main__":
    obj.get_keys()
    T_reddit_data = Thread(target = obj.get_redditt_data)
    try:
        T_reddit_data.start()
        app.run()
        while True: time.sleep(100)
    except(KeyboardInterrupt, SystemExit):
        print("\n\t------- KEYBOARD INTERRUPT SUCCESSFUL -------")
        obj.thread_quit = True
        T_reddit_data.join()
        exit()