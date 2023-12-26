from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler(daemon=True)

sched.add_job(lambda : sched.print_jobs(),'interval',seconds=5)
sched.start()