from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate
from serpapi import GoogleSearch
import json
from urllib.parse import (parse_qsl, urlsplit)
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
HOSTNAME = "13.212.232.71"
PORT = 3306
USERNAME = "serpApi"
PASSWORD = "CGpch5JKsSD4w6rP"
DATABASE = "serpapi"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"



db = SQLAlchemy(app)
migration = Migrate(app, db)
sched = BackgroundScheduler(daemon=True)  # scheduler
sched.start()
class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    snippet = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.Text, nullable=False)
    # keyword = db.Column(db.Text, nullable=False)
    # keyword_ids = db.Column(db.Integer, db.ForeignKey('keywords.id'))
    #
    # keywords = db.relationship('Keywords', back_populates='news')

# class Keywords(db.Model):
#     __tablename__ = 'keywords'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     keyword = db.Column(db.Text, nullable=False)
#
#     news = db.relationship('News', back_populates='keywords')



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


def prompt(task_id):
    print("Executing Task..."+str(task_id))

def search_news(keywords, time_limit):
    GoogleSearch.SERP_API_KEY = "39ffcd6e2c5819a50c7ceb95d2dcecec4f38960d1f065a0f33c848e1abf51da2"
    search = GoogleSearch({
        "q": keywords,  # search
        "tbm": "nws",  # news
        "tbs": time_limit, #"qdr:d",   last 24h
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
            db.session.add(news)
            db.session.commit()
            position_num += 1
        news_num += len(data['news_results'])
        page_num += 1

    print('page_num: '+str(page_num))
    print('news_num: '+str(news_num))

@app.route('/add_task', methods=['GET'])
def add_task():
    #keywords_input = request.args.get('keywords')
    #time_limit_input = request.args.get('time_limit')

    # input time
    year_input = request.args.get('year')
    month_input = request.args.get('month')
    day_input = request.args.get('day')
    hour_input = request.args.get('hour')
    minute_input = request.args.get('minute')
    second_input = request.args.get('second')

    # if input time is none then use default time
    if year_input is None:
        year_input = '*'
    if month_input is None:
        month_input = '*'
    if day_input is None:
        day_input = '*'
    if hour_input is None:
        hour_input = '*'
    if minute_input is None:
        minute_input = '*'
    if second_input is None:
        second_input = '*/5'

    try:
        sched.add_job(search_keyword, 'cron',
                      year=year_input, month=month_input, day=day_input,
                      hour=hour_input, minute=minute_input, second=second_input)
        return 'Task added: search' #+ keywords_input + ' ' + time_limit_input, 200
    except Exception as e:
        return 'Error adding task: ' + str(e), 500

@app.route('/list_jobs')
def list_jobs():
    jobs = sched.get_jobs()
    jobs_info = [{"id": job.id, "next_run_time": str(job.next_run_time)} for job in jobs]
    return jsonify(jobs_info)

@app.route('/search')
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
                db.session.add(news)
                db.session.commit()
                position_num += 1
            news_num += len(data['news_results'])
            page_num += 1

        print('page_num'+str(page_num))

        return 'number of news: ' + str(news_num)




if __name__ == '__main__':

    app.run()
