# MKT-SSH-Automation
Tool to automate configuration on multiple routers Mikrotik via SSH

## Use

**FILE hosts**

Contains the host IP (one per line) of the routers to deploy commands.

**FILE commands**

Contains all the commands to execute in every host of hosts FILE.

The program reads the first line in the hosts FILE connects to it via SSH and execute every line in commands FILE, after execution of the command output is shown in console.
After it finishes with all the commands, reads the second line in the hosts FILE and repeats the process.

## Real life example

Supouse you have 10 routers and want to update all of them, you can add the 10 IPs to the hosts FILE and in the commands FILE add the following:

```bash
/system package update set channel=long-term 
/system package update install
```

Execute the program with:

```bash
python3 mikrotik-ssh.py
```

Enter the SSH port of your routers, the user and password to establish an SSH connection.

The program will connect to every switch and update its RouterOS to the last long-term version available.
