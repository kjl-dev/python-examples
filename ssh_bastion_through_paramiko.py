#!/usr/bin/python -u

# This is an example script that shows how to connect to a destination
# host through a jump/bastion host, utilizing the keys of the running SSH agent.
# local host --> bastion host --> destination host

import paramiko

# Bastion hostname/ip
BASTION_IP = "10.1.1.1"

# Destination hostname/ip
DESTINATION_IP = "10.50.1.1"

SSH_PORT = 22
SSH_USERNAME = "user"


def main():

  bastionAddr = (BASTION_IP, SSH_PORT)
  destAddr = (DESTINATION_IP, SSH_PORT)

  bastionHost = paramiko.SSHClient()
  bastionHost.set_missing_host_key_policy(paramiko.AutoAddPolicy())

  agent = paramiko.Agent()
  agent_keys = agent.get_keys()

  # Assumes you only have one key loaded on your SSH agent, easy to configure with Jenkins
  # but you would need to test each key if you had more than one
  bastionHost.connect(BASTION_IP, username=SSH_USERNAME, pkey=agent_keys[0])
  bastionTransport = bastionHost.get_transport()
  bastionChannel = bastionTransport.open_channel("direct-tcpip", destAddr, bastionAddr)

  destHost = paramiko.SSHClient()
  destHost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  destHost.connect(DESTINATION_IP, username=SSH_USERNAME, pkey=agent_keys[0], sock=bastionChannel)

  stdin, stdout, stderr = destHost.exec_command('ls -ltr /usr/bin')

  print(stderr.read())
  print(stdout.read())

  destHost.close()
  bastionHost.close()


main()
