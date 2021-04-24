# Sabi
# Core Function

# Copyright 2021 Sabi
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.

import os, sys

version=1.41

def config_read(file_path):
    config_dict = {}
    with open(file_path, 'r') as cfile:
        for line in cfile.readlines():
            if line[0] == '#': # remove comments
                continue
            line = line.split('=')
            while line[0][-1] == ' ': # remove whitespace
                line[0] = line[0][:-1]
            while line[1][0] == ' ':
                line[1] = line[1][1:]
            config_dict[line[0]] = line[1]
    return config_dict # dictionary

def config_write(config_dict, file_path):
    with open(file_path, 'w') as cfile:
        for key_name in config_dict.keys():
            cfile.write(key_name + ' = ' + config_dict[key_name])

def set_config_value(key_name, key_value, config_dict):
    if key_name not in config_dict:
        config_dict[key_name] = key_value
    return config_dict

def key_check(key_name, dict_name):
    found = False
    if key_name in dict_name.keys():
        found = True
    return found

# Systems Tools

def clear_screen():
    if os.name != 'nt':
        os.system('cls')
    else:
        os.system('clear')

def linux_check():
    linux = False
    if sys.platform == 'linux':
        linux = True
    return linux

def linux_exit(msg='This feature is currently only compatible with Unix shells.'):
    if not linux_check():
        sys.exit(msg)

def sudocheck():
    sudo = False
    if os.geteuid() == 0:
        sudo = True
    return sudo

def sudoexit(msg='Please run with sudo/root'):
    if not sudocheck():
        sys.exit(msg)

def domainname(ip):
    linux_exit()
    nsname = bashout('nslookup ' + ip + ' | cut -d "=" -f 2 | cut -d " " -f 2 | head -1 | cut -d "." -f 1').read().strip()
    return nsname

def bashout(command):
    linux_exit()
    out = os.popen(command).read().strip()
    return out

# Sabi

def sabifs(software_name):
    sabi_path = '/opt/sabi/' + software_name
    if sudocheck():
        if linux_check():
            if not os.path.isdir(sabi_path):
                os.system('mkdir -p ' + sabi_path)

def this_file_location():
    return os.path.abspath(os.path.dirname(__file__))

def cwd(software_name, local_install=False):
    if linux_check() and not local_install:
        cwd = '/opt/sabi/' + software_name + '/'
    else:
        cwd = this_file_location() + '/'
    return cwd

def symlink(software_name):
    if linux_check():
        if not os.path.isfile('/usr/local/bin/' + software_name):
            os.system('ln -s /opt/sabi/' + software_name + '/' + software_name + '.py  /usr/local/bin/' + software_name)
        os.system('chmod 755 /usr/local/bin/' + software_name)
        os.system('chmod 755 /opt/sabi/' + software_name + '/' + software_name + '.py')

def arg_check(software_name):
    if len(sys.argv) < 2:
        sys.exit('You need an argument. "' + software_name + ' -h" for more information.')


# Commands

def cat(file_name):
    with open(file_name, 'r') as ifile:
        msg = ifile.read()
    sys.exit(msg)

def dircheck(dir_name):
    found = False
    if os.path.isdir(dir_name):
        found = True
    return found

def which(software):
    found = False
    linux_exit()
    if not os.system('which ' + software + ' > /dev/null 2>&1'):
        found = True
    return found
