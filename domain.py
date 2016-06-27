from tld import get_tld
import socket
import subprocess
import sys
import urllib.request
from ipwhois import IPWhois
from datetime import datetime
from pprint import pprint
from gui import printSpaceText


def get_ip_address(url):
    ip_address = socket.gethostbyname(url)
    return ip_address


#def get_domain_name(url):
#     try:
#        domain_name = get_tld(url)
#     except ValueError:
#         print("Probabbly bad URL")
#         staticURL = url
#    return domain_name


def get_remote_ports(url):

    try:
        ip_address = get_ip_address(url)
        print(ip_address)
        remote_server_ip = ip_address

        print("Please wait, scanning remote host", remote_server_ip)

        t1 = datetime.now()
        print("Start port : ")
        port_one = input()
        print("End port : ")
        port_sec = input()
        if port_one == port_sec:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((remote_server_ip, int(port_one)))
            if result == 0:
                print("Port {}: 	 Open".format(port_one))
            else:
                print("Port {}: 	 Close".format(port_one))
                sock.close()
        else:
            try:
                for port in range(int(port_one), int(port_sec)):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex((remote_server_ip, port))

                    if result == 0:
                        print("Port {}: 	 Open".format(port))
                    else:
                        print("Port {}: 	 Close".format(port))
                    sock.close()

            except KeyboardInterrupt:
                print("You pressed Ctrl+C")
                sys.exit()

            except socket.gaierror:
                print('Hostname could not be resolved. Exiting')
                sys.exit()

            except socket.error:
                print("Couldn't connect to server")
                sys.exit()

            t2 = datetime.now()

            total = t2 - t1

            print('Scanning Completed in: ', total)

    except socket.error as err_msg:
        print("%s: %s" % (url, err_msg))


def read_robots_txt(url):
    try:
        with urllib.request.urlopen("http://"+url+"/robots.txt") as url:
            s = url.read()
        pprint(s)
    except socket.error:
        print("No connection .. Robots.txt")


def whos_lookup(url):
    try:
        obj = IPWhois(get_ip_address(url))
        results = obj.lookup_rdap(depth=1)
        pprint(results)
    except socket.error:
        print("Error no connection .. WHOS")