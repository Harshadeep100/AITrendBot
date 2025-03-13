import schedule
import time
import os

def run_ai_trendbot():
    os.system("python /path/to/ai_trendbot.py")

schedule.every().day.at("08:00").do(run_ai_trendbot)
schedule.every().day.at("20:00").do(run_ai_trendbot)

while True:
    schedule.run_pending()
    time.sleep(60)
