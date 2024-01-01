from flask import Flask
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
from models import db
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migration = Migrate(app, db)
sched = BackgroundScheduler(daemon=True)
sched.start()
app.register_blueprint(routes)

if __name__ == '__main__':
    Debug = True
    app.run()
