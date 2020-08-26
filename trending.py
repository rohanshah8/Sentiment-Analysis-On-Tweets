import tweepy 
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")



def find_trending():
	log = pd.read_csv("C:\\Users\\Rohan\\Desktop\\Sentiment-Analysis\\Login.csv") // login.csv contain all keys in comma separeted form
	consumerKey = log["key"][0]
	consumerSecret = log["key"][1]
	accessToken = log["key"][2]
	accessTokenSecret = log["key"][3]
	authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)   
	authenticate.set_access_token(accessToken, accessTokenSecret) 
	api = tweepy.API(authenticate, wait_on_rate_limit = True)

	INDIA_WOE_ID = 23424848

	INDIA_trends = api.trends_place(INDIA_WOE_ID)

	trends = json.loads(json.dumps(INDIA_trends, indent=1))

	#trends[0]["trends"]=cleanNullTerms(trends[0]["trends"])

	ignored_values = set(["null", "", None])

	trends[0]["trends"]=[elem for elem in trends[0]["trends"] if elem['tweet_volume'] not in ignored_values]

	name=[]
	tweet_volume=[]
	for trend in trends[0]["trends"]:
		if  trend["name"] is not None and  trend["tweet_volume"] is not None:
			#print (trend["name"].strip("#") +"-------"+ str(trend["tweet_volume"]))
			name.insert(0,str(trend["name"].strip("#")) )
			tweet_volume.insert(0,int(str(trend["tweet_volume"])))
	#print (trend["tweet_volume"])

	#places = api.geo_search(query="INDIA", granularity="country")
	#place_id = places[0].id
	#print('india id is: ',place_id)
	fig, ax = plt.subplots(figsize=(15, 12))
	sns.barplot(y=name[0:15],x=tweet_volume[0:15],orient="h")
	plt.title("Treending ")
	temp='trend'
	plt.savefig('C:\\Users\\Rohan\\Desktop\\Sentiment-Analysis\\static\\img\\'+temp+'.png')

find_trending()
# Plot horizontal bar graph
#trends[0]["trends"].sort_values(by=trend["tweet_volume"]).plot.barh(x='tweets',
#                      y='name',
#                      ax=ax,
#                      color="purple")
#
#ax.set_title("Common Words Found in Tweets (Including All Words)")

#plt.show()
