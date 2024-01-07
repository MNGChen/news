import datetime
import time
import pandas as pd
from config import Config
from controllers import search_news, search_keyword
from flask import Blueprint, request, jsonify, current_app
from models import db, News
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl

routes = Blueprint('routes', __name__)


@routes.route('/')
def hello_world():
    return 'Hello World!'


@routes.route('/add_task', methods=['GET'])
def add_task():
    keywords_input = request.args.get('keywords')
    task_id_input = request.args.get('task_id')
    filter_input = request.args.get('filter')
    nfpr_input = request.args.get('nfpr')
    safe_input = request.args.get('safe')
    location_input = request.args.get('location')
    gl_input = request.args.get('gl')
    lr_input = request.args.get('lr')
    no_cache_input = request.args.get('no_cache')
    tbs_input = request.args.get('tbs')

    # input time
    year_input = request.args.get('year')
    month_input = request.args.get('month')
    day_input = request.args.get('day')
    hour_input = request.args.get('hour')
    minute_input = request.args.get('minute')
    second_input = request.args.get('second')
    keyword_id_input = request.args.get('keyword_id')
    dept_belong_id_input = request.args.get('dept_belong_id')

    # if input time is none then use default time
    # Accurate time by giving value to each parameter
    # * means every
    # sample input: month_input = '6-8,11-12'
    #                day_input = 'last fri' '3rd fri'
    if year_input is None or year_input == '':
        year_input = '*'
    if month_input is None or month_input == '':
        month_input = '*'
    if day_input is None or day_input == '':
        day_input = '*'
    if hour_input is None or hour_input == '':
        hour_input = '*'
    if minute_input is None or minute_input == '':
        minute_input = '*'
    if second_input is None or second_input == '':
        second_input = '*/5'

    try:
        scheduler = current_app.scheduler
        scheduler.add_job(search_news, 'cron',
                            args=[keywords_input,
                                  filter_input,
                                  nfpr_input,
                                  safe_input,
                                  location_input,
                                  gl_input,
                                  lr_input,
                                  no_cache_input,
                                  tbs_input,
                                  task_id_input,
                                  keyword_id_input,
                                  dept_belong_id_input],
                            year=year_input, month=month_input, day_of_week=day_input,
                            hour=hour_input, minute=minute_input, second=second_input)

        # sched.add_job(search_keyword, 'cron',
        #               year=year_input, month=month_input, day=day_input,
        #               hour=hour_input, minute=minute_input, second=second_input)
        # return 'Task added: search'  # + keywords_input + ' ' + time_limit_input, 200
        return 'Task added: search' + keywords_input
    except Exception as e:
        return 'Error adding task: ' + str(e), 500


@routes.route('/list_jobs')
def list_jobs():
    scheduler = current_app.scheduler
    jobs = scheduler.get_jobs()
    jobs_info = [{"id": job.id, "next_run_time": str(job.next_run_time)} for job in jobs]
    return jsonify(jobs_info)


@routes.route('/search')
def search_keyword():
    with current_app.app_context():
        GoogleSearch.SERP_API_KEY = Config.SERP_API_KEY
        search = GoogleSearch({
            "q": "usa",  # search
            "tbm": "nws",  # news
            "tbs": "qdr:d",  # last 24h
            "num": "100",  # number of news
        })
        data = search.get_dict()
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
                news_upload.date = data['news_results'][position_num]['date']
                news_upload.snippet = data['news_results'][position_num]['snippet']
                news_upload.thumbnail = data['news_results'][position_num]['thumbnail']
                #news_upload.task_id = task_id_input
                #news_upload.keyword_id = keyword_id_input
                #news_upload.dept_belong_id = dept_belong_id_input
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
                    news_upload.date = data['news_results'][position_num]['date']
                    news_upload.snippet = data['news_results'][position_num]['snippet']
                    news_upload.thumbnail = data['news_results'][position_num]['thumbnail']
                    #news_upload.task_id = task_id_input
                    #news_upload.keyword_id = keyword_id_input
                    #news_upload.dept_belong_id = dept_belong_id_input
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

        print('page_num' + str(page_num))
        print('news_num' + str(news_num))
        print('reject_num' + str(reject_num))

        return 'number of news: ' + str(news_num)
