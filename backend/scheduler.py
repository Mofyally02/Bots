from apscheduler.schedulers.background import BackgroundScheduler
import time
import subprocess

# Function to run sender.py
def run_sender():
    print("Running sender.py to process messages...")
    subprocess.run(["python", "backend/sender.py"])

# Initialize scheduler
scheduler = BackgroundScheduler()

# Schedule sender.py to run every 10 minutes
scheduler.add_job(run_sender, "interval", minutes=10)

# Start scheduler
scheduler.start()

print("Scheduler is running... Press Ctrl+C to exit.")

# Keep script running
try:
    while True:
        time.sleep(60)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler stopped.")
