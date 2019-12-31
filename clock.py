# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
# from hello.management.commands.scraping_books import Command

# sched = BackgroundScheduler()
sched = BlockingScheduler()

# @sched.scheduled_job('cron', hour=6, minute=35)
@sched.scheduled_job('interval', minutes=3)
def scheduled_job():
    cmd = "python manage.py scraping_books"
    subprocess.call(cmd.split())
    # Command.handle

sched.start()

