#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
import sys


# start a new nmap scan on localhost with some specific options
def do_scan(targets, options):
    parsed = None
    nmproc = NmapProcess(targets, options)
    rc = nmproc.run()
    if rc != 0:
        print("nmap scan failed: {0}".format(nmproc.stderr))
    print(type(nmproc.stdout))

    try:
        parsed = NmapParser.parse(nmproc.stdout)
    except NmapParserException as e:
        print("Exception raised while parsing scan: {0}".format(e.msg))

    return parsed


# print scan results from a nmap report
def print_scan(nmap_report):
    print("Starting Nmap {0} ( http://nmap.org ) at {1}".format(
        nmap_report.version,
        nmap_report.started))
    content = ""
    for host in nmap_report.hosts:
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
        else:
            tmp_host = host.address

        print("Nmap scan report for {0} ({1})".format(
            tmp_host,
            host.address))
        print("Host is {0}.".format(host.status))
        print("  PORT     STATE         SERVICE")

        for serv in host.services:
            pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format(
                    str(serv.port),
                    serv.protocol,
                    serv.state,
                    serv.service)
            if (serv.port == int(scan_port)) and (serv.state == "open"):
                content = content + tmp_host + "\n"
            if len(serv.banner):
                pserv += " ({0})".format(serv.banner)
            print(pserv)
    write_to_file('out.txt',content)
    print(nmap_report.summary)

def write_to_file(filename,content):
    outfile = open(filename,'w');
    outfile.write(content)
    outfile.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('usage: python %s ip -p{port}' % sys.argv[0])
    ips = sys.argv[1]
    opts = "-sV %s" % sys.argv[2]
    _,scan_port = sys.argv[2].split('p')
    # print scan_port
    report = do_scan(ips, opts)
    if report:
        print_scan(report)
    else:
        print("No results returned")