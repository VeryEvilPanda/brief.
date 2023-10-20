# Copyright © William Adams 2023, licensed under Mozilla Public License Version 2.0

# pip install lxml

import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('IMAGE_API_KEY')

def getNews():
    pass


def getHeadlinesBBCRSS():
    response = requests.get("http://feeds.bbci.co.uk/news/rss.xml")
    bs = BeautifulSoup(response.text, 'xml')
    stories = bs.find_all('item')
    stories_list = []
    for story in stories:
        story_dict = {}
        story_dict['headline'] = story.find('title').text
        story_dict['summary'] = story.find('description').text
        story_dict['url'] = story.find('guid').text
        story_dict['date'] = story.find('pubDate').text
        stories_list.append(story_dict)
    return stories_list
    


    

def getHeadlinesBBC():
    # Not my code lmao: https://jonathansoma.com/lede/foundations-2017/classes/adv-scraping/scraping-bbc/
    response = requests.get("http://www.bbc.com/news")
    doc = BeautifulSoup(response.text, 'html.parser')
    # Start with an empty list
    stories_list = []
    stories = doc.find_all('div', { 'class': 'gs-c-promo' })
    for story in stories:
        # Create a dictionary without anything in it
        story_dict = {}
        headline = story.find('h3')
        link = story.find('a')
        summary = story.find('p')
        image = story.find('img')
        if headline and link and summary and image:
            story_dict['headline'] = headline.text
            story_dict['url'] = 'https://bbc.co.uk' + link['href']
            story_dict['summary'] = summary.text
            # Add the dict to our list
            stories_list.append(story_dict)
    return stories_list


def dictToHeadlines(newsDict):
    headlines = []
    for i in newsDict:
        headlines.append(i['headline'])
    return headlines

# Need a better way to do this
def getImage(headlines):
    img_urls = []
    for headline in headlines:
        response = requests.get(f"https://serpapi.com/search?q={headline.replace(' ', '%20')}%20site:bbc.co.uk&tbm=isch&api_key={api_key}")
        img_urls.append(response.json()['images_results'][0]['original'])
    return img_urls

def formatNewsHTML(news, img_urls, num = 5):
    newsString = '<p>'
    for i in range(num):
        newsString += f"<a href='{news[i]['url']}'><img src='{img_urls[i]}' width=100><br>"
        newsString += f"{news[i]['headline']}</a>"
        newsString += f"<br>{news[i]['summary']}"
        newsString += f"<br>Published: {news[i]['date']}<br><br>"
        newsString += '</p>'
    return newsString






def main():
    print("Getting news...")
    news = getHeadlinesBBCRSS()
    print("News obtained from BBC")
    print("Preparing to get images...")
    headlines = dictToHeadlines(news)
    print("Preparation complete")
    print("Getting images... (this can take a while)")
    img_urls = getImage(headlines)
    print("Images retrieved")
    return formatNewsHTML(news, img_urls)
