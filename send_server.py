import os
import logging
import requests
import sqlite3
from datetime import datetime
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError, HTTPError, RequestException
from dotenv import load_dotenv
from database.db import connect_cursor

load_dotenv()

API_URL = os.getenv("API_URL")
USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")  
PC_ID = os.getenv("PC_ID")

if not API_URL:
    raise RuntimeError("API URL not found!")

# time_format = "%Y-%m-%d %H:%M:%S"

# def format_dt(dt: datetime) -> str:
#     return dt.replace(microsecond=0).strftime(time_format)
    
session = requests.Session()
session.auth = HTTPBasicAuth(USERNAME, PASSWORD)

def mark_sent(row_id: int):
    connect, cursor =  connect_cursor()
    cursor.execute("UPDATE downtime_log SET status = 1 WHERE id = ?", (row_id,))
    connect.commit();connect.close()
    
def send_server(row: sqlite3.Row) -> bool:
    payload = {
        "pc_id": PC_ID,
        "shutdown_time": row["shutdown_time"],
        "startup_time": row["startup_time"],
        "downtime_min": row["downtime"]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        r = session.post(
            API_URL, 
            json=payload, 
            headers=headers, 
            timeout=10
            )
        r.raise_for_status()
        logging.info("OK downtime sent id=%s payload=%s", row["id"], payload)
        mark_sent(row["id"])
        return True
    except ConnectionError:
        logging.warning("Network error sending payload")
    except HTTPError as e:
        logging.error("HTTP %s error: %s", e.response.status_code, e)
    except RequestException as e:
        logging.error("Requests error: %s", e)
    except Exception as e:
        logging.exception("Unexpected error: %s", e)
    return False