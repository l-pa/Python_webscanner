import sys
import socket
import urllib.request
import argparse
import telnetlib

from ipwhois import IPWhois
from datetime import datetime, time
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--destination", type=str, help="Type website (ex. google.com)")
parser.add_argument("-o", "--output", help="Output to file", action='store_true')
parser.add_argument("-t", "--telnet", action='store_true', help="Telnet")
parser.add_argument("-p", "--ports", type=str, help="Port range (20,21,22 ...)")
parser.add_argument("-r", "--robots", action='store_true', help="Robots.txt")
parser.add_argument("-w", "--whois", action='store_true', help="Site WhoIs")

args = parser.parse_args()


class Gui(object):
    @staticmethod
    def start_text():
        Gui.print_space_text('Simple web scanner \n-d Web/IP -p ports 21,22,80...')

    def print_space_text(text):
        print("-" * 60)
        print(text)
        print("-" * 60)


class DomainCheck(object):
    def __init__(self, website, ports):
        DomainCheck.get_remote_ports(website, ports)
        Gui.print_space_text("Robots.txt : ")
        DomainCheck.read_robots_txt(website)
        Gui.print_space_text("Whos : ")
        DomainCheck.whos_lookup(website)

    @staticmethod
    def get_ip_address(url):
        ip_address = socket.gethostbyname(url)
        return ip_address

    def get_remote_ports(url, ports):
        try:
            ip_address = DomainCheck.get_ip_address(url)
            Gui.print_space_text('IP address ' + ip_address)
            print("Please wait, scanning remote host", ip_address)

            t1 = datetime.now()
            for port in ports:
                print(port)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((ip_address, int(port)))

                if result == 0:
                    print("Port {}: 	 Open".format(port))
                else:
                    print("Port {}: 	 Close".format(port))
                    sock.close()

                t2 = datetime.now()

                total = t2 - t1

                print('Scanning Completed in: ', total)

        except socket.error as err_msg:
            print("%s: %s" % (url, err_msg))

    def read_robots_txt(url):
        try:
            with urllib.request.urlopen("http://" + url + "/robots.txt") as url:
                s = url.read()
                for x in s.splitlines():
                    print(x)
        except socket.error:
            print("No connection .. Robots.txt")

    def whos_lookup(url):
        try:
            obj = IPWhois(DomainCheck.get_ip_address(url))
            results = obj.lookup_rdap(depth=1)
            pprint(results)
        except socket.error:
            print("Error no connection .. WHOS")


class Telnet(object):
    def connect_telnet(port, timeout):
        pass

    def read_telnet(self):
        pass


if __name__ == "__main__":
    Gui.start_text()

    if args.output:
        sys.stdout = open("Output.txt", "a")

    if args.ports:
        ports = args.ports.split(',')
        ports = list(map(int, ports))
        print('Port array to scan : ' + str(ports))
        DomainCheck.get_remote_ports(args.destination, ports)

    if args.robots:
        Gui.print_space_text("Robots")
        DomainCheck.read_robots_txt(args.destination)

    if args.whois:
        Gui.print_space_text("WhoIs")
        DomainCheck.whos_lookup(args.destination)
        pass

    if args.telnet:
        Telnet.connect_telnet(int(23), int(3))