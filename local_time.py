from datetime import datetime
from zoneinfo import ZoneInfo
import os


LOCAL_TZ = ZoneInfo("Asia/Ulaanbaatar")

def now_local():
    return datetime.now(LOCAL_TZ)