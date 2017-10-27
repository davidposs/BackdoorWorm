import nclib
import time
local_ip = "192.168.1.4"
LISTEN_PORT = 1234
logfile = open("badsystems.txt", "w")

data = []

while True:
    print "Listening..."
    try:
        nc = nclib.Netcat(listen=(local_ip, LISTEN_PORT), log_send=False, log_recv=logfile)
        data.append(nc.recv_all() + "\n")
        print data[-1]
    except KeyboardInterrupt:
        logfile.close()
    time.sleep(5)
