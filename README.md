# antsible
Sabi. Simple, Lightweight, but Not Beautiful.

## What is it?
Automatic Ansible Hosts file management server.  A server listens on your Ansible master node. Through GET requests it updates the main Ansible Hosts file to update new nodes added to your cluster.  Multiple categories can be added at once. 

## Requirements
- Linux environment
- sudo/root permissions to do installation
- python3, flask, and gunicorn
  - `apt install python3 python3-pip`
  - `pip3 install flask gunicorn`
 
## Setup
- Download and extract this antsible directory
- Copy the hosts file generator to your PATH
  - `# cp antsible.py /usr/local/bin`
- Create an easy to call symlink
  - `# ln -s /usr/local/bin/antsible.py /usr/local/bin/ants`
- (Optional) Consider creating a systemd service to start antsible at boot
- Edit the `hostsFile` variable in `antsible.py`.  This should be the path of your Ansible hosts file.

## How to use
- Start server `gunicorn --bind 0.0.0.0:11110 -w 4 server.py`
- Anytime you need to add a new host to your Ansible hosts file.  `curl http://your_ansible_master_ip:11110/ansible_category/hostname_of_new_node`
- *Suggestion*: Consider appending `curl http://your_ansible_master_ip:11110/$1/$2` to your installation scripts so that you can keep your hosts file up to date as you build new servers.
