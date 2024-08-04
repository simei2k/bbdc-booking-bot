from app import app
import schedule
import time
from config import load_config
from log_in import log_in
from checkwebpage import check_webpage

# load config
config = load_config("config.yaml")
interval = config["interval"]

# checking whether calendar elemnent can be viewed 
# if yes, proceed to check whether there are slots

def job():
    try:
        app(config)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    log_in(config)
    #click the instructor and proceed button
    time.sleep(3)
    job() 
    schedule.every(interval).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
