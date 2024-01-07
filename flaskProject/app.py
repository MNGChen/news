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

# Create and start the scheduler
sched = BackgroundScheduler(daemon=True)
sched.start()

# Save the scheduler in the app context
app.scheduler = sched

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
