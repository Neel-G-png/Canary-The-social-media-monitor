# social-media-buzz 
[Full reddit data](https://www.kaggle.com/carneyjp/251403-bookthemed-reddit-entries-with-sentiment "Orignal dataset")\
[Orignal Youtube data](https://www.kaggle.com/wchaktse/data-of-5132-youtube-videos?select=data_20210101_145809.csv "used to generated required dataset")

# Social Monitoring Dashboard

This project was built on react-hooks, context API and flask with JWT authentication.

Along with your peronal mysql connection with 4 seprate tables. Details of which are given below.

With this application we are able to utilize data for data interpretations and visualizations such as Outreach prediction, word cloud, sentiment analysis and brand mentions. 

The outreach prediction where by analyzing the previous trends and training the dataset we can predict the target audience outreach the post would have even before it goes live. This quick feedback for start-ups and companies helps them to quickly implement the changes required thus saving resources and ensuring to always get a higher chance of being visible on social media platforms.


## Objectives 
1. **Predicting Outreach** of various campaigns, posts and marketing strategies by predicting the impact it will have on the internet.
2. **Collecting Data from Public APIs** of multiple social media sites and storing them on a mysql database.
3. **Analysing** the indexed data and visualizing it via data visualization tools.
4. **Making strategic** market and business decisions based on the data shown on the dashboard.

## Public APIs used
1. PRAW / Tweepy  API
2. Youtube Data API V3
3. Twitter API V2

![landing page](https://github.com/Neel-G-png/Canary-The-social-media-monitor/blob/master/screenshots/dashboard.png)

![signup page](https://github.com/Neel-G-png/Canary-The-social-media-monitor/blob/master/screenshots/signup.png)

![login page](https://github.com/Neel-G-png/Canary-The-social-media-monitor/blob/master/screenshots/login.png)

![dashboard page](https://github.com/Neel-G-png/Canary-The-social-media-monitor/blob/master/screenshots/data.png)

## MySql tables you will need
![Tables](https://github.com/Neel-G-png/Canary-The-social-media-monitor/blob/master/screenshots/tables.PNG)

![User Password Keyword](https://github.com/Neel-G-png/Canary-The-social-media-monitor/blob/master/screenshots/user_data_details.PNG)

![Reddit Data](https://github.com/Neel-G-png/Canary-The-social-media-monitor/blob/master/screenshots/reddit_data_details.PNG)

![Youtube Data](https://github.com/Neel-G-png/Canary-The-social-media-monitor/blob/master/screenshots/youtube_data_details.PNG)

![Twitter Data page](https://github.com/Neel-G-png/Canary-The-social-media-monitor/blob/master/screenshots/twitter_data_details.PNG)

### `Run all the training files in twitter and youtube folders to generate models`
Store them in "models" folder inside "api folder"

### `python canary_api.py`

### `npm install`
Run from "complete project" folder to install node-modules

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.