from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour=4, minute=30)
# @sched.scheduled_job('interval', minutes=3)
def scheduled_job():
    cmd = "python manage.py scraping_books"
    subprocess.call(cmd.split())

sched.start()

