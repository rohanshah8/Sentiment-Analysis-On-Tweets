import tweepy 
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sklearn
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
#import sklearn.metrics.scorer
import matplotlib
matplotlib.use('Agg')

def do_work_gujarat(keyword):
	delhi=get_tweets_gujarat(keyword)

	filename='C:\\Users\\Rohan\\Desktop\\Sentiment-Analysis\\Nclfmodel.sav'
	clf=pickle.load(open(filename,'rb'))

	data1=delhi
	rawdata=data1['Tweets']
	data1= pd.DataFrame([preprocess_text(t) for t in rawdata],columns=['Tweets'])
	#clf=pickle.Unpickler(open(filename)).load()
	data1['Sentiment']=clf.predict(data1['Tweets'])
	k="-gujarat"
	bar_plot(data1,"".join([keyword, k]))
	return (data1['Sentiment'].value_counts())[0]-(data1['Sentiment'].value_counts())[1]

def do_work_delhi(keyword):
	delhi=get_tweets_delhi(keyword)

	filename='C:\\Users\\Rohan\\Desktop\\Sentiment-Analysis\\Nclfmodel.sav'
	clf=pickle.load(open(filename,'rb'))

	data1=delhi
	rawdata=data1['Tweets']
	data1= pd.DataFrame([preprocess_text(t) for t in rawdata],columns=['Tweets'])
	#clf=pickle.Unpickler(open(filename)).load()
	data1['Sentiment']=clf.predict(data1['Tweets'])
	k="-delhi"
	bar_plot(data1,"".join([keyword, k]))
	return (data1['Sentiment'].value_counts())[0]-(data1['Sentiment'].value_counts())[1]

def do_work(keyword):
	india=get_tweets(keyword)

	filename='C:\\Users\\Rohan\\Desktop\\Sentiment-Analysis\\Nclfmodel.sav'
	clf=pickle.load(open(filename,'rb'))
	data1=india
	rawdata=data1['Tweets']
	data1= pd.DataFrame([preprocess_text(t) for t in rawdata],columns=['Tweets'])
	#clf=pickle.Unpickler(open(filename)).load()
	data1['Sentiment']=clf.predict(data1['Tweets'])
	bar_plot(data1,keyword)

	return (data1['Sentiment'].value_counts())[0]-(data1['Sentiment'].value_counts())[1]

log = pd.read_csv("C:\\Users\\Rohan\\Desktop\\Sentiment-Analysis\\Login.csv")

consumerKey = log["key"][0] // edit your key secret token here
consumerSecret = log["key"][1]
accessToken = log["key"][2]
accessTokenSecret = log["key"][3]

authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret) 
        
authenticate.set_access_token(accessToken, accessTokenSecret) 
        
api = tweepy.API(authenticate, wait_on_rate_limit = True)


def get_tweets(keyword):
	#posts = api.user_timeline(screen_name=keyword, count = 200, lang ="en",include_retweets=True, tweet_mode="extended")

	#df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])
	#pd.set_option('display.max_colwidth', -1)
	#return df
	delhi_tweets={}
	query = keyword
	places = api.geo_search(query='INDIA', granularity="country")
	place_id = places[0].id
	date_since = "2019-11-16"
	for status in tweepy.Cursor(api.user_timeline,q=(query+" -filter:retweets")  and ("place:%s" %place_id),since=date_since,tweet_mode="extended",lang='en',locale='ja',result_type='recent',truncated=False).items():
	    delhi_tweets[status.created_at]=status.full_text
	delhi_tweets=pd.DataFrame(delhi_tweets.items(),columns=['Time_stamp','Tweets'])
	del delhi_tweets['Time_stamp']
	return delhi_tweets

def get_tweets_delhi(keyword):
	delhi_tweets={}
	query = keyword
	for status in tweepy.Cursor(api.search,q=query+"-filter:retweets",tweet_mode="extended",lang='en',locale='ja',result_type='recent',geocode="28.61309,77.209211,500km",truncated=False).items():
		delhi_tweets[status.created_at]=status.full_text
	delhi_tweets=pd.DataFrame(delhi_tweets.items(),columns=['Time_stamp','Tweets'])
	del delhi_tweets['Time_stamp']
	return delhi_tweets

def get_tweets_gujarat(keyword):
	log = pd.read_csv("C:\\Users\\Rohan\\Desktop\\Sentiment-Analysis\\Login.csv")

	consumerKey = log["key"][0]
	consumerSecret = log["key"][1]
	accessToken = log["key"][2]
	accessTokenSecret = log["key"][3]

	authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret) 
        
	authenticate.set_access_token(accessToken, accessTokenSecret) 
        
	api = tweepy.API(authenticate, wait_on_rate_limit = True)
	delhi_tweets={}
	query = keyword
	for status in tweepy.Cursor(api.search,q=query+"-filter:retweets",tweet_mode="extended",lang='en',locale='ja',result_type='recent',geocode="21.48642,69.93125,500km",truncated=False).items():
		delhi_tweets[status.created_at]=status.full_text
	delhi_tweets=pd.DataFrame(delhi_tweets.items(),columns=['Time_stamp','Tweets'])
	del delhi_tweets['Time_stamp']
	return delhi_tweets

def preprocess_text(text):
	text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','', str(text))
	text = re.sub('RT @[^\s]+','', str(text))
	text = re.sub('@[^\s]+','',str(text))
	text = text.lower().replace("ё", "е")
	text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ',str(text))
	text = re.sub(' +',' ',str(text))
	text=re.sub('#(\w+)','',str(text))
	RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
	return text.strip()

def strip_emoji(text):
	return RE_EMOJI.sub(r'', text)

def bar_plot(data1,keyword1):	
	plt.style.use('fivethirtyeight')
	plt.title(keyword1)
	plt.xlabel('Sentiment')
	plt.ylabel('Counts')
	data1['Sentiment'].value_counts().plot(kind = 'bar')
	plt.savefig('C:\\Users\\Rohan\\Desktop\\Sentiment-Analysis\\static\\img\\'+keyword1+'-bar.png')
	plt.clf() 
	plt.cla()
	plt.close()

def pie_plot(keys,x1,x2):
	fig = plt.figure()
	ax = fig.add_axes([0,0,1,1])
	ax.axis('equal')
	langs = keys
	score = [x1,x2]
	ax.pie(score, labels = keys,autopct='%1.2f%%')
	temp='pie-chart'+'-'+keys[0]+'-'+keys[1]
	plt.savefig('C:\\Users\\Rohan\\Desktop\\Sentiment-Analysis\\static\\img\\'+temp+'.png')
	plt.clf() 
	plt.cla()
	plt.close()
