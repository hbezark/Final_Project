#SI 206 Final Project
#Name: Hana Bezark

import requests
import json
import sqlite3
import time
import collections
import random
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS

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
	else:
		print('fetching data')
		CACHE_DICTION[search_term] = []
		page = 0 #The value of page corresponds to a set of 10 results. Page = 0 corresponds to records 0-9
		while page != 13: #Page = 10 corresponds to records 100-109 in order to get to the 100 interactions (There is no way to get exactly 100 interactions, it is either going to be 99 or 109)
			New_York_Times_baseurl = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
			New_York_Times_request = requests.get(New_York_Times_baseurl, params = {'q': search_term, 'fl': 'web_url, headline, keywords, news_desk, pub_date, byline, word_count', 'page': page, 'api-key': '9bbd4dcfe7c14c08badb0a3d571abc42'})
			time.sleep(1)
			New_York_Times_data = json.loads(New_York_Times_request.text)
			for item in New_York_Times_data['response']['docs']:
				CACHE_DICTION[search_term].append(item)
			page += 1
	f = open(CACHE_FNAME, 'w')
	f.write(json.dumps(CACHE_DICTION))
	f.close()
	return CACHE_DICTION[search_term]

def newyorktimes_info(search_term):
	New_York_Times_articles = newyorktimes_data(search_term)
	info = {}
	for article in New_York_Times_articles:
		if article['headline']['print_headline'] in info:
			continue
		info[article['headline']['print_headline']] = {}
		if 'web_url' not in article.keys():
			info[article['headline']['print_headline']]['web_url'] = "EMPTY" 
		else:
			info[article['headline']['print_headline']]['web_url'] = article['web_url'] 
		if 'new_desk' not in article.keys():
			info[article['headline']['print_headline']]['new_desk'] = "EMPTY"
		else:
			info[article['headline']['print_headline']]['new_desk'] = article['new_desk']
		if 'pub_date' not in article.keys():
			info[article['headline']['print_headline']]['pub_date'] = "EMPTY"
		else:
			info[article['headline']['print_headline']]['pub_date'] = article['pub_date']
		if 'byline' not in article.keys():
			info[article['headline']['print_headline']]['byline'] = "EMPTY" 
		else:
			info[article['headline']['print_headline']]['byline'] = article['byline']['original']
		if 'word_count' not in article.keys():
			info[article['headline']['print_headline']]['word_count'] = "EMPTY" 
		else:
			info[article['headline']['print_headline']]['word_count'] = article['word_count']
	return info

trump_New_York_Times_info = newyorktimes_info('Donald Trump')
#print(trump_New_York_Times_info)


# #SQL
# import pdb
# pdb.set_trace()
conn = sqlite3.connect('final_project_database.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS NYT')
cur.execute('CREATE TABLE NYT (Headline TEXT, Web_URL TEXT, New_Desk TEXT, Publication_Date TEXT, Byline TEXT, Word_Count TEXT)')

for key in trump_New_York_Times_info:
	cur.execute('INSERT INTO NYT (Headline, Web_URL, New_Desk, Publication_Date, Byline, Word_Count) VALUES (?, ?, ?, ?, ?, ?)', (key, trump_New_York_Times_info[key]['web_url'], trump_New_York_Times_info[key]['new_desk'], trump_New_York_Times_info[key]['pub_date'], trump_New_York_Times_info[key]['byline'], trump_New_York_Times_info[key]['word_count']))

conn.commit()
cur.close()

#New York Times Word Cloud
d = path.dirname(__file__)
#text = (' ').join(trump_New_York_Times_info)
#text = (' ').join(trump_New_York_Times_info[key])
text = open(path.join(d, 'trump.rtf')).read()
trump_mask = np.array(Image.open(path.join(d, "trump_pic.png")))
image_colors = ImageColorGenerator(trump_mask)
stopwords = set(STOPWORDS)
#stopwords.add("Trump")
#stopwords.add("Donald")
cloud = WordCloud(mask = trump_mask, stopwords = stopwords).generate(text)
plt.imshow(cloud.recolor(color_func=image_colors), interpolation = 'bilinear')
plt.axis('off')
plt.figure()
cloud.to_file(path.join(d, 'trump.png'))


