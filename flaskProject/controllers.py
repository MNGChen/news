from models import db, News
from serpapi import GoogleSearch
from urllib.parse import parse_qsl, urlsplit
from config import Config
import pandas as pd
from datetime import datetime, timedelta
import time


def search_news(keywords, filter, nfpr, safe, location, gl, lr, no_cache, tbs, task_id_input, keyword_id_input, dept_belong_id_input):

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
    if 'news_results' not in data:
        return "no news found"
    news_num = len(data['news_results'])
    page_num = 1
    position_num = 0
    reject_num = 0
    page_news_num = len(data['news_results'])
    while position_num < page_news_num:
        # get the new link
        news_link = data['news_results'][position_num]['link']
        # 检查数据库中是否已存在相同的 link
        existing_news = News.query.filter_by(link=news_link).first()
        if existing_news is None:
            news_upload = News()
            # get data from serpapi
            news_upload.link = data['news_results'][position_num]['link']
            news_upload.title = data['news_results'][position_num]['title']
            news_upload.source = data['news_results'][position_num]['source']
            news_upload.date = time_convert(data['news_results'][position_num]['date'])
            news_upload.snippet = data['news_results'][position_num]['snippet']
            news_upload.thumbnail = data['news_results'][position_num]['thumbnail']
            news_upload.task_id = task_id_input
            news_upload.keyword_id = keyword_id_input
            news_upload.dept_belong_id = dept_belong_id_input
            news_upload.create_time = time.time()
            news_upload.update_time = time.time()
            # update to database
            db.session.add(news_upload)
            db.session.commit()
        else:
            reject_num += 1

        position_num += 1
    while 'next' in data.get('serpapi_pagination', {}):
        search.params_dict.update(dict(parse_qsl(urlsplit(data.get('serpapi_pagination', {}).get('next')).query)))
        data = search.get_dict()
        if 'news_results' not in data:
            break
        page_news_num = len(data['news_results'])
        position_num = 0
        while position_num < page_news_num:
            # get the new link
            news_link = data['news_results'][position_num]['link']
            # 检查数据库中是否已存在相同的 link
            existing_news = News.query.filter_by(link=news_link).first()
            if existing_news is None:
                news_upload = News()
                # get data from serpapi
                news_upload.link = data['news_results'][position_num]['link']
                news_upload.title = data['news_results'][position_num]['title']
                news_upload.source = data['news_results'][position_num]['source']
                news_upload.date = time_convert(data['news_results'][position_num]['date'])
                news_upload.snippet = data['news_results'][position_num]['snippet']
                news_upload.thumbnail = data['news_results'][position_num]['thumbnail']
                news_upload.task_id = task_id_input
                news_upload.keyword_id = keyword_id_input
                news_upload.dept_belong_id = dept_belong_id_input
                news_upload.create_time = time.time()
                news_upload.update_time = time.time()
                # update to database
                db.session.add(news_upload)
                db.session.commit()
            else:
                reject_num += 1
            position_num += 1
        news_num += len(data['news_results'])
        page_num += 1

    print('page_num: ' + str(page_num))
    print('news_num: ' + str(news_num))
    print('reject_num: ' + str(reject_num))

def search_keyword():
    with app.app_context():
        GoogleSearch.SERP_API_KEY = "39ffcd6e2c5819a50c7ceb95d2dcecec4f38960d1f065a0f33c848e1abf51da2"
        search = GoogleSearch({
            "q": "usa",  # search
            "tbm": "nws",  # news
            "tbs": "qdr:d",  # last 24h
            "num": "100",  # number of news
        })
        data = search.get_dict()
        if 'news_results' not in data:
            return "no news found"
        news_num = len(data['news_results'])
        page_num = 1
        position_num = 0
        page_news_num = len(data['news_results'])
        while position_num < page_news_num:
            news_upload = News()
            news_upload.link = data['news_results'][position_num]['link']
            news_upload.title = data['news_results'][position_num]['title']
            news_upload.source = data['news_results'][position_num]['source']
            news_upload.date = time_convert(data['news_results'][position_num]['date'])
            news_upload.snippet = data['news_results'][position_num]['snippet']
            news_upload.thumbnail = data['news_results'][position_num]['thumbnail']
            news_upload.task_id = task_id_input
            news_upload.keyword_id = keyword_id_input
            news_upload.dept_belong_id = dept_belong_id_input
            news_upload.create_time = time.time()
            news_upload.update_time = time.time()
            non_duplicate_data = news_upload[~news_upload.isin(existing_data.to_dict('list')).all(axis=1)]
            non_duplicate_data.to_sql('news', db.engine, if_exists='append', index=False)
            position_num += 1
        while 'next' in data.get('serpapi_pagination', {}):
            search.params_dict.update(dict(parse_qsl(urlsplit(data.get('serpapi_pagination', {}).get('next')).query)))
            data = search.get_dict()
            if 'news_results' not in data:
                break
            page_news_num = len(data['news_results'])
            position_num = 0
            while position_num < page_news_num:
                news_upload = News()
                news_upload.link = data['news_results'][position_num]['link']
                news_upload.title = data['news_results'][position_num]['title']
                news_upload.source = data['news_results'][position_num]['source']
                news_upload.date = time_convert(data['news_results'][position_num]['date'])
                news_upload.snippet = data['news_results'][position_num]['snippet']
                news_upload.thumbnail = data['news_results'][position_num]['thumbnail']
                news_upload.task_id = task_id_input
                news_upload.keyword_id = keyword_id_input
                news_upload.dept_belong_id = dept_belong_id_input
                news_upload.create_time = time.time()
                news_upload.update_time = time.time()
                non_duplicate_data = news_upload[~news_upload.isin(existing_data.to_dict('list')).all(axis=1)]
                non_duplicate_data.to_sql('news', db.engine, if_exists='append', index=False)
                position_num += 1
            news_num += len(data['news_results'])
            page_num += 1

        print('page_num: ' + str(page_num))
        print('news_num: ' + str(news_num))


def time_convert(date_str):
    # current time
    date = datetime.now()

    if 'month' in date_str:
        month = int(date_str.split(' ')[0])
        date = timedelta(days=month * 30)
        return (datetime.now() - date).strftime("%Y-%m-%d %H:%M:%S")

    if 'day' in date_str:
        day = int(date_str.split(' ')[0])
        date = timedelta(days=day)
        return (datetime.now() - date).strftime("%Y-%m-%d %H:%M:%S")

    if 'hour' in date_str:
        hour = int(date_str.split(' ')[0])
        date = timedelta(hours=hour)
        return (datetime.now() - date).strftime("%Y-%m-%d %H:%M:%S")

    if 'min' in date_str:
        minute = int(date_str.split(' ')[0])
        date = timedelta(minutes=minute)
        return (datetime.now() - date).strftime("%Y-%m-%d %H:%M:%S")

    if 'second' in date_str:
        second = int(date_str.split(' ')[0])
        date = timedelta(seconds=second)
        return (datetime.now() - date).strftime("%Y-%m-%d %H:%M:%S")

    # if Sept in string, replace it with Sep
    if 'Sept' in date_str:
        date_str = date_str.replace('Sept', 'Sep')

    date_obj = datetime.strptime(date_str, '%d %b %Y')
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")
