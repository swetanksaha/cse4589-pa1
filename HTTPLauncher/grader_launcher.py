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

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import urlparse
import argparse
import os
import cgi
import tarfile
import subprocess

parser = argparse.ArgumentParser(description='CSE 489/589 Grader Launcher v'+__version__)

requiredArgs = parser.add_argument_group('required named arguments')
requiredArgs.add_argument('-p', '--port', dest='port', type=int, nargs=1, help='server port', required=True)
requiredArgs.add_argument('-u', '--upload-dir', dest='upload_dir', type=str, nargs=1, help='upload directory', required=True)
requiredArgs.add_argument('-g', '--grade-dir', dest='grading_dir', type=str, nargs=1, help='grading directory', required=True)

def upload_file(submit_file):
    file_name = submit_file.filename
    file_data = submit_file.file.read()

    with open(os.path.join(udir, file_name), 'w') as submission:
        submission.write(file_data)

    del file_data

def build_submission(filename):
    student_dir = os.path.join(gdir, os.path.splitext(filename)[0])
    if not os.path.exists(student_dir): os.makedirs(student_dir)

    tar = tarfile.open(os.path.join(udir, filename))
    tar.extractall(path=student_dir)
    tar.close()

    os.system('cd %s && make clean && make' % (student_dir))

def init_grading_server(remote_grader_path, python, port):
    subprocess.Popen('cd %s;%s grader_remote.py -p %s' % (remote_grader_path, python, port), shell=True)

class HTTPHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        message = urlparse.parse_qs(parsed.query)

        action = message.get('action')[0]
        response = 'OK'

        if action == 'build':
            tarball = message.get('tarball')[0]
            build_submission(tarball)

        if action == 'init':
            remote_grader_path = message.get('remote_grader_path')[0]
            python = message.get('python')[0]
            port = message.get('port')[0]
            init_grading_server(remote_grader_path, python, port)

        if action == 'get-gdir':
            response = gdir

        self.send_response(200)
        self.end_headers()
        self.wfile.write(response)
        self.wfile.close()
        return

    def do_POST(self):
        parsed = cgi.FieldStorage(fp=self.rfile, headers=self.headers,
                                environ={'REQUEST_METHOD':'POST',
                                         'CONTENT_TYPE': self.headers['Content-Type'],
                                        })

        submit_file = parsed['submit']
        upload_file(submit_file)

        self.send_response(200)
        self.end_headers()
        self.wfile.write('OK')
        self.wfile.close()
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':
    args = parser.parse_args()

    port = args.port[0]
    udir = args.upload_dir[0]
    gdir = args.grading_dir[0]

    # Kill existing process (if any)
    os.system("kill -9 $(netstat -tpal | grep :%s | awk '{print $NF}' | cut -d/ -f1) > /dev/null 2>&1" % (port))

    server = ThreadedHTTPServer(('0.0.0.0', port), HTTPHandler)
    server.serve_forever()
