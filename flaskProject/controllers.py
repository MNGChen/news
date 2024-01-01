from models import db, News
from serpapi import GoogleSearch
from urllib.parse import parse_qsl, urlsplit
from config import Config
import datetime

def search_news(keywords, filter, nfpr, safe, location, gl, lr, no_cache, tbs, task_id_input):
    GoogleSearch.SERP_API_KEY = Config.SERP_API_KEY
    search = GoogleSearch({
        "q": keywords,  # search
        "tbm": "nws",  # news
        "filter": filter,  # filter
        "nfpr": nfpr,  # nfpr
        "safe": safe,  # safe
        "location": location,  # location
        "gl": gl,  # gl
        "lr": lr,  # lr
        "no_cache": no_cache,  # no_cache
        "tbs": tbs,  # "qdr:d",   last 24h
        "num": "100",  # number of news
    })
    data = search.get_dict()
    news_num = len(data['news_results'])
    page_num = 1
    position_num = 0
    page_news_num = len(data['news_results'])
    while position_num < page_news_num:
        news = News()
        news.link = data['news_results'][position_num]['link']
        news.title = data['news_results'][position_num]['title']
        news.source = data['news_results'][position_num]['source']
        news.date = data['news_results'][position_num]['date']
        news.snippet = data['news_results'][position_num]['snippet']
        news.thumbnail = data['news_results'][position_num]['thumbnail']
        news.task_id = task_id_input
        news.create_time = datetime.datetime.now()
        news.create_time = datetime.datetime.now()
        db.session.add(news)
        db.session.commit()
        position_num += 1
    while 'next' in data.get('serpapi_pagination', {}):
        search.params_dict.update(dict(parse_qsl(urlsplit(data.get('serpapi_pagination', {}).get('next')).query)))
        data = search.get_dict()
        page_news_num = len(data['news_results'])
        position_num = 0
        while position_num < page_news_num:
            news = News()
            news.link = data['news_results'][position_num]['link']
            news.title = data['news_results'][position_num]['title']
            news.source = data['news_results'][position_num]['source']
            news.date = data['news_results'][position_num]['date']
            news.snippet = data['news_results'][position_num]['snippet']
            news.thumbnail = data['news_results'][position_num]['thumbnail']
            news.task_id = task_id_input
            # get current timestamp and save to create_time and update_time
            news.create_time = datetime.datetime.now()
            news.create_time = datetime.datetime.now()
            db.session.add(news)
            db.session.commit()
            position_num += 1
        news_num += len(data['news_results'])
        page_num += 1

    print('page_num: ' + str(page_num))
    print('news_num: ' + str(news_num))
