#!usr/bin/python

import socket
import sys
import time
import getpass

# function that retrieves a timestamp for log propouses
def time_stamp():
    t = time.strftime("%Y-%m-%d %H:%M:%S")
    return t

# try to install paramiko, if is not installed raises an error
try:
    import paramiko

except ImportError:
    sys.tracebacklimit = 0
    with open("error.log", "a") as e:
        e.write(time_stamp() + " \"Paramiko\" module missing! Please visit http://www.paramiko.org/installing.html for more details.\n")
    e.close()
    raise ImportError("\rPlease install \"paramiko\" module! Visit http://www.paramiko.org/installing.html for more details.\r\n")

# try to open file hosts, if file is not accessible or inexistent the program closes
try:
    f = open("hosts", "r")
except IOError:
    sys.tracebacklimit = 0
    print("\nFile \"hosts\" does not exist or is not accessible.\n")
    quit()


# prompt user to enter SSH port, username and password
port_SSH = input("Enter SSH port: ")
mt_username = input("Enter username: ")
if sys.stdin.isatty():
    mt_password = getpass.getpass("Enter password: ")
else:
    mt_password = sys.stdin.readline().rstrip()

# establishes a 5 second timeout to make a ssh conection
timeout = 5
# cont for hosts
nlines = 0

# for host in hosts (file)
for line in f:
    # try to open file commands, if file is not accessible or inexistent the program closes
    try:
        k = open("commands", "r")
    except IOError:
        sys.tracebacklimit = 0
        print("\nFile \"commands\" does not exist or is not accessible.\n")
        quit()

    nlines += 1
    # grab next host from hosts file
    host = line.rstrip("\n")

    # create a new object that is gonna handle the ssh connection, if the key from that host is not known, automatically adds it to known_hosts file
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("\r\n########################################## Connecting to " + str(nlines) + ". host: " + host + " ##########################################\r\n")

    # try to make the ssh connection
    try:
        ssh.connect(host, username=mt_username, password=mt_password, timeout=timeout, look_for_keys=False,port=port_SSH)

    # error handlers
    except socket.timeout as e:
        print("Connection timeout. Log entry created.")
        with open("error.log", "a") as e:
            e.write(time_stamp() + " " + host + " Timeout connecting to the device.\n")
        e.close()
        continue

    except paramiko.AuthenticationException:
        print("Wrong credentials. Log entry created.")
        with open("error.log", "a") as e:
            e.write(time_stamp() + " " + host + " Wrong credentials.\n")
        e.close()
        continue

    except:
        print("Error connecting to the device. Log entry created.")
        with open("error.log", "a") as e:
            e.write(time_stamp() + " " + host + " Unknown error while connecting to the device.\n")
        e.close()
        continue

    print("Succsessfully connected to the host. Executing commands from the external file:\r\n")

    # for command in commands file
    for line in k:
        # take the command
        line = line.rstrip("\n")
        if line.startswith("#"):
            print("Line", line, "skipped")
        else:
            mt_command = line
        # Adding 200ms delay between commands
        time.sleep(.2)
        # execute the command
        stdin, stdout, stderr = ssh.exec_command(mt_command)
        print(mt_command)
        # prints the output
        print(stdout.read().decode())

    print("\nExternal commands are executed successfully.")
    # if all commands were correctly executed, logs a success entry in log
    with open("success.log", "a") as s:
        s.write(time_stamp() + " " + host + " Successfully executed commands on the host.\n")

    s.close()
    k.close()
    ssh.get_transport().close()
    ssh.close()

    print("Programa Finalizado...") 

if nlines == 0:
    print("\nList of hosts is empty.\n")

f.close()
quit()
