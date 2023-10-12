import subprocess
import time


server_script = "AS.py"  # Replace with the actual name of your server script
restart_delay = 5  # Number of seconds to wait before restarting the server

while True:
    print(f"Running {server_script}...")
    process = subprocess.Popen(["python", server_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()  # Wait for the server script to finish
    print(f"{server_script} has stopped. Restarting in {restart_delay} seconds...")
    time.sleep(restart_delay)
