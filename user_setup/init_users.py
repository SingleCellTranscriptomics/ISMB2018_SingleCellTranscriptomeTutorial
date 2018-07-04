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


docker_image = "trinityctat/scellismb2018"

resources_dir = "/data/SINGLE_CELL/single_cell_data_ro"

def main():

    parser = argparse.ArgumentParser(description="instantiate user spaces", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--num_users", type=int, default="", required=True, help="number of users")

    parser.add_argument("--user_id_start", type=int, default=1, help="index to start user IDs (ex. 1)")
    
    parser.add_argument("--apache_base_port", type=int, default=8001, help="base port for apache")
    parser.add_argument("--gateone_base_port", type=int, default=9001, help="base port for gateone")
    parser.add_argument("--ssh_base_port", type=int, default=10001, help="base port for rstudio")

    args = parser.parse_args()

    
    apache_user_port = args.apache_base_port
    gateone_user_port = args.gateone_base_port
    ssh_user_port = args.ssh_base_port
    
    users_basedir = os.path.abspath("user_spaces")
    if not os.path.isdir(users_basedir):
        os.makedirs(users_basedir)

    print("sudo chown -R training user_spaces")
    print("sudo chgrp -R training user_spaces")

    user_id_start = args.user_id_start
    
    for i in range(user_id_start, user_id_start + args.num_users):
        
        # create user directory
        user = "user_{:02d}".format(i)
        user_dir = os.path.sep.join([users_basedir, user])
        if not os.path.isdir(user_dir):
            os.makedirs(user_dir)
            
        # launch docker
        cmd = str("sudo docker run --rm -v {}:/home/training ".format(user_dir) +
                  " -v {}/shared:/home/training/shared_ro:ro ".format(resources_dir) +
                  #" -v {}:/var/www/html ".format(user_dir) +
                  #" -v {}/js:/var/www/html/js:ro ".format(resources_dir) +
                  #" -v {}/css:/var/www/html/css:ro ".format(resources_dir) +
                  #" -p {}:22 -p {}:80 -p {}:443 ".format(ssh_user_port, apache_user_port, gateone_user_port) +
                  #" -p {}:22 -p {}:80 -p {}:443 ".format(ssh_user_port, apache_user_port, gateone_user_port) +
                  " -p {}:8787 ".format(ssh_user_port) + #rstudio port actually
                  " --name rstudio_{} -d {}".format(user, docker_image))
        
        #subprocess.check_output(cmd)
        
        print(cmd)
        
        print()

        
        apache_user_port += 1
        gateone_user_port += 1
        ssh_user_port += 1



    sys.exit(0)
 
####################
 
if __name__ == "__main__":
    main()

