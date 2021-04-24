#!/usr/bin/python3

# antsible - server utility
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

from flask import Flask
import antsible

version = '2.0'

app = Flask(__name__)

hosts_file = '/etc/ansible/hosts'

@app.route('/')
def hello():
    return '/hostname/group1+group2+group3\n'

@app.route('/<host>/<groups>')
def add_host(host, groups=None):
    hosts_dict = antsible.read_hosts()
    if groups != None:
        if '+' in groups:
            groups = groups.split('+')
            hosts_dict = antsible.add_host(host, groups, hosts_dict)
        else:
            hosts_dict = antsible.add_host(host, [groups], hosts_dict)
    antsible.write_hosts(hosts_dict, hosts_file)
    return 'antsible updated\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='11110', debug=True)
