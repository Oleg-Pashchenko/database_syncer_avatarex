import schedule
import time
from syncer import sync


schedule.every().day.at("12:00").do(sync)
schedule.every().day.at("00:00").do(sync)

while True:
    schedule.run_pending()
    time.sleep(1)
