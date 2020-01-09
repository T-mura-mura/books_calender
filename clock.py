from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=5)
def timed_job():
  cmd = "curl https://books-date.herokuapp.com/"
  subprocess.call(cmd.split())

@sched.scheduled_job('cron', hour=8)
def scheduled_job():
  cmd = "python manage.py scraping_books"
  subprocess.call(cmd.split())

sched.start()

