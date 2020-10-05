#!/usr/bin/python3

# antsible
# Sabi. Simple, Lightweight, but Not Beautiful

# See LICENSE for a copy of the MIT License
# that should be distributed with this software

# For more check out https://github.com/sabi

import os, sys

version = 1.0

# This is the path of the hosts file
hostsFile = "/tmp/hosts"

# This function reads the old hosts and adds each as a key:value pair
# as server group:list of servers
def readOldHosts():
    bigDict = {}
    currentCategory = ""
    with open(hostsFile, "r") as hfile:
        data = hfile.read().splitlines()
    for line in data:
        if line != "" and line[0] == "[":
            currentCategory = line
            bigDict[line] = []
        elif line != "":
            bigDict[currentCategory].append(line)
    return bigDict

# This function is what actually writes the new hosts file
def writeHosts(bigDict):
    categories = list(bigDict.keys())
    categories.sort()
    with open(hostsFile, "w") as hfile:
        for group in categories:
            hfile.write(group + "\n")
            hosts = list(bigDict[group])
            hosts.sort()
            for server in hosts:
                hfile.write(server + "\n")
            hfile.write("\n")


# Start Program

# Argument Handling
if len(sys.argv) > 1:
    if sys.argv[1] in ["-h","--help"]:
        sys.exit("python3 antsible.py name_of_host category_for_hosts_file\n-v --version : Print the version")
    if sys.argv[1] in ["-v","--version"]:
        sys.exit(version)
elif len(sys.argv) != 3:
    sys.exit("You must have two arguments.\npython3 antsible.py name_of_host category_for_hosts_file")

# Ensure the hostsFile is set
if hostsFile == "W00T":
    sys.exit("Change the path of your hosts file in the top of this script.")

# Build the dictionary used to write hosts file
newhost = sys.argv[1]
category = sys.argv[2]
bigDict = readOldHosts()

# Check for multi Ansible categories in request
if "+" in category:
    categories = category.split("+")
    for cat in categories:
        if cat[0] != '[':
            cat = '[' + cat
        if cat[-1] != ']':
            cat = cat + ']'
        if cat not in bigDict.keys():
            bigDict[cat] = []
            print('Heads up, that was a new category')
        if newhost not in bigDict[cat]:
            bigDict[cat].append(newhost)

# If single Ansible category is requested
else:
    if category[0] != '[':
        category = '[' + category
    if category[-1] != ']':
        category = category + ']'
    if category not in bigDict.keys():
        bigDict[category] = []
        print('Heads up, that was a new category')
    if newhost not in bigDict[category]:
        bigDict[category].append(newhost)

# Finalize
writeHosts(bigDict)
print("Hosts file has been updated")
