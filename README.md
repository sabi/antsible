# antsible
Sabi. Simple, Lightweight, but Not Beautiful.

## What is it?
Automatic Ansible Hosts file management server

## Requirements
- Linux environment
- sudo/root permissions to do installation
- python3, flask, and gunicorn
  - `apt install python3 python3-pip`
  - `pip3 install flask gunicorn`
 
## Setup
- Download and extract this antsible directory
- `sudo python3 antsible.py install`
- (Optional) Consider creating a systemd service to start antsible at boot

## How to use
- Start server `gunicorn --bind 0.0.0.0:11110 -w 4 server.py`
- - From the command line: `ants host group1 group2`
- Remotely via curl:  `curl http://your_ansible_master_ip:11110/ansible_category/hostname_of_new_node`
- *Suggestion*: Consider appending `curl http://your_ansible_master_ip:11110/$1/$2` to your installation scripts so that you can keep your hosts file up to date as you build new servers.
