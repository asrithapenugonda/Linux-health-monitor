#config file

import os
#thresholds

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 85
DISK_THRESHOLD = 90

#Timing
CHECK_INTERVAL = 60
LOG_FILE = "health.log"

#email read from environment variable
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_RECEIVER = "asrithajyakumar@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

#safety check warnings
if not EMAIL_SENDER:
    print("warning: EMAIL_SENDER environment variable not set.")
if not EMAIL_PASSWORD:
    print("warning: EMAIL_PASSWORD environment variable not set")

