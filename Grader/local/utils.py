#!/usr/bin/python
#
# This file is part of CSE 489/589 Grader.
#
# CSE 489/589 Grader is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# CSE 489/589 Grader is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with CSE 489/589 Grader. If not, see <http://www.gnu.org/licenses/>.
#

import sys
import os
import socket
import ConfigParser
import re
import random
import urllib

GRADING_SERVER_PORT = None
GRADING_SERVERS_HOSTNAME = []
GRADING_SERVERS_IP = []

def print_regular(text):
	print '\033[33m'+text+'\033[0m'
	sys.stdout.flush()

def get_grading_server_paths(config, student_type):
    grading_servers = [server[1] for server in config.items('GradingServerList')]
    grading_dir = os.path.join(config.get('GradingServer', 'dir-submission'), student_type)
    return [server+':'+grading_dir for server in grading_servers]

def resolveIP(fqdn):
    return socket.gethostbyname(fqdn)

def readConfiguration(config_file):
    global GRADING_SERVER_PORT, GRADING_SERVERS_HOSTNAME, GRADING_SERVERS_IP

    config = ConfigParser.SafeConfigParser()
    config.read(config_file.name)

    print_regular('Reading configuration file: '+'\033[0m'+config_file.name+'\033[0m'+' ...')

    GRADING_SERVERS_HOSTNAME = [server[1] for server in config.items('GradingServerList')]
    GRADING_SERVERS_IP = [resolveIP(server[1]) for server in config.items('GradingServerList')]

    config_file.close()
    return config

def extractOutputSuccess(command, log_output, mode='one'):
    pattern = '\['+command+':SUCCESS\]\\n(.*?)\['+command+':END\]\\n'
    if mode == 'one':
        matches = re.compile(pattern, re.DOTALL).search(log_output)

        if not matches: return None
        return matches.group(1)
    else:
        return re.findall(pattern, log_output, re.DOTALL)

def extractOutputError(command, log_output, mode='one'):
    pattern = '\['+command+':ERROR\]\\n(.*?)\['+command+':END\]\\n'
    if mode == 'one':
        matches = re.compile(pattern, re.DOTALL).search(log_output)

        if not matches: return None
        return matches.group(1)
    else:
        return re.findall(pattern, log_output, re.DOTALL)

def random_port():
    return random.randint(1000, 50000)

def doGET(URL, port, message):
    query_str = urllib.urlencode(message)
    return urllib.urlopen('http://'+URL+':'+str(port)+'?'+query_str).read()
