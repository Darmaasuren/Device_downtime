import logging
from datetime import datetime
from database.db import (
    insert_startup_time,
    update_last_shutdown_time,
    get_last_shutdown_time,
    insert_shutdown_time,
    get_last_complete
)
from send_server import send_server

def log_start():
    startup_time = datetime.now()
    
    shutdown = get_last_shutdown_time()
    
    if shutdown:
        shutdown_time = datetime.strptime(shutdown, "%Y-%m-%d %H:%M:%S")
        downtime = int((startup_time - shutdown_time).total_seconds()//60)
    else:
        downtime = 0
    
    insert_startup_time(startup_time, downtime)
    insert_shutdown_time(startup_time)
    
    result_row = get_last_complete()
    if(result_row):
        ok = send_server(result_row)
        logging.info("payload delivered: %s", ok)
    
def update_shutdown():
    now = datetime.now()
    update_last_shutdown_time(now)
    logging.info("Updated shutdown time %s", now.strftime("%Y-%m-%d %H:%M:%S"))
    
def log_shutdown():
    shutdown_time = datetime.now()
    update_last_shutdown_time(shutdown_time)
    logging.info("Inserted shutdown time %s", shutdown_time.strftime("%Y-%m-%d %H:%M:%S"))