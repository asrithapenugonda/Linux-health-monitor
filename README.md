# Linux System Health Monitor

A lightweight Python monitoring tool that tracks CPU, memory, and disk usage
on a Linux server and sends email alerts when configurable thresholds are breached.

---

## What it does

- Monitors CPU, memory, and disk usage every 60 seconds
- Sends email alerts when any metric exceeds its threshold
- Logs all metrics with timestamps to a local log file
- Reports top 5 CPU consuming processes on every check

---

## Project Structure
```
linux-health-monitor/
├── config.py          # all settings and thresholds
├── alert.py           # email alert logic
├── monitor.py         # main monitoring loop
├── requirements.txt   # dependencies
└── README.md          # this file
```

---

## Tech Used

- Python 3.9
- psutil library
- Linux /proc filesystem
- smtplib (Python standard library)
- logging (Python standard library)

---

## How to Run

**1. Clone the repo**
```
git clone https://github.com/asrithapenugonda/Linux-health-monitor.git
cd Linux-health-monitor
```

**2. Install dependencies**
```
pip install -r requirements.txt
```

**3. Set environment variables**
```
# Windows
$env:EMAIL_SENDER = "youremail@gmail.com"
$env:EMAIL_PASSWORD = "your-gmail-app-password"

# Linux
export EMAIL_SENDER="youremail@gmail.com"
export EMAIL_PASSWORD="your-gmail-app-password"
```

**4. Run the monitor**
```
python monitor.py
```

---

## Configuration

All thresholds are set in `config.py`

| Setting | Default | Description |
|---|---|---|
| CPU_THRESHOLD | 80% | Alert if CPU exceeds this |
| MEMORY_THRESHOLD | 85% | Alert if memory exceeds this |
| DISK_THRESHOLD | 90% | Alert if disk exceeds this |
| CHECK_INTERVAL | 60 | Seconds between each check |

---

## Sample Output
```
2026-03-10 16:54:05 - INFO - === Health Monitor Started ===
2026-03-10 16:54:05 - INFO - Thresholds — CPU: 80% | Memory: 85% | Disk: 90%
2026-03-10 16:54:05 - INFO - --- Running health check ---
2026-03-10 16:54:05 - INFO - CPU Usage: 18.3% [OK]
2026-03-10 16:54:05 - INFO - Memory: 62.1% [OK]
2026-03-10 16:54:05 - INFO - Disk: 44.8% [OK]
2026-03-10 16:54:05 - INFO - Top 5 processes by CPU:
2026-03-10 16:54:05 - INFO -   PID 10480 — chrome.exe — 7.6%
2026-03-10 16:54:05 - INFO -   PID 20248 — idea64.exe — 6.2%
```

---

## What I Learned

- How Linux exposes system data through the /proc filesystem
- Difference between free memory and available memory
- How monitoring tools collect metrics using polling intervals
- Separating configuration from logic using environment variables
- Structured logging with timestamps using Python logging module
- Deploying and running a script as a background service on AWS EC2

---