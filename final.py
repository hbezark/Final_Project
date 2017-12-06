#SI 206 Final Project
#Name: Hana Bezark

import requests
import json
import sqlite3
import datetime
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
from os import path
from wordcloud import wordCloud, STOPWORDS

#Caching pattern
CACHE_FNAME = "206final_project.json" 
try: 
	cache_file = open(CACHE_FNAME, 'r') #Try to read the data from the cache_file
	cache_contents = cache_file.read() #If it's there, get it into a string
	CACHE_DICTION = json.loads(cache_contents) #And then load it into a dictionary
	cache_file.close() #Close the file, we're good, we got the data in a dictionary
except:
	CACHE_DICTION = {}

#API: New York Times
def newyorktimes_data(search_term):
	if search_term in CACHE_DICTION:
		print('using cache')
		results = CACHE_DICTION[search_term]
	if search_term not in CACHE_DICTION['New_York_Times']:
		print('fetching data')
		CACHE_DICTION['New_York_Times'][search_term] = []
		page = 0 #The value of page corresponds to a set of 10 results. Page = 0 corresponds to records 0-9
		while page != 10: #Page = 10 corresponds to records 100-109 in order to get to the 100 interactions (There is no way to get exactly 100 interactions, it is either going to be 99 or 109)
			New_York_Times_baseurl = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
			New_York_Times_request = requests.get(New_York_Times_baseurl, params = {'q': search_term, 'fl': 'web_url, headline, keywords, pub_date, byline, word_count', 'page': page, 'api-key': '9bbd4dcfe7c14c08badb0a3d571abc42'}
			New_York_Times_data = json.loads(New_York_Times_request.text)
			for item in New_York_Times_data['response']['docs']:
				CACHE_DICTION['New_York_Times'][search_term].append(item)
			page += 1
		f = open(CACHE_FNAME, 'w')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	return CACHE_DICTION['New_York_Times'][search_term]

def newyorktimes_info(search_term):
	New_York_Times_articles = newyorktimes_data(search_term)
	info = {}
	for article in New_York_Times_articles:
		info[article['headline']['main']] = (article['web_url'], article['keywords'], article['pub_date'], article['byline'], article['word_count'])
	return info

trump_New_York_Times_info = newyorktimes_info('Donald Trump')

#API: Yelp
def initialize_yelp_client():
	auth = Oauth1Authenticator(
	    consumer_key="qqfkowMgc--mtmvbiXAAAA",
	    consumer_secret="mn53in8yCNzni0HmIxZpjgGVxvQ",
	    token="mDuuEhFRBzHKLMty7QcA8iIC9jX3Kgh4",
	    token_secret="vm5NE7QilQ7uG8ihEA6VklBdUYY"
	)

	return Client(auth)
yelp_client = initialize_yelp_client()

def yelp_data(search_term2):
	if search_term2 in CACHE_DICTION:
		print('using cache')
		results = CACHE_DICTION[search_term2]
	if search_term2 not in CACHE_DICTION['Yelp']:
		print('fetching data')
		CACHE_DICTION['Yelp'][search_term2] = []

def yelp_info(search_term2):
	yelp_reviews = yelp_data(search_term2)
	info2 = {}
	for review in yelp_reviews:
		...
	return info2

summer_house_santa_monica_reviews = yelp_info('Sumemr House Santa Monica')

#SQL
conn = sqlite3.connect('final_project_database.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS New York Times')
cur.execute('CREATE TABLE New York Times (Headline TEXT, Web_URL TEXT, Keywords TEXT, Publication_Date TEXT, Byline TEXT, Word_Count TEXT)')

for article in trump_New_York_Times_info:
	cur.execute('INSERT INTO New York Times (Headline, Web_URL, Keywords, Publication_Date, Byline, Word_Count) VALUES (?, ?, ?, ?, ?, ?)', ([article['headline']['main']], (article['web_url'], article['keywords'], article['pub_date'], article['byline'], article['word_count'])

cur.execute('DROP TABLE IF EXISTS Yelp')
cur.execute('CREATE TABLE Yelp (Rating INTEGER, User TEXT, Text TEXT, Time_Created DATETIME, URL TEXT)')

for review in ___:
	cur.execute('INSERT INTO Yelp (Rating, User, Text, Time_Created, URL) VALUES (?, ?, ?, ?, ?'), ([reviews['rating'], [reviews]['user']['name'], reviews['text'], reviews['time_created'], reviews['url'])

conn.commit()

cur.close()

#New York Times Word Cloud
d = path.dirname(__file__)
text = (' ').join(trump_New_York_Times_info)
trump_mask = np.array(Image.open(path.join(d, "trump_pic.png")))
image_colors = ImageColorGenerator(trump_mask)
stopwords = set(STOPWORDS)
stopwords.add("")
stopwords.add("")
cloud = WordCloud(mask = trump_mask, stopwords = stopwords).generate(text)
plt.imshow(cloud.recolor(color_func=image_colors), interpolation = 'bilinear')
plt.axis('off')
plt.figure()
cloud.to_file(path.join(d, 'trump.png'))

#Yelp Plotly

