import os
from dotenv import load_dotenv
import telegram
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

load_dotenv(verbose=True)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telegram.Bot(TELEGRAM_TOKEN)
url = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0013&date="
date = "20211108"

url = url + date


def job_func():
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    imax = soup.select_one('span.imax')
    response_date = soup.select_one('div.day')
    month = response_date.select_one('span').text.strip()
    month = month[:-1]
    day = response_date.select_one('strong').text.strip()
    res_date = "2021" + month + day
    if(res_date == date):
        if(imax):
            imax = imax.find_parent('div', class_='col-times')
            title = imax.select_one('div.info-movie > a > strong').text.strip()
            bot.sendMessage(chat_id=CHANNEL_ID,
                            text=title + " IMAX 예매가 열렸습니다.")
            sched.pause()
    else:
        bot.sendMessage(chat_id=CHANNEL_ID,
                            text="IMAX 예매가 열리지 않았습니다.")


sched = BlockingScheduler()
sched.add_job(job_func, 'interval', seconds=30)
sched.start()
