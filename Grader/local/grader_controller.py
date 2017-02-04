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

import argparse
import sys
import os
import subprocess
import time

import utils

parser = argparse.ArgumentParser(description='CSE 489/589 Grader Controller v'+__version__)

requiredArgs = parser.add_argument_group('required named arguments')
requiredArgs.add_argument('-c', '--config', dest='config', type=argparse.FileType('r'), nargs=1, help='configuration file', required=True)
requiredArgs.add_argument('-s', '--student', dest='student', type=str, nargs=1 , help='path to assignment folder: e.g. CSE489/jane_doe', required=True)
requiredArgs.add_argument('-t', '--test', dest='test', type=str, nargs=1, help='test name', required=True)

if __name__ == '__main__':
    args = parser.parse_args()

    cfg = utils.readConfiguration(args.config[0])

    utils.print_regular('Initializing grading servers ...')
    remote = subprocess.Popen(['./init_remote_grader.sh', ','.join(utils.GRADING_SERVERS_HOSTNAME), cfg.get('GradingServer', 'dir-grader'),
                    cfg.get('GradingServer', 'path-python'), str(utils.GRADING_SERVER_PORT), cfg.get('SSH', 'user'), cfg.get('SSH', 'id')])

    # Wait for all servers to init.
    time.sleep(3)

    binary = os.path.join(*[cfg.get('GradingServer', 'dir-local'), args.student[0], cfg.get('Grader', 'binary')])
    test_name = args.test[0]

    import pa1_grader
    getattr(pa1_grader, test_name)(binary)

    remote.kill()
