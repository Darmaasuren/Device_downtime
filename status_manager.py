from datetime import datetime
from database.db import (
    insert_startup_time,
    update_last_shutdown_time,
    get_last_shutdown_time
)

def log_start():
    startup_time = datetime.now()
    
    shutdown = get_last_shutdown_time()
    
    if shutdown:
        shutdown_time = datetime.strptime(shutdown, "%Y-%m-%d %H:%M:%S.%f")
        downtime = int((startup_time - shutdown_time).total_seconds()/60)
    else:
        downtime = 0
    
    insert_startup_time(startup_time, downtime)
    
def log_shutdown():
    shutdown_time = datetime.now()
    update_last_shutdown_time(shutdown_time)
    