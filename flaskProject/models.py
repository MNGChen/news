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
