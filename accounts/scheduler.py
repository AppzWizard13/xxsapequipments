from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
import atexit
import requests

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# List of URLs to self-ping
PING_URLS = [
    'https://codespikestudio.onrender.com/',
    'https://iron-suite.onrender.com/'
]

def self_ping():
    """
    Sends a GET request to each URL in the PING_URLS list to keep them awake.
    """
    for url in PING_URLS:
        try:
            response = requests.get(url)
            print(f"Pinging URL: {url}")
            if response.status_code == 200:
                logger.info(f"Self-ping successful: {url}")
            else:
                logger.warning(f"Self-ping failed for {url} with status code {response.status_code}")
        except Exception as e:
            logger.error(f"Error during self-ping for {url}: {e}")

def start():
    """
    Starts the background scheduler that pings the URLs periodically.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(self_ping, IntervalTrigger(seconds=15))  # Ping every 15 seconds
    scheduler.start()
    logger.info("Scheduler started.")

    # Ensure scheduler shuts down properly on exit
    atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    start()
