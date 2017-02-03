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

import socket
import urllib
import urllib2
import sys

import utils

def msg_to_payload(message):
    payload = {}
    payload['action'] = message[0]
    payload['binary'] = message[1]
    payload['nargs'] = str(len(message) - 2)
    argc = 0
    for arg in message[2:]:
        payload['arg'+str(argc)] = arg
        argc += 1

    return payload

def run_on_server(server, message):
    payload = msg_to_payload(message)
    query_str = urllib.urlencode(payload)

    response = urllib.urlopen('http://'+server+':'+str(utils.GRADING_SERVER_PORT)+'?'+query_str).read()
    return response

def run_on_servers(message):
    payload = msg_to_payload(message)
    query_str = urllib.urlencode(payload)

    response = [urllib.urlopen('http://'+server+':'+str(utils.GRADING_SERVER_PORT)+'?'+query_str).read() for server in utils.GRADING_SERVERS_HOSTNAME]
    return response
