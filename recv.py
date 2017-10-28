""" Listens on port 1234 for connections from other computers, which will send a message
    containing their IP address, then writes them to a file """
import nclib
import time

""" THIS VERSION WORKS """

def main():
    """ Infnite loop until user hits ctrl+c, waits for IPs to be sent """
    local_ip = "192.168.1.4"
    port = 1234
    file_name = "badsystems.txt"
    logfile = open(file_name, "w")
    data = []
    print "Listening, printing data to badsystems.txt"
    while True:
        try:
            nc = nclib.Netcat(listen=(local_ip, port), log_send=False, log_recv=logfile)
            data.append(nc.recv())
            time.sleep(5)
            nc.close()
            print "recevied " + data[-1]
        except KeyboardInterrupt as quit:
            print "... stopped"
            logfile.close()
            return

    logfile.close()


if __name__ == "__main__":
    main()

