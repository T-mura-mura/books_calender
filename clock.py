from apscheduler.schedulers.background import BackgroundScheduler
import subprocess

sched = BackgroundScheduler()

@sched.scheduled_job('cron', hour=6, minute=35)
def scheduled_job():
    cmd = "python manage.py scraping_books"
    subprocess.call(cmd.split())

sched.start()

