import logging
import time
import signal
import sys
from database.db import init_db
from status_manager import log_start, log_shutdown, update_shutdown

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def shutdown_handler(signum, frame):
    log_shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


if __name__ == "__main__":
    
    init_db()
    log_start()
    
    try:
        while True:
            logging.debug("System running...")
            update_shutdown()
            time.sleep(60)
    except Exception as e:
        print(f"ERROR, {e}")
        log_shutdown()
        sys.exit(1)