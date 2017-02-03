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

import copy
import itertools
import random
from collections import Counter
from pprint import pprint
from random import choice
import string
import sys
import threading
import time
import Queue

from remote_api import run_on_servers, run_on_server
from pa1_parser import *
from utils import *

# STARTUP
def startup(binary):
    score = 0.0

    message = ['STARTUP', binary, 's', '5678']
    if run_on_servers(message) == ['True']*5:
        score += 2.5

    message = ['STARTUP', binary, 'c', '7845']
    if run_on_servers(message) == ['True']*5:
        score += 2.5

    print score

# AUTHOR
def author(binary):
    score = 0.0

    student_ubit = binary.split(os.sep)[-2]

    message = ['AUTHOR', binary, 's', '6354']
    output = extractOutputSuccess('AUTHOR', run_on_server('stones.cse.buffalo.edu', message))
    if output:
        if parseAUTHOR(output) == student_ubit: score += 0.5

    message = ['AUTHOR', binary, 'c', '7435']
    output = extractOutputSuccess('AUTHOR', run_on_server('highgate.cse.buffalo.edu', message))
    if output:
        if parseAUTHOR(output) == student_ubit: score += 0.5

    if score == 1.0: print 'TRUE'
    else: print 'FALSE'

# IP
def ip(binary):
    score = 0.0

    for index in range(5):
        server = GRADING_SERVERS_HOSTNAME[index]
        port = str(random_port())

        message = ['IP', binary, 's', port]
        output = extractOutputSuccess('IP', run_on_server(server, message))
        if output:
            if parseIP(output) == GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(server)]:
                score += 0.5

    for index in range(5):
        server = GRADING_SERVERS_HOSTNAME[index]
        port = str(random_port())

        message = ['IP', binary, 'c', port]
        output = extractOutputSuccess('IP', run_on_server(server, message))
        if output:
            if parseIP(output) == GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(server)]:
                score += 0.5

    print score

# PORT
def port(binary):
    score = 0.0

    for index in range(5):
        server = GRADING_SERVERS_HOSTNAME[index]
        port = str(random_port())

        message = ['PORT', binary, 's', port]
        output = extractOutputSuccess('PORT', run_on_server(server, message))
        if output:
            if parsePORT(output) == port:
                score += 0.5

    for index in range(5):
        server = GRADING_SERVERS_HOSTNAME[index]
        port = str(random_port())

        message = ['PORT', binary, 'c', port]
        output = extractOutputSuccess('PORT', run_on_server(server, message))
        if output:
            if parsePORT(output) == port:
                score += 0.5

    print score

# LIST
def list_client_output(server_list, port_list):
    output = []
    for num_hosts in range(1,5):
        host_list = []
        for index in range(num_hosts):
            server = server_list[index]
            port = port_list[index]
            host = [server, GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(server)], str(port)]
            host_list.append(host)

        host_list.sort(key=lambda x: int(x[2]))
        for x in range(len(host_list)):
            host_list[x].insert(0,str(x+1))

        output.append(host_list)

    return output

def list_server_output(server_list, port_list):
    output = []
    for server, port in itertools.izip(server_list, port_list):
        host = [server, GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(server)], str(port)]
        output.append(host)

    output.sort(key=lambda x: int(x[2]))
    for x in range(len(output)):
        output[x].insert(0,str(x+1))

    return output

def list(binary):
    score = 0.0

    server_list = copy.deepcopy(GRADING_SERVERS_HOSTNAME)
    for index in range(0,5):
        app_server = server_list.pop(0)
        app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
        app_server_port = str(random_port())

        message = ['LIST', binary, 's', app_server_port]
        retval_q = Queue.Queue()
        s_thread = threading.Thread(target=lambda queue, server, msg: queue.put(run_on_server(server, msg)), args=(retval_q, app_server, message))
        s_thread.start()

        time.sleep(1)

        port_list = [random_port() for x in range(4)]
        clients_output = []
        for server in server_list:
            port = port_list.pop(0)
            message = ['LIST', binary, 'c', str(port), app_server_ip, app_server_port]
            clients_output.append(extractOutputSuccess('LIST', run_on_server(server, message)))
            port_list.append(port)

        client_output = [parseLIST(output) for output in clients_output]
        s_thread.join()
        server_output = parseLIST(extractOutputSuccess('LIST', retval_q.get()))

        # Sort the output
        try:
            for output in client_output:
                output.sort(key=lambda x: int(x[3]))
                for x in range(len(output)):
                    output[x][0] = str(x+1)

            server_output.sort(key=lambda x: int(x[3]))
            for x in range(len(server_output)):
                server_output[x][0] = str(x+1)
        except: pass

        if cmp(client_output, list_client_output(server_list, port_list)) == 0: score += 1.0
        else:
            print 'Client:'
            pprint(client_output)
            print
            pprint(list_client_output(server_list, port_list))
        if cmp(server_output, list_server_output(server_list, port_list)) == 0: score += 1.0
        else:
            print 'Server:', app_server
            pprint(server_output)
            print
            pprint(list_server_output(server_list, port_list))

        server_list.append(app_server)
        time.sleep(3)

    del(server_list)
    print score

def refresh(binary):
    score = 0.0

    app_server = GRADING_SERVERS_HOSTNAME[0]
    app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
    app_server_port = str(random_port())

    message = ['LIST', binary, 's', app_server_port]
    s_thread = threading.Thread(target=run_on_server, args=(app_server, message))
    s_thread.start()

    time.sleep(1)

    port_list = [random_port() for x in range(4)]
    clients_output = []

    c_threads = []
    retval_q = Queue.Queue()
    server_list = GRADING_SERVERS_HOSTNAME[1:]
    for server in server_list:
        port = port_list.pop(0)
        message = ['REFRESH', binary, 'c', str(port), app_server_ip, app_server_port]
        c_thread = threading.Thread(target=lambda queue, svr, msg: queue.put(run_on_server(svr, msg)), args=(retval_q, server, message))
        c_thread.start()
        c_threads.append(c_thread)
        port_list.append(port)

    # Wait till all client threads finish
    for t in c_threads:
        t.join()

    # Collect all output
    while not retval_q.empty():
        clients_output.append(extractOutputSuccess('LIST', retval_q.get()))

    client_output = [parseLIST(output) for output in clients_output]

    # Sort the output
    try:
        for output in client_output:
            output.sort(key=lambda x: int(x[3]))
            for x in range(len(output)):
                output[x][0] = str(x+1)
    except: pass

    for output in client_output:
        if cmp(output, list_server_output(server_list, port_list)) == 0: score += 1.25
        else:
            pprint(output)
            print '-----'
            pprint(list_server_output(server_list, port_list))

    print score

def send_server_output(send_server, server_list, short_msg, big_msg):
    index = 0
    output = []
    for recv_server in server_list[1:]:
        output.append([GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(send_server)],
                         GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(recv_server)],
                         short_msg[index]])
        output.append([GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(send_server)],
                         GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(recv_server)],
                         big_msg[index]])
        index += 1

    return output

def send_client_output(send_server, server_list, short_msg, big_msg):
    index = 0
    output = []
    for recv_server in server_list[1:]:
        output.append([[GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(send_server)],
                          short_msg[index]],
                        [GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(send_server)],
                          big_msg[index]]])
        index += 1

    return output

def send(binary):
    score = 0.0

    server_list = copy.deepcopy(GRADING_SERVERS_HOSTNAME)
    for index in range(0,2):
        app_server = server_list.pop(0)
        app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]

        server_port = str(random_port())
        message = ['SEND', binary, 's', server_port]
        s_retval_q = Queue.Queue()
        s_thread = threading.Thread(target=lambda queue, svr, msg: queue.put(run_on_server(svr, msg)), args=(s_retval_q, app_server, message))
        s_thread.start()

        time.sleep(1)

        # Init. Receiving Servers
        port_list = [random_port() for x in range(3)]
        clients_output = []

        c_threads = []
        c_retval_q = Queue.Queue()
        for server in server_list[1:]:
            port = port_list.pop(0)
            message = ['SEND', binary, 'c', str(port), app_server_ip, server_port]
            c_thread = threading.Thread(target=lambda queue, svr, msg: queue.put(run_on_server(svr, msg)), args=(c_retval_q, server, message))
            c_thread.start()
            c_threads.append(c_thread)
            port_list.append(port)

        time.sleep(2)

        # Sending Server
        send_server = server_list[0]
        send_server_port = str(random_port())
        #ASCII = ''.join(chr(x) for x in range(32,127)).replace(';','').replace(':','')\n\t\r!#$%&\()*+,-./<=>?@[\\]^_{|}~
        ASCII_easy = string.digits+string.ascii_letters
        ASCII_hard = string.digits+string.ascii_letters+' !#%&();*+,-./<=>?@^_{}~'
        short_msg = []
        big_msg = []
        for index in range(3):
            msg = ''.join(choice(ASCII_easy) for _ in range(126))
            msg = 'x'+msg+'y'
            short_msg.append(msg)
            msg = ''.join(choice(ASCII_hard) for _ in range(254))
            msg = 'x'+msg+'y'
            big_msg.append(msg)

        ssend_message = ['SSEND', binary, 'c', str(send_server_port), app_server_ip, server_port]
        ip_list = [GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(server)] for server in server_list[1:]]
        msg_list = []
        for s_msg, b_msg in itertools.izip(short_msg, big_msg):
            msg_list.append('"'+s_msg+'"')
            msg_list.append('"'+b_msg+'"')

        ssend_message.append(str(ip_list+msg_list))
        run_on_server(send_server, ssend_message)

        # Wait till all threads finish
        s_thread.join()
        for t in c_threads:
            t.join()

        # Collect all output
        while not c_retval_q.empty():
            clients_output.append(extractOutputSuccess('RECEIVED', c_retval_q.get(), mode='all'))
        server_output = extractOutputSuccess('RELAYED', s_retval_q.get(), mode='all')

        server_output = [parseRELAYED(output) for output in server_output]
        client_output = []
        for client in clients_output:
            output = [parseRECEIVED(msg) for msg in client]
            client_output.append(output)

        expected_server_output = send_server_output(send_server, server_list, short_msg, big_msg)
        expected_client_output = send_client_output(send_server, server_list, short_msg, big_msg)

        print
        pprint(server_output)
        pprint(expected_server_output)
        print
        pprint(client_output)
        pprint(expected_client_output)

        #Match Server Output
        for srv_msg, exp_msg in itertools.izip(server_output, expected_server_output):
            if cmp(srv_msg, exp_msg) == 0: score += (7.5/6.0)/2.0
            else:
                print
                pprint(srv_msg)
                print
                pprint(exp_msg)

        #Match Client output
        for client, exp_client in itertools.izip(client_output, expected_client_output):
            for cl_msg, exp_msg in itertools.izip(client, exp_client):
                if cmp(cl_msg, exp_msg) == 0: score += (7.5/6.0)/2.0
                else:
                    print
                    pprint(cl_msg)
                    print
                    pprint(exp_msg)

        server_list.append(app_server)

    del(server_list)
    print score

def broadcast(binary):
    score = 0.0

    server_list = copy.deepcopy(GRADING_SERVERS_HOSTNAME)

    app_server = server_list.pop(0)
    app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
    app_server_port = str(random_port())

    message = ['SEND', binary, 's', app_server_port]
    s_retval_q = Queue.Queue()
    s_thread = threading.Thread(target=lambda queue, svr, msg: queue.put(run_on_server(svr, msg)), args=(s_retval_q, app_server, message))
    s_thread.start()

    time.sleep(3)

    # Init. Receiving Servers
    port_list = [random_port() for x in range(3)]
    clients_output = []

    c_threads = []
    c_retval_q = Queue.Queue()
    for server in server_list[1:]:
        port = port_list.pop(0)
        message = ['SEND', binary, 'c', str(port), app_server_ip, app_server_port]
        c_thread = threading.Thread(target=lambda queue, svr, msg: queue.put(run_on_server(svr, msg)), args=(c_retval_q, server, message))
        c_thread.start()
        c_threads.append(c_thread)
        port_list.append(port)

    time.sleep(1)

    # Broadcasting Server
    send_server = server_list[0]
    send_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(send_server)]
    send_server_port = str(random_port())
    bcast_msg = ''.join(choice(string.ascii_letters) for _ in range(50))
    broadcast_message = ['BROADCAST', binary, 'c', str(send_server_port), app_server_ip, app_server_port, '5', bcast_msg]
    run_on_server(send_server, broadcast_message)

    # Wait till all threads finish
    s_thread.join()
    for t in c_threads:
        t.join()

    # Collect all output
    while not c_retval_q.empty():
        clients_output.append(extractOutputSuccess('RECEIVED', c_retval_q.get(), mode='all'))
    server_output = extractOutputSuccess('RELAYED', s_retval_q.get(), mode='all')

    server_output = [parseRELAYED(output) for output in server_output]
    client_output = []
    for client in clients_output:
        output = [parseRECEIVED(msg) for msg in client]
        client_output.append(output)

    expected_server_output = [[send_server_ip, '255.255.255.255', bcast_msg] for _ in range(5)]
    expected_client_output = [[[send_server_ip, bcast_msg] for _ in range(5)] for _ in range(3)]

    print
    pprint(server_output)
    pprint(expected_server_output)
    print
    pprint(client_output)
    pprint(expected_client_output)

    #Match Server Output
    for srv_msg, exp_msg in itertools.izip(server_output, expected_server_output):
        if cmp(srv_msg, exp_msg) == 0: score += 0.5

    #Match Client output
    for m_index in range(5):
        try:
            if (cmp(client_output[0][m_index], expected_client_output[0][m_index]) == 0 and
                cmp(client_output[1][m_index], expected_client_output[1][m_index]) == 0 and
                cmp(client_output[2][m_index], expected_client_output[2][m_index]) == 0): score += 1.5
        except: pass

    del(server_list)
    print score

def block(binary):
    score = 0.0

    app_server = GRADING_SERVERS_HOSTNAME[0]
    app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
    app_server_port = str(random_port())

    message = ['SEND', binary, 's', app_server_port]
    s_retval_q = Queue.Queue()
    s_thread = threading.Thread(target=lambda queue, svr, msg: queue.put(run_on_server(svr, msg)), args=(s_retval_q, app_server, message))
    s_thread.start()

    time.sleep(1)

    blocked_server = GRADING_SERVERS_HOSTNAME[1]
    blocked_port = str(random_port())
    blocking_server = GRADING_SERVERS_HOSTNAME[2]
    blocking_port = str(random_port())
    sending_server = GRADING_SERVERS_HOSTNAME[3]
    sending_server_port = str(random_port())

    message = ['BLOCK', binary, 'c', blocked_port, app_server_ip, app_server_port, GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(blocking_server)]]
    threading.Thread(target=run_on_server, args=(blocked_server, message)).start()
    time.sleep(1)
    message = ['SBLOCK', binary, 'c', sending_server_port, app_server_ip, app_server_port, GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(blocking_server)], 'Hello']
    threading.Thread(target=run_on_server, args=(sending_server, message)).start()
    time.sleep(1)
    message = ['BBLOCK', binary, 'c', blocking_port, app_server_ip, app_server_port, GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(blocked_server)]]
    c_retval_q = Queue.Queue()
    c_thread = threading.Thread(target=lambda queue, svr, msg: queue.put(run_on_server(svr, msg)), args=(c_retval_q, blocking_server, message))
    c_thread.start()

    c_thread.join()
    s_thread.join()

    server_output = extractOutputSuccess('RELAYED', s_retval_q.get(), mode='all')
    client_output = extractOutputSuccess('RECEIVED', c_retval_q.get(), mode='all')

    if len(client_output) == 1:
        if cmp(parseRECEIVED(client_output[0]), [GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(sending_server)], 'Hello']) == 0: score += 5.0

    print score

def blocked(binary):
    score = 0.0

    app_server = GRADING_SERVERS_HOSTNAME[0]
    app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
    app_server_port = str(random_port())

    blocking_server = GRADING_SERVERS_HOSTNAME[4]
    blocking_server_port = str(random_port())

    message = ['BLOCKED', binary, 's', app_server_port, GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(blocking_server)]]
    s_retval_q = Queue.Queue()
    s_thread = threading.Thread(target=lambda queue, svr, msg: queue.put(run_on_server(svr, msg)), args=(s_retval_q, app_server, message))
    s_thread.start()

    time.sleep(1)

    port_list = [random_port() for x in range(3)]

    for server in GRADING_SERVERS_HOSTNAME[1:4]:
        port = port_list.pop(0)
        message = ['BLOCKED', binary, 'c', str(port), app_server_ip, app_server_port]
        threading.Thread(target=run_on_server, args=(server, message)).start()
        port_list.append(port)
        time.sleep(1)

    message = ['ABLOCKED', binary, 'c', blocking_server_port, app_server_ip, app_server_port, ';'.join(GRADING_SERVERS_IP[1:4])]
    run_on_server(blocking_server, message)

    s_thread.join()

    server_output = parseLIST(extractOutputSuccess('BLOCKED', s_retval_q.get()))

    # Sort the output
    try:
        server_output.sort(key=lambda x: int(x[3]))
        for x in range(len(server_output)):
            server_output[x][0] = str(x+1)
    except: pass

    if cmp(server_output, list_server_output(GRADING_SERVERS_HOSTNAME[1:4], port_list)) == 0: score += 5.0

    print score

def unblock(binary):
    score = 0.0

    app_server = GRADING_SERVERS_HOSTNAME[0]
    app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
    app_server_port = str(random_port())

    message = ['SEND', binary, 's', app_server_port]
    threading.Thread(target=run_on_server, args=(app_server, message)).start()
    time.sleep(1)

    blocked_server = GRADING_SERVERS_HOSTNAME[1]
    blocked_port = str(random_port())
    blocking_server = GRADING_SERVERS_HOSTNAME[2]
    blocking_port = str(random_port())

    message = ['UNBLOCK', binary, 'c', blocked_port, app_server_ip, app_server_port, GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(blocking_server)], 'HiThere']
    threading.Thread(target=run_on_server, args=(blocked_server, message)).start()
    time.sleep(1)

    message = ['UUNBLOCK', binary, 'c', blocking_port, app_server_ip, app_server_port, GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(blocked_server)]]
    client_output = extractOutputSuccess('RECEIVED', run_on_server(blocking_server, message), mode='all')

    print client_output

    if len(client_output) == 1:
        if cmp(parseRECEIVED(client_output[0]), [GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(blocked_server)], 'HiThere']) == 0: score += 2.5

    print score

def logout(binary):
    score = 0.0

    app_server = GRADING_SERVERS_HOSTNAME[0]
    app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
    app_server_port = str(random_port())

    message = ['LIST', binary, 's', app_server_port]
    s_retval_q = Queue.Queue()
    s_thread = threading.Thread(target=lambda queue, svr, msg: queue.put(run_on_server(svr, msg)), args=(s_retval_q, app_server, message))
    s_thread.start()

    time.sleep(1)

    port_list = [random_port() for x in range(3)]
    clients_output = []

    for server in GRADING_SERVERS_HOSTNAME[1:4]:
        port = port_list.pop(0)
        message = ['LIST', binary, 'c', str(port), app_server_ip, app_server_port]
        threading.Thread(target=run_on_server, args=(server, message)).start()
        port_list.append(port)
        time.sleep(1)

    logout_server = GRADING_SERVERS_HOSTNAME[4]
    logout_server_port = str(random_port())
    message = ['LOGOUT', binary, 'c', logout_server_port, app_server_ip, app_server_port]
    client_output = run_on_server(logout_server, message)

    s_thread.join()

    server_output = parseLIST(extractOutputSuccess('LIST', s_retval_q.get()))

    print
    print server_output
    print
    print client_output
    print

    # Sort the output
    try:
        server_output.sort(key=lambda x: int(x[3]))
        for x in range(len(server_output)):
            server_output[x][0] = str(x+1)
    except: pass

    if cmp(server_output, list_server_output(GRADING_SERVERS_HOSTNAME[1:4], port_list)) == 0: score += 2.0
    if extractOutputSuccess('AUTHOR', client_output) != None: score += 0.5

    print score

def buffer(binary):
    score = 0.0

    app_server = GRADING_SERVERS_HOSTNAME[0]
    app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
    app_server_port = str(random_port())

    message = ['SEND', binary, 's', app_server_port]
    threading.Thread(target=run_on_server, args=(app_server, message)).start()

    time.sleep(1)

    recv_server = GRADING_SERVERS_HOSTNAME[2]
    recv_server_port = str(random_port())
    send_server = GRADING_SERVERS_HOSTNAME[1]
    send_server_port = str(random_port())

    message = ['BUFFER', binary, 'c', recv_server_port, app_server_ip, app_server_port]
    threading.Thread(target=run_on_server, args=(recv_server, message)).start()
    time.sleep(1)
    msg = ''.join(choice(string.ascii_letters) for _ in range(50))
    message = ['SBUFFER', binary, 'c', send_server_port, app_server_ip, app_server_port, GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(recv_server)], msg]
    threading.Thread(target=run_on_server, args=(send_server, message)).start()

    time.sleep(5)
    #Query 1
    message = ['LOGFILE', binary, str(recv_server_port)]
    server_output_1 = run_on_server(recv_server, message)

    time.sleep(7)
    #Query 2
    message = ['LOGFILE', binary, str(recv_server_port)]
    server_output_2 = run_on_server(recv_server, message)

    if len(extractOutputSuccess('RECEIVED', server_output_1, mode='all')) == 0:
        if len(extractOutputSuccess('RECEIVED', server_output_2, mode='all')) == 5: score += 5.0

    print score

def exit(binary):
    score = 0.0

    message = ['EXIT', binary, 'c', '7845']
    if run_on_servers(message) == ['True']*5:
        score += 2.5

    print score

def statistics_server_output(server_list, send_server):
    output = []
    for server in server_list:
        if server == send_server:
            output.append([server, '6', '0', 'offline'])
        else: output.append([server, '0', '2', 'online'])

    return output

def statistics(binary):
    score = 0.0

    server_list = copy.deepcopy(GRADING_SERVERS_HOSTNAME)
    for index in range(0,2):
        app_server = server_list.pop(0)
        app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
        app_server_port = str(random_port())

        message = ['STATISTICS', binary, 's', app_server_port]
        s_retval_q = Queue.Queue()
        s_thread = threading.Thread(target=lambda queue, svr, msg: queue.put(run_on_server(svr, msg)), args=(s_retval_q, app_server, message))
        s_thread.start()

        time.sleep(1)

        # Init. Receiving Servers
        port_list = [random_port() for x in range(3)]
        clients_output = []

        c_threads = []
        for server in server_list[1:]:
            port = port_list.pop(0)
            message = ['SEND', binary, 'c', str(port), app_server_ip, app_server_port]
            c_thread = threading.Thread(target=run_on_server, args=(server, message))
            c_thread.start()
            c_threads.append(c_thread)
            port_list.append(port)

        time.sleep(1)

        # Sending Server
        send_server = server_list[0]
        send_server_port = str(random_port())
        ASCII = ''.join(chr(x) for x in range(32,127)).replace(';','').replace(':','')
        short_msg = []
        big_msg = []
        for index in range(3):
            short_msg.append(''.join(choice(string.ascii_letters) for _ in range(12)))
            big_msg.append(''.join(choice(string.ascii_letters) for _ in range(25)))

        message = ['STATISTICS', binary, 'c', str(send_server_port), app_server_ip, app_server_port]
        ip_list = [GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(server)] for server in server_list[1:]]
        msg_list = []
        for s_msg, b_msg in itertools.izip(short_msg, big_msg):
            msg_list.append('"'+s_msg+'"')
            msg_list.append('"'+b_msg+'"')

        message.append(str(ip_list+msg_list))
        threading.Thread(target=run_on_server, args=(send_server, message)).start()

        # Wait till all threads finish
        s_thread.join()
        for t in c_threads:
            t.join()

        server_output = extractOutputSuccess('STATISTICS', s_retval_q.get())
        server_output = parseSTATISTICS(server_output)

        # Remove the index
        try:
            for host in server_output:
                host.pop(0)
        except: pass

        expected_server_output = statistics_server_output(server_list, send_server)

        print server_output
        print expected_server_output

        try:
            if len(server_output) == len(expected_server_output):
                for host in server_output:
                    if host in expected_server_output: score += 2.5/4.0
        except: pass

        server_list.append(app_server)

    del(server_list)
    print score

def exception_login(binary):
    score = 0.0

    app_server = GRADING_SERVERS_HOSTNAME[0]
    app_server_port = str(random_port())

    message = ['EXCEPTION-LOGIN', binary, 'c', app_server_port]
    output = extractOutputError('LOGIN', run_on_server(app_server, message), mode='all')
    print output

    expected = ['','','','']

    for index in range(len(expected)):
        try:
            if output[index] == expected[index]: score += 0.5
        except: pass

    print score

def exception_send(binary):
    score = 0.0

    app_server = GRADING_SERVERS_HOSTNAME[0]
    app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
    app_server_port = str(random_port())
    message = ['SEND', binary, 's', app_server_port]
    threading.Thread(target=run_on_server, args=(app_server, message)).start()

    time.sleep(1)

    client = GRADING_SERVERS_HOSTNAME[1]
    client_port = str(random_port())
    message = ['EXCEPTION-SEND', binary, 'c', client_port, app_server_ip, app_server_port]

    output = extractOutputError('SEND', run_on_server(client, message), mode='all')
    expected = ['','']

    for index in range(len(expected)):
        try:
            if output[index] == expected[index]: score += 1.0
        except: pass

    print score

def exception_block(binary):
    score = 0.0

    app_server = GRADING_SERVERS_HOSTNAME[0]
    app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
    app_server_port = str(random_port())

    message = ['SEND', binary, 's', app_server_port]
    threading.Thread(target=run_on_server, args=(app_server, message)).start()

    time.sleep(1)

    blocked_client = GRADING_SERVERS_HOSTNAME[1]
    blocked_client_port = str(random_port())
    blocking_client = GRADING_SERVERS_HOSTNAME[2]
    blocking_client_port = str(random_port())

    message = ['EXCEPTION-BLOCK', binary, 'c', blocked_client_port, app_server_ip, app_server_port]
    threading.Thread(target=run_on_server, args=(blocked_client, message)).start()
    time.sleep(1)
    message = ['EXCEPTION-BLOCK', binary, 'c', blocking_client_port, app_server_ip, app_server_port, GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(blocked_client)]]

    output = run_on_server(blocking_client, message)
    output_e = extractOutputError('BLOCK', output, 'all')
    output_s = extractOutputSuccess('BLOCK', output, 'all')
    expected_e = ['','','']
    expected_s = ['']

    print output

    for index in range(len(expected_e)):
        try:
            if output_e[index] == expected_e[index]: score += 0.5
        except: pass

    if cmp(output_s, expected_s) == 0: score += 0.5

    print score

def exception_unblock(binary):
    score = 0.0

    app_server = GRADING_SERVERS_HOSTNAME[0]
    app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
    app_server_port = str(random_port())

    message = ['SEND', binary, 's', app_server_port]
    threading.Thread(target=run_on_server, args=(app_server, message)).start()

    time.sleep(1)

    client = GRADING_SERVERS_HOSTNAME[1]
    client_port = str(random_port())
    message = ['EXCEPTION-UNBLOCK', binary, 'c', client_port, app_server_ip, app_server_port]

    output = extractOutputError('UNBLOCK', run_on_server(client, message), mode='all')
    expected = ['','','','']

    for index in range(len(expected)):
        try:
            if output[index] == expected[index]: score += 0.5
        except: pass

    print score

def exception_blocked(binary):
    score = 0.0

    server = GRADING_SERVERS_HOSTNAME[0]
    server_port = str(random_port())
    message = ['EXCEPTION-BLOCKED', binary, 's', server_port]

    output = extractOutputError('BLOCKED', run_on_server(server, message), 'all')
    expected = ['','']

    for index in range(len(expected)):
        try:
            if output[index] == expected[index]: score += 1.0
        except: pass

    print score

def bonus(binary):
    score = 0.0

    app_server = GRADING_SERVERS_HOSTNAME[0]
    app_server_ip = GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(app_server)]
    app_server_port = str(random_port())

    message = ['BONUS', binary, 's', app_server_port]
    threading.Thread(target=run_on_server, args=(app_server, message)).start()

    time.sleep(1)

    recv_client = GRADING_SERVERS_HOSTNAME[1]
    recv_client_port = str(random_port())
    message = ['BONUS', binary, 'c', recv_client_port, app_server_ip, app_server_port]
    threading.Thread(target=run_on_server, args=(recv_client, message)).start()
    time.sleep(1)
    send_client = GRADING_SERVERS_HOSTNAME[2]
    send_client_port = str(random_port())
    message = ['SBONUS', binary, 'c', send_client_port, app_server_ip, app_server_port, GRADING_SERVERS_IP[GRADING_SERVERS_HOSTNAME.index(recv_client)]]
    run_on_server(send_client, message)

    message = ['CBONUS', binary, 'cse4589test.txt']
    if run_on_server(recv_client, message) == 'True': score += 10.0
    else: print 'TXT Failed'

    message = ['CBONUS', binary, 'cse4589test.pdf']
    if run_on_server(recv_client, message) == 'True': score += 10.0
    else: print 'PDF Failed'

    print score
