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
CACHE_FNAME = "206final_project.json"  #The name of the cache file is '206final_project.json'
try: 
	cache_file = open(CACHE_FNAME, 'r')  #Try to read the data from the cache_file
	cache_contents = cache_file.read()  #If it's there, get it into a string
	CACHE_DICTION = json.loads(cache_contents)  #And then load it into a dictionary
	cache_file.close()  #Close the file, we're good, we got the data in a dictionary
except:
	CACHE_DICTION = {}  


#API: New York Times
def newyorktimes_data(search_term):
	if search_term in CACHE_DICTION:  #Checks if the search term is in the cached file
		print('using cache')  #Print 'using cache'
		results = CACHE_DICTION[search_term]  #If the search term has already been cached, it uses the data in the file and returns that
	else:  #If there is not cached data
		print('fetching data')  #Print 'fetching data'
		CACHE_DICTION[search_term] = []
		page = 0  #The value of page corresponds to a set of 10 results. Page = 0 corresponds to records 0-9
		while page != 13:  #Page = 13 corresponds to records 130-139 in order to get to the 100 interactions (There is no way to get exactly 100 interactions - I needed to loop through 13 pages in order to get as close to the 100 interactions as possible in my database, because there are repeats)
			New_York_Times_baseurl = "https://api.nytimes.com/svc/search/v2/articlesearch.json" 
			New_York_Times_request = requests.get(New_York_Times_baseurl, params = {'q': search_term, 'fl': 'web_url, headline, keywords, news_desk, pub_date, byline, word_count, score', 'page': page, 'api-key': 'enter-api-key'})  #Makes a request to get each article's web url, headline, keywords, news desk, publication date, byline word count and score that contains the search term
			time.sleep(1)  #Time delay of one second so that the program does not move onto the next line of the code before all of the data has been collected
			New_York_Times_data = json.loads(New_York_Times_request.text)
			for item in New_York_Times_data['response']['docs']:  #Loops through json object and gets data that is nested within response and then docs dictionaries
				CACHE_DICTION[search_term].append(item)  #Appends dictionaries containing all information to the cache
			page += 1  #Loops through the pages until the page number is 13 
	cache_file1 = open(CACHE_FNAME, 'w')  #Opens the cache file 
	cache_file1.write(json.dumps(CACHE_DICTION))  #Write the new information into the cached file
	cache_file1.close()  #Closes the cache file
	return CACHE_DICTION[search_term]  #Returns a list of dictionaries that contains each article's web url, headline, keywords, news desk, publication date, byline, word count and score

def newyorktimes_info(search_term):
	New_York_Times_articles = newyorktimes_data(search_term)  #Creates variable New_York_Times_articles that contains all of the data gathered above
	info = {}  #Initializes empty dictionary
	for article in New_York_Times_articles:  #Loops through every article in the cache
		if article['headline']['print_headline'] in info:  #If the article's print headline is in the dictionary...
			continue  #Continue with the code block (This and the line above are necessary because there are some duplicate print headlines)
		info[article['headline']['print_headline']] = {}  #The print headline is the key in the dictionary
		if 'web_url' not in article.keys():  #If an article does not have a web url...
			info[article['headline']['print_headline']]['web_url'] = "EMPTY"  #Set the web url equal to EMPTY
		else:  #If an article does have a web url...
			info[article['headline']['print_headline']]['web_url'] = article['web_url']  #Store the web url
		if 'new_desk' not in article.keys():  #If an article does not have a news desk
			info[article['headline']['print_headline']]['new_desk'] = "EMPTY"  #Set the news desk equal to EMPTY
		else:  #If an article does have a news desk...
			info[article['headline']['print_headline']]['new_desk'] = article['new_desk']  #Store the news desk
		if 'pub_date' not in article.keys():  #If an article does not have a publication date...
			info[article['headline']['print_headline']]['pub_date'] = "EMPTY"  #Set the publication date equal to EMPTY
		else:  #If an article does have a publication date...
			info[article['headline']['print_headline']]['pub_date'] = article['pub_date']  #Store the publication date
		if 'byline' not in article.keys():  #If an article does not have a byline...
			info[article['headline']['print_headline']]['byline'] = "EMPTY"  #Set the byline equal to EMPTY
		else:  #If an article does have a byline...
			info[article['headline']['print_headline']]['byline'] = article['byline']['original']  #Store the byline
		if 'word_count' not in article.keys():  #If an article does not have a word count...
			info[article['headline']['print_headline']]['word_count'] = "EMPTY"  #Set the word count to EMPTY
		else:  #If an article does have a word count...
			info[article['headline']['print_headline']]['word_count'] = article['word_count']  #Store the word count
		if 'score' not in article.keys():  #If an article does not have a score...
			info[article['headline']['print_headline']]['score'] = EMPTY  #Set the score to EMPTY
		else:  #If an article does have a score...
			info[article['headline']['print_headline']]['score'] = article['score'] #Store the score
	return info  #Return the dictinary

trump_New_York_Times_info = newyorktimes_info('Donald Trump')  #Saves web url, headline, keywords, news desk, publication date, byline and word count for articles that contain the search term Donald Trump in the variable trump_New_York_Times_info 

print("Here are the headlines from articles containing the search term Donald Trump:\n")
for key in trump_New_York_Times_info:  #For each headline in the dictionary
	print(key)  #Print the headline


#SQL
conn = sqlite3.connect('final_project_database.sqlite')  #SQL database is named final_project_database.sqlite
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS New_York_Times')  #Removes the table if it exists so tha we can create a table without errors
cur.execute('CREATE TABLE New_York_Times (Headline TEXT, Web_URL TEXT, New_Desk TEXT, Publication_Date TEXT, Byline TEXT, Word_Count TEXT, Score INTEGER)')  #Creates the table with the specified columns

for key in trump_New_York_Times_info:
	cur.execute('INSERT INTO New_York_Times (Headline, Web_URL, New_Desk, Publication_Date, Byline, Word_Count, Score) VALUES (?, ?, ?, ?, ?, ?, ?)', 
	(key, trump_New_York_Times_info[key]['web_url'], trump_New_York_Times_info[key]['new_desk'], trump_New_York_Times_info[key]['pub_date'], trump_New_York_Times_info[key]['byline'], trump_New_York_Times_info[key]['word_count'], trump_New_York_Times_info[key]['score']))  #Navigates through the nested dictionary to find desires variables and puts desired variables into the table columns

conn.commit()  #Commits the information into the table
cur.close()  #Closes the cursor


#New York Times Word Cloud
d = path.dirname(__file__) #Sets the path of the running script equal to d so that the word coud can later be saved to my working directory
text = open(path.join(d, 'trump.rtf')).read()  #Opens text file containing print headlines and reads that file
trump_mask = np.array(Image.open(path.join(d, "trump_pic.png")))  #Uploads image in directory named trump_pic.png to be used for the colors of the words in the cloud
trump_colors = ImageColorGenerator(trump_mask)  #Assigns colors from the picture in the line above to variable trump_colors to be used later
stopwords = set(STOPWORDS)  #Initializes stop words, which are the words to be used in the cloud
cloud = WordCloud(mask = trump_mask, stopwords = stopwords).generate(text)  #Creates the word cloud based on the text file above
plt.imshow(cloud.recolor(color_func=trump_colors), interpolation = 'bilinear')  #Word cloud is colored based on colors saved from picture above
plt.axis('off')  #No axis
plt.figure()  #Finishes creating the word cloud
cloud.to_file(path.join(d, 'trump.png'))  #Saves the word cloud as trump.png in the directory I am working from 


