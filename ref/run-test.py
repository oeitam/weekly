#! /usr/bin/python

import re
import argparse
import sys
import os
import json
import subprocess
import tempfile
import time
import socket

gverbose = ""
gresults = {}

gchild_stdout = open('gchild_stdout', 'w')
gchild_stderr = open('gchild_stderr', 'w')


# helper functions
def get_next_port():
    # increment the counter file with each call
    # write to file for debug
    fh = open('/home/ubuntu/bibifi/rundir/port', 'r+')
    count_str = fh.read()
    count_int = int(count_str)
    count_int += 1
    fh.seek(0)  # reset teh location in the file to beginning
    fh.write(str(count_int))
    fh.close
    return count_int


def connect_to_server(port):
    s = socket.socket()  # Create a socket object
    s.connect(("localhost", port))
    return s


def send_input(s, inp):
    s.send(inp)


def readlines(sock, recv_buffer=4096, delim='\n'):
    buffer = ''
    data = True
    while data:
        data = sock.recv(recv_buffer)
        buffer += data
        while buffer.find(delim) != -1:
            line, buffer = buffer.split('\n', 1)
            yield line
    return


def read_test():
    f = open(testFile, 'r')
    test = json.loads(f.read())
    f.close()
    return test


def runServer(server, port):
    # print "--" + server + "--"
    # print type(server)
    p = subprocess.Popen([server, str(port)]
                         #                      )
                         ,
                         stdout=gchild_stdout,
                         stderr=gchild_stderr)
    ##out,err = p.communicate())
    # gchild_stdout, gchild_stderr = p.communicate()


    time.sleep(2)

    p.poll()
    # print( p.returncode)
    if p.returncode == 63:
        return runServer(server, port + 1)

    return (p, port)


def stopServer(p):
    # print "one"
    p.terminate()
    cnt = 0
    while cnt < 3:
        stat = p.poll()
        # print stat
        if stat == None:
            time.sleep(1)
            cnt += 1
            print
            "waited for %d second" % cnt
        else:
            cnt = 10

            # p.wait()
    if p.poll == None:  # still alive -> kill
        p.kill()

        print("server exited with return code: " + str(p.returncode))


def serializeProgram(program):
    plist = list(program)
    l = len(plist)

    for i in range(l - 1, -1, -1):
        if (ord(plist[i]) == 10):  # new line
            plist[i] = "n"
            plist.insert(i, chr(92))  # "\"
        if (ord(plist[i]) == 34):  # -"-
            plist.insert(i, chr(92))  # "\"

            # print "%2d: -%s-%d-" % (i,alist[i],ord(alist[i]))

    return ("".join(plist))


def extract_team_num(server):
    match = re.search(r'\/(\d{3,4})\/', server)
    return match.group(1)


def compare_results():
    print
    "================== COMPARE ==================================="
    for i in range(0, len(gresults)):
        # print i
        for j in range(0, len(gresults)):
            # print "  " + str(j)
            if j > i:
                print
                "compare keys %s vs %s" % (gresults.keys()[i], gresults.keys()[j])
                for k in range(0, len(gresults[gresults.keys()[0]])):
                    # print "    " + str(k)
                    elem1 = gresults[gresults.keys()[i]]
                    elem2 = gresults[gresults.keys()[j]]
                    if (elem1[k] == [] or elem2[k] == []):
                        empty = " (one is empty)"
                    else:
                        empty = ""
                    if (elem1[k] == elem2[k]):
                        print
                        "%2d:        MATCH" % k
                    else:
                        print
                        "%2d: DO NOT MATCH%s" % (k, empty)
                        print
                        "%s: %s" % (gresults.keys()[i], elem1[k])
                        print
                        "%s: %s" % (gresults.keys()[j], elem2[k])

    print
    "====================================================="


################################################################
def Init():
    # this procedure is used for initializations of what
    # ever is needed
    global gverbose

    test = ""
    init_file = ""
    servers = ""
    gverbose = ""
    test_path = ""
    filt_server = []
    only_server = []

    # handling arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', '-t',
                        help='the name of the test that is being run')
    parser.add_argument('--test_path', '-p',
                        help='path to where the tests are stored')
    parser.add_argument('--verbose', '-v',
                        help='spits out also the communication with teh server',
                        action='store_true')
    parser.add_argument('--init_file', '-i',
                        help='points to the init file that holds the definitions of locations for the program. default is init.file in the run directory')
    parser.add_argument('--servers', '-s',
                        help='points to the list of servers to run the test upon.')
    parser.add_argument('--filter_server', '-f',
                        help='do not run for this server. can take multiple of these. conflicts with -o, but the program does not protect from this.',
                        action='append')
    parser.add_argument('--only_server', '-o',
                        help='run only for this server. can take multiple of these. conflicts with -f, but no protection in the program itself.',
                        action='append')

    args = parser.parse_args()
    test = args.test
    init_file = args.init_file
    servers = args.servers
    gverbose = args.verbose
    test_path = args.test_path
    filt_server = args.filter_server
    only_server = args.only_server

    # print init_file
    # print type(init_file)


    if init_file == None:
        fh = open('init.file', 'r')
    else:
        fh = open(init_file, 'r')

    for line in fh:
        # print line.rstrip("\n")
        match = re.search(r'^(\w+) (\S+)', line)
        if match:
            if match.group(1) == "test":
                if test == None:
                    test = match.group(2)
            if match.group(1) == "test_path":
                if test_path == None:
                    test_path = match.group(2)
            # if match.group(1) == "init_file":
            #    if init_file == False:
            #        init_file = match.group(2)
            if match.group(1) == "servers":
                if servers == None:
                    servers = match.group(2)

    fh.close()

    print
    "using as test: %s" % test
    print
    "using as test path: %s" % test_path
    print
    "using as init_file: %s" % init_file
    print
    "using as servers: %s" % servers
    print
    "using as gverbose: %s" % gverbose

    return test, init_file, servers, test_path, filt_server, only_server


#######################################################
def run_test_on_server(progs, server):
    global gresults
    # spec = read_test()

    snum = extract_team_num(server)
    res_list = []

    # print server
    port_sent = get_next_port()
    (p, port) = runServer(server.rstrip("\n"), port_sent)
    # (p, port) = runServer("/home/osboxes/MYSTUFF/breakers/840/build/server",8900)

    # progs = spec['programs']

    prog_cnt = 1
    for prog in progs:
        # send program
        # prog = proginfo['program']
        s = connect_to_server(port)
        print("===> sending program ")
        # print("Printing prog:")
        # for i in prog.splitlines(True):
        #    print("^^" + i)
        # print(prog.splitlines(True))
        for i in prog.splitlines(True):
            print
            i.rstrip("\n")
        send_input(s, prog)
        # get output
        print("===> receiving output:")
        results = "["
        oneline = False
        for line in readlines(s):
            # print(line)
            if (oneline):
                results += ", "
            results += line
            oneline = True
        results += "]"
        s.close()
        if gverbose:
            print("===============================")
            print(results)
            print("===============================")

        res = json.loads(results)
        res_list.append(res)
        # output = proginfo['output']
        output = {"status": "INVALID - FOR TEST PURPOSE ONLY"}
        if (res == output):
            print("===> output MATCHES")
        else:
            print("===> output DOES NOT match")
        prog_cnt += 1

    gresults[snum] = res_list
    stopServer(p)


########################################################################

def main():
    print
    "Starting ...                                          "
    print
    "======================================================"
    print

    test, init_file, servers, test_path, filt_server, only_server = Init()

    # print test
    # print init_file
    print
    servers

    testfile = test_path + "/" + test + ".scr"
    outfile = test_path + "/" + test + ".out"

    print
    "======================================================"
    print
    "Working on test %s" % testfile
    print
    "Expecting output from %s" % outfile
    print
    "======================================================"

    progs1 = []
    progs2 = []
    f = open(testfile, 'r')
    build_prog = ""
    for line in f:
        match = re.search(r'^\s*$', line)
        if match:
            continue
        print
        line.rstrip("\n")
        build_prog = build_prog + line
        match = re.search(r'^\*\*\*', line)
        if match:
            progs1.append(serializeProgram(build_prog))
            progs2.append(build_prog)
            # print "--" + build_prog
            build_prog = ""

    f.close()

    # for p in progs1:
    #    print p
    # for p in progs2:
    #    print p

    # build the test
    # read the test and create a json file out of it
    # spec = { "arguments" : { "argv" : ["%PORT%" ]} }

    # print json.dumps(spec, sort_keys=True, indent=4, separators=(',', ': '))

    ## send to server in

    if type(filt_server) != type([]):
        filt_server = []
    if type(only_server) != type([]):
        only_server = []

    f = open(servers, 'r')
    for s in f:
        match = re.search(r'^\s*$', s)
        if match:
            continue
        match = re.search(r'^#', s)
        if match:
            continue
        tmp1 = 0
        for h in filt_server:
            if h in s:
                print
                "Filtered %s" % h
                tmp1 = 1
                continue
        if tmp1 == 1:
            continue

        tmp2 = 0
        if only_server != []:
            for h in only_server:
                if h in s:
                    tmp2 = 1
            if tmp2 == 0:
                continue

        print
        "================================================================"
        print
        s
        print
        "================================================================"
        run_test_on_server(progs2, s)

    f.close()

    print
    json.dumps(gresults, sort_keys=True,
               indent=4, separators=(',', ': '))

    if (gchild_stdout):
        gchild_stdout.close()

    if (gchild_stderr):
        gchild_stderr.close()

    compare_results()


#######################################################

main()

#######################################################
