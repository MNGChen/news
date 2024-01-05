from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    snippet = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.Text, nullable=False)
    task_id = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer, nullable=False)
    keyword_id = db.Column(db.Integer, nullable=True)
    dept_belong_id = db.Column(db.Integer, nullable=True)


class News_log(db.Model):
    __tablename__ = 'dvadmin_task_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serpapi_id = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    json_endpoint = db.Column(db.Text, nullable=False)
    google_url = db.Column(db.Text, nullable=False)
    raw_html_file = db.Column(db.Text, nullable=False)
    search_parameters = db.Column(db.Text, nullable=False)
    error_message = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.Integer, nullable=False)
    task_id = db.Column(db.Integer, nullable=False)
