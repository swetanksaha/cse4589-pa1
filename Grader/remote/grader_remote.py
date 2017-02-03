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

__author__ = "Swetank Kumar Saha (swetankk@buffalo.edu)"
__copyright__ = "Copyright (C) 2017 Swetank Kumar Saha"
__license__ = "GNU GPL"
__version__ = "1.0"

import sys
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import urlparse
import argparse
import os

from test_cases import *
from utils import read_logfile

parser = argparse.ArgumentParser(description='CSE 489/589 Grader Remote v'+__version__)

requiredArgs = parser.add_argument_group('required named arguments')
requiredArgs.add_argument('-p', '--port', dest='port', type=int, nargs=1, help='server port', required=True)

def test_runner(action, binary, args):

    if action == 'COMMAND':
        response = grade_app_startup(binary)

    if action == 'LOGFILE':
        response = read_logfile(binary, args[0])

    if action == 'STARTUP':
        response = grade_startup(binary, args[0], args[1])

    if action == 'AUTHOR':
        response = grade_author(binary, args[0], args[1])

    if action == 'IP':
        response = grade_ip(binary, args[0], args[1])

    if action == 'PORT':
        response = grade_port(binary, args[0], args[1])

    if action == 'LIST':
        response = grade_list(binary, *args)

    if action == 'REFRESH':
        response = grade_refresh(binary, args[0], args[1], args[2], args[3])

    if action == 'SEND':
        response = grade_send(binary, *args)

    if action == 'SSEND':
        response = ssend(binary, args[0], args[1], args[2], args[3], args[4])

    if action == 'BROADCAST':
        response = grade_broadcast(binary, args[0], args[1], args[2], args[3], args[4], args[5])

    if action == 'BLOCK':
        response = grade_block(binary, args[0], args[1], args[2], args[3], args[4])

    if action == 'SBLOCK':
        response = sblock(binary, args[0], args[1], args[2], args[3], args[4], args[5])

    if action == 'BBLOCK':
        response = bblock(binary, args[0], args[1], args[2], args[3], args[4])

    if action == 'BLOCKED':
        response = grade_blocked(binary, *args)

    if action == 'ABLOCKED':
        response = ablocked(binary, *args)

    if action == 'UNBLOCK':
        response = grade_unblock(binary, *args)

    if action == 'UUNBLOCK':
        response = uunblock(binary, *args)

    if action == 'LOGOUT':
        response = grade_logout(binary, *args)

    if action == 'BUFFER':
        response = grade_buffer(binary, *args)

    if action == 'SBUFFER':
        response = sbuffer(binary, *args)

    if action == 'EXIT':
        response = grade_exit(binary, *args)

    if action == 'STATISTICS':
        response = grade_statistics(binary, *args)

    if action == 'EXCEPTION-LOGIN':
        response = grade_exception_login(binary, *args)

    if action == 'EXCEPTION-SEND':
        response = grade_exception_send(binary, *args)

    if action == 'EXCEPTION-BLOCK':
        response = grade_exception_block(binary, *args)

    if action == 'EXCEPTION-UNBLOCK':
        response = grade_exception_unblock(binary, *args)

    if action == 'EXCEPTION-BLOCKED':
        response = grade_exception_blocked(binary, *args)

    if action == 'BONUS':
        response = grade_bonus(binary, *args)

    if action == 'SBONUS':
        response = sbonus(binary, *args)

    if action == 'CBONUS':
        response = cbonus(binary, *args)

    return str(response)

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        message = urlparse.parse_qs(parsed.query)

        action = message.get('action')[0]
        binary = message.get('binary')[0]
        nargs = int(message.get('nargs')[0])
        args = [message.get('arg'+str(argc))[0] for argc in range(nargs)]

        self.send_response(200)
        self.end_headers()
        self.wfile.write(test_runner(action, binary, args))
        self.wfile.close()
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':
    args = parser.parse_args()
    port = args.port[0]

    # Kill existing process (if any)
    os.system("kill -9 $(netstat -tpal | grep :%s | awk '{print $NF}' | cut -d/ -f1) > /dev/null 2>&1" % (port))

    server = ThreadedHTTPServer(('0.0.0.0', port), GetHandler)
    print 'Starting grading server ...'
    server.serve_forever()
