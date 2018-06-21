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
    
    parser.add_argument("--num_users", type=int, default="", required=True, help="number of users")
    parser.add_argument("--ip_addr", type=str, required=True, help="IP address for server")

    parser.add_argument("--user_id_start", type=int, default=1, help="index to start user IDs (ex. 1)")
    parser.add_argument("--apache_base_port", type=int, default=8001, help="base port for apache")
    parser.add_argument("--gateone_base_port", type=int, default=9001, help="base port for gateone")
    parser.add_argument("--rstudio_base_port", type=int, default=10001, help="base port for rstudio")

    args = parser.parse_args()

    
    apache_user_port = args.apache_base_port
    gateone_user_port = args.gateone_base_port
    rstudio_user_port = args.rstudio_base_port

    users_basedir = os.path.abspath("user_spaces")
    if not os.path.isdir(users_basedir):
        os.makedirs(users_basedir)

    print("sudo chown -R training user_spaces")
    print("sudo chgrp -R training user_spaces")

    user_id_start = args.user_id_start
    
    for i in range(user_id_start, user_id_start + args.num_users + 1):
        
        # create user directory
        user = "user_{:02d}".format(i)
        user_dir = os.path.sep.join([users_basedir, user])
        if not os.path.isdir(user_dir):
            os.makedirs(user_dir)
            
        # launch docker
        cmd = str("sudo docker run --rm -v {}:/home/training ".format(user_dir) +
                  #" -v /home/training/workshop_shared/shared:/home/training/shared_ro:ro " +
                  #" -v {}:/var/www/html ".format(user_dir) +
                  #" -v /home/training/workshop_shared/js:/var/www/html/js:ro " +
                  #" -v /home/training/workshop_shared/css:/var/www/html/css:ro " +
                  " -p {}:80 -p {}:443 -p {}:8787 ".format(apache_user_port, gateone_user_port, rstudio_user_port) +
                  " --name trinity_{} -d trinityctat/scellismb2018".format(user))
        
        #subprocess.check_output(cmd)
        
        print(cmd)
                
        apache_user_port += 1
        gateone_user_port += 1
        rstudio_user_port += 1



    sys.exit(0)
 
####################
 
if __name__ == "__main__":
    main()
