#!/usr/bin/python3

# antsible - Ansible Hosts File Management
# Sabi. Simple, Lightweight, but Not Beautiful

# Copyright 2021 Sabi
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.

import sabi
import os
import sys
import datetime
import shutil

version = '2.0'
software_name = 'antsible'

hosts_file = '/etc/ansible/hosts'

def help_menu():
    sys.exit('''
Antsible - Hosts File Management Server
Sabi. Simple, Lightweight, but Not Beautiful

To install: sudo python3 antsible.py install

To Use
Via Command Line:
    antsible host
    antsible host group1 group2 group3

Remotely via curl:
    curl http://server_ip:port_number/<host>/<group1+group2+group3>
    Ex: curl http://localhost:11110/ubuntu201/kubernetes+storage
''')

def read_hosts():
    hosts_dict = {'groupless':[],'groups':{}}
    group = ""

    with open(hosts_file, "r") as hfile:
        groupless = True
        for line in hfile.readlines():
            line = line.strip()
            if line == "" or line[0] == '#' or line == '\n':
                continue
            if line[0] == '[' and line[-1] == ']':
                groupless = False
                group = line[1:-1]
                if group not in hosts_dict['groups']:
                    hosts_dict['groups'][group] = []
            else:
                if groupless:
                    hosts_dict['groupless'].append(line)
                else:
                    hosts_dict['groups'][group].append(line)

    return hosts_dict

# This function is what actually writes the new hosts file
def write_hosts(hosts_dict, hosts_file):
    hosts_dict['groupless'].sort()
    for group in hosts_dict['groups']:
        hosts_dict['groups'][group].sort()
    with open(hosts_file, 'w') as hfile:
        if len(hosts_dict['groupless']) > 0:
            for host in hosts_dict['groupless']:
                hfile.write(host + '\n')
        if len(hosts_dict['groups']) > 0:
            first_entry = True
            for group in hosts_dict['groups']:
                if first_entry:
                    hfile.write('[' + group + ']\n')
                    first_entry = False
                else:
                    hfile.write('\n[' + group + ']\n')
                if len(hosts_dict['groups'][group]) > 0:
                    for host in hosts_dict['groups'][group]:
                        hfile.write(host + '\n')

def setup():
    cwd = sabi.this_file_location()
    if cwd != '/opt/sabi/' + software_name:
        shutil.move(cwd + '/antsible.py', '/opt/sabi/antsible/antsible.py')
        shutil.move(cwd + '/server.py', '/opt/sabi/antsible/server.py')
        shutil.move(cwd + '/sabi.py', '/opt/sabi/antsible/sabi.py')
    sabi.symlink(software_name)
    if not os.path.isfile('/usr/local/bin/ants'):
        os.system('ln -s /usr/local/bin/antsible /usr/local/bin/ants')

def add_host(host, groups, hosts_dict):
    hosts_dict = read_hosts()
    if len(groups) == 0:
        hosts_dict['groupless'].append(host)
    else:
        for group in groups:
            if group not in hosts_dict['groups']:
                hosts_dict['groups'][group] = []
            if host not in hosts_dict['groups'][group]:
                hosts_dict['groups'][group].append(host)
    return hosts_dict

def main():
    sabi.arg_check(software_name)
    if sys.argv[1] in ['-h','--help']:
        help_menu()
    sabi.linux_exit()
    sabi.sudoexit()
    if not sabi.which('ansible'):
        sys.exit('Please install Ansible')
    sabi.sabifs(software_name)
    setup()

    host = sys.argv[1]
    if host == 'install':
        sys.exit('Antsible installed correctly.\nSee antsible -h for usage.')

    groups = []
    if len(sys.argv) > 1:
        for group in sys.argv[2:]:
            groups.append(group)
    hosts_dict = read_hosts()

    hosts_dict = add_host(host, groups, hosts_dict)
    write_hosts(hosts_dict, hosts_file)

if __name__ == '__main__':
    main()
