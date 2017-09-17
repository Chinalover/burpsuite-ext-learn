#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
import sys

MAX_THREAD_NUM = 10 
usage = """
		masscan 192.168.1.0/24 -p 1-65535 >out
		python %s out
		""" % sys.argv[0]
# start a new nmap scan on localhost with some specific options
def do_scan(targets, options):
    parsed = None
    nmproc = NmapProcess(targets, options)
    rc = nmproc.run()
    if rc != 0:
        print("nmap scan failed: {0}".format(nmproc.stderr))
    # print(nmproc.stdout)

    try:
        parsed = NmapParser.parse(nmproc.stdout)
    except NmapParserException as e:
        print("Exception raised while parsing scan: {0}".format(e.msg))

    return parsed


# print scan results from a nmap report
def print_scan(nmap_report):
    # print("Starting Nmap {0} ( http://nmap.org ) at {1}".format(
    #     nmap_report.version,
    #     nmap_report.started))
    for host in nmap_report.hosts:
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
        else:
            tmp_host = host.address

        for serv in host.services:
            pserv = "{0}  {1:>3s}/{2:3s}  {3:12s}  {4}".format(tmp_host,
                    str(serv.port),
                    serv.protocol,
                    serv.state,
                    serv.service)
            if len(serv.banner):
                pserv += " ({0})".format(serv.banner)
            print(pserv)
	# print(nmap_report.summary)

def write_to_file(filename,content):
    outfile = open(filename,'w');
    outfile.write(content)
    outfile.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(usage)
    masscan_results = open(sys.argv[1],'r').readlines()
    print("   HOST          PORT   STATE         SERVICE")
    for one_result in masscan_results:
    	one_result = one_result.replace("\n","")
    	if len(one_result.split(" "))>4:
			ip = one_result.split(" ")[5]
			port = one_result.split(" ")[3].split("/")[0]
			opts = "-sV -p%s -Pn" % port
			report = do_scan(ip, opts)
			if report:
				print_scan(report)
			else:
				print("No results returned")