import nclib

# Who e want to send to
target_host = "192.168.1.4"
nc = nclib.Netcat((target_host, 1234))
nc.send("hey there!")
