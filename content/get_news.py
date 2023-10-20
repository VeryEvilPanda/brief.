# Copyright © William Adams 2023, licensed under Mozilla Public License Version 2.0

import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import aiohttp
from database import mongo_database 
import asyncio

database = mongo_database

async def getNews():
    response = await getHeadlinesBBC()
    if response[0]:
        stories_list = response[1]
        for story in stories_list:
            await updateDatabaseNews(story)
        print('true')
        return True, 200
    else:
        print('false')
        return response
    


async def updateDatabaseNews(news_item):
    collection = database.client['brief_content']['news']
    await collection.insert_one(news_item)



async def getHeadlinesBBC():
    async with aiohttp.request('GET', "http://feeds.bbci.co.uk/news/rss.xml") as response:
        if response.status == 200:
            data = await response.text()
            bs = BeautifulSoup(data, 'xml')
            stories = bs.find_all('item')
            stories_list = []
            for story in stories:
                story_dict = {}
                story_dict['headline'] = story.find('title').text
                story_dict['summary'] = story.find('description').text
                story_dict['url'] = story.find('guid').text
                story_dict['date'] = story.find('pubDate').text
                stories_list.append(story_dict)
            return True, stories_list
        else:
            return False, response.status




asyncio.run(getNews())

