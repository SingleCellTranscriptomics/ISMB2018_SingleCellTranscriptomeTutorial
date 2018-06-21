#!/usr/bin/env python
# encoding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os, sys, re
import logging
import argparse
import subprocess

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)



def main():

    parser = argparse.ArgumentParser(description="instantiate user spaces", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--ip_addr", type=str, required=True, help="IP address for server")
    parser.add_argument("--attendee_list", type=str, required=True, help="attendee list file")
    parser.add_argument("--user_id_start", type=int, required=True, help="index to start user IDs (ex. 1)")
    parser.add_argument("--apache_base_port", type=int, default=None, help="base port for apache")
    parser.add_argument("--gateone_base_port", type=int, default=None, help="base port for gateone")
    parser.add_argument("--rstudio_base_port", type=int, default=None, help="base port for rstudio")
    
    args = parser.parse_args()

    
    apache_user_port = args.apache_base_port
    gateone_user_port = args.gateone_base_port
    rstudio_user_port = args.rstudio_base_port
    
    print("<html><body><h1>Single Cell RNA-Seq Workshop in <br>Bern, Switzerland (October 12-13, 2016)</h1></body></html>")

    print("<style>\n" +
          "tr:nth-child(even) {background: #CCC}\n" +
          "tr:nth-child(odd) {background: #FFF}\n" +
          "</style>\n")
    

    print("<table shade='rows'>\n")
    print ("<tr><th>id</th><th>Attendee</th><th>SSH Terminal</th><th>Apache Viewer</th><th>Rstudio</th></tr>")
        
    user_id = args.user_id_start
    with open(args.attendee_list) as f:
        for attendee_name in f:
            attendee_name = attendee_name.rstrip()
            print("<tr><td>{}</td>".format(user_id) +
                  "<td>{}</td>".format(attendee_name) +
                  "<td><a href=\"{}\" target='_sshterm'>ssh terminal</a></td>".format(url_maker(args.ip_addr, gateone_user_port)) +
                  "<td><a href=\"{}\" target='_apacheview'>apache</a></td>".format(url_maker(args.ip_addr, apache_user_port)) +
                  "<td><a href=\"{}\" target='_rstdioview'>rstudio</a></td>".format(url_maker(args.ip_addr, rstudio_user_port)) +
                  "</tr>")
            
            apache_user_port += 1
            gateone_user_port += 1
            rstudio_user_port += 1

            user_id += 1
    
    print("</table></body></html>")
    
    sys.exit(0)


def url_maker(ip_addr, port_num):

    return("http://" + ip_addr + ":" + str(port_num))



####################
 
if __name__ == "__main__":
    main()
