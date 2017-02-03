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

import subprocess
import os
import time
import ast

from utils import *

def grade_startup(binary, s_or_c, port):
    command = binary+" "+s_or_c+" "+str(port)
    process = subprocess.Popen(command, shell=True, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
    time.sleep(2)
    status = procStatus(process.pid)
    if status == 'R' or status == 'S':
        kill(process.pid)
        return True
    else:
        return False

def grade_author(binary, s_or_c, port):
    command = "expect -f author.exp "+binary+" "+s_or_c+" "+str(port)
    process = subprocess.Popen(command, shell=True, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)

    time.sleep(3)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_ip(binary, s_or_c, port):
    command = "expect -f ip.exp "+binary+" "+s_or_c+" "+str(port)
    process = subprocess.Popen(command, shell=True)

    time.sleep(2)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_port(binary, s_or_c, port):
    command = "expect -f port.exp "+binary+" "+s_or_c+" "+str(port)
    process = subprocess.Popen(command, shell=True, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)

    time.sleep(2)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_list(binary, s_or_c, port, s_ip="", s_port=""):
    if s_or_c == 's': command = "expect -f list_server.exp "+binary+" "+s_or_c+" "+str(port)
    else: command = "expect -f list_client.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port
    process = subprocess.Popen(command, shell=True, close_fds=True)

    if s_or_c == 's': time.sleep(15)
    else: time.sleep(2)

    return read_logfile(binary, port)

def grade_refresh(binary, s_or_c, port, s_ip, s_port):
    command = "expect -f refresh_client.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port
    process = subprocess.Popen(command, shell=True)

    time.sleep(8)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_send(binary, s_or_c, port, s_ip="", s_port=""):
    if s_or_c == 's': command = "expect -f send_server.exp "+binary+" "+s_or_c+" "+str(port)
    else: command = "expect -f send_client_r.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port
    process = subprocess.Popen(command, shell=True)

    time.sleep(15)
    kill(process.pid)

    return read_logfile(binary, port)

def ssend(binary, s_or_c, port, s_ip, s_port, sender_string):
    sender_info = ast.literal_eval(sender_string)
    command = "expect -f send_client_s.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port+" "+' '.join(sender_info)
    process = subprocess.Popen(command, shell=True)

    time.sleep(12)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_broadcast(binary, s_or_c, port, s_ip, s_port, num_messages, msg):
    command = "expect -f broadcast_client_s.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port+" "+num_messages+" "+msg
    process = subprocess.Popen(command, shell=True)

    time.sleep(12)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_block(binary, s_or_c, port, s_ip, s_port, server_to_send):
    command = "expect -f blocked_client.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port+" "+server_to_send
    process = subprocess.Popen(command, shell=True)

    time.sleep(7)
    kill(process.pid)

    return read_logfile(binary, port)

def sblock(binary, s_or_c, port, s_ip, s_port, server_to_send, msg):
    command = "expect -f send_client_b.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port+" "+server_to_send+" "+msg
    process = subprocess.Popen(command, shell=True)

    time.sleep(7)
    kill(process.pid)

    return read_logfile(binary, port)

def bblock(binary, s_or_c, port, s_ip, s_port, server_to_block):
    command = "expect -f blocking_client.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port+" "+server_to_block
    process = subprocess.Popen(command, shell=True)

    time.sleep(7)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_blocked(binary, s_or_c, port, s_ip, s_port=""):
    if s_or_c =='s': command = "expect -f sblocked_server.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip
    else: command = "expect -f sblocked_client.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port
    process = subprocess.Popen(command, shell=True)

    time.sleep(11)
    kill(process.pid)

    return read_logfile(binary, port)

def ablocked(binary, s_or_c, port, s_ip, s_port, servers):
    command = "expect -f allblock_client.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port+" "+servers.replace(';', ' ')
    process = subprocess.Popen(command, shell=True)

    time.sleep(10)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_unblock(binary, s_or_c, port, s_ip, s_port, server_to_send, msg):
    command = "expect -f unblocked_client.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port+" "+server_to_send+" "+msg
    process = subprocess.Popen(command, shell=True)

    time.sleep(10)
    kill(process.pid)

    return read_logfile(binary, port)

def uunblock(binary, s_or_c, port, s_ip, s_port, server_to_block):
    command = "expect -f unblocking_client.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port+" "+server_to_block
    process = subprocess.Popen(command, shell=True)

    time.sleep(10)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_logout(binary, s_or_c, port, s_ip, s_port):
    command = "expect -f logout_client.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port
    process = subprocess.Popen(command, shell=True)

    time.sleep(4)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_buffer(binary, s_or_c, port, s_ip, s_port):
    command = "expect -f buffer_client_r.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port
    process = subprocess.Popen(command, shell=True, close_fds=True)

    time.sleep(15)
    kill(process.pid)

    return read_logfile(binary, port)

def sbuffer(binary, s_or_c, port, s_ip, s_port, send_to_server, msg):
    command = "expect -f buffer_client_s.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port+" "+send_to_server+" "+msg
    process = subprocess.Popen(command, shell=True, close_fds=True)

    time.sleep(8)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_exit(binary, s_or_c, port):
    command = binary+" "+s_or_c+" "+str(port)
    process = subprocess.Popen(command, shell=True, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
    time.sleep(2)
    status = procStatus(process.pid)
    if status == 'R' or status == 'S':
        os.system('kill -9 '+str(process.pid))
        command = "expect -f exit.exp "+binary+" "+s_or_c+" "+str(port)
        process = subprocess.Popen(command, shell=True, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
        time.sleep(2)
        status = procStatus(process.pid)
        os.system('kill -9 '+str(process.pid))
        if status == 'Z':
            return True
        else: return False
    else:
        return False

def grade_statistics(binary, s_or_c, port, s_ip="", s_port="", sender_string=""):
    if s_or_c == 's': command = "expect -f statistics_server.exp "+binary+" "+s_or_c+" "+str(port)
    else:
        sender_info = ast.literal_eval(sender_string)
        command = "expect -f statistics_client_s.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port+" "+' '.join(sender_info)
    process = subprocess.Popen(command, shell=True)

    time.sleep(16)
    kill(process.pid)

    return read_logfile(binary, port)


def grade_exception_login(binary, s_or_c, port):
    command = "expect -f exception_login.exp "+binary+" "+s_or_c+" "+str(port)
    process = subprocess.Popen(command, shell=True)

    time.sleep(5)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_exception_send(binary, s_or_c, port, s_ip, s_port):
    command = "expect -f exception_send.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port
    process = subprocess.Popen(command, shell=True)

    time.sleep(5)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_exception_block(binary, s_or_c, port, s_ip, s_port, server_to_block=""):
    if len(server_to_block) == 0: command = "expect -f exception_block_bd.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port
    else: command = "expect -f exception_block_bg.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port+" "+server_to_block
    process = subprocess.Popen(command, shell=True)

    time.sleep(5)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_exception_unblock(binary, s_or_c, port, s_ip, s_port):
    command = "expect -f exception_unblock.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port
    process = subprocess.Popen(command, shell=True)

    time.sleep(5)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_exception_blocked(binary, s_or_c, port):
    command = "expect -f exception_blocked.exp "+binary+" "+s_or_c+" "+str(port)
    process = subprocess.Popen(command, shell=True)

    time.sleep(5)
    kill(process.pid)

    return read_logfile(binary, port)

def grade_bonus(binary, s_or_c, port, s_ip="", s_port=""):
    if s_or_c == 's': command = "expect -f bonus_server.exp "+binary+" "+s_or_c+" "+str(port)
    else:
        #Clear files from folder
        folder = os.path.dirname(binary)
        txt_file = os.path.join(folder, 'cse4589test.txt')
        bin_file = os.path.join(folder, 'cse4589test.pdf')
        os.system('rm -f '+txt_file+' '+bin_file)

        command = "expect -f bonus_client_r.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port

    process = subprocess.Popen(command, shell=True)

    time.sleep(15)
    kill(process.pid)

    return read_logfile(binary, port)

def sbonus(binary, s_or_c, port, s_ip, s_port, send_to_server):
    #Transfer files to folder
    folder = os.path.dirname(binary)
    txt_file = 'cse4589test.txt'
    bin_file = 'cse4589test.pdf'
    os.system('cp -f '+txt_file+' '+folder)
    os.system('cp -f '+bin_file+' '+folder)

    command = "expect -f bonus_client_s.exp "+binary+" "+s_or_c+" "+str(port)+" "+s_ip+" "+s_port+" "+send_to_server
    process = subprocess.Popen(command, shell=True)

    time.sleep(12)
    kill(process.pid)

    return 'DONE'

def cbonus(binary, filename):
    folder = os.path.dirname(binary)
    recv_file = os.path.join(folder, filename)
    compare = os.system('cmp '+recv_file+' '+filename)

    if compare == 0: return True
    else: return False
