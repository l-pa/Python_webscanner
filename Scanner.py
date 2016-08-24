import socket
import sys
import urllib.request
from ipwhois import IPWhois
from datetime import datetime, time
from pprint import pprint
import argparse
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--destination", type=str, help="Type website (ex. google.com)")
parser.add_argument("-o", "--output", help="Output to file", action='store_true')
parser.add_argument("-t", "--telnet", action='store_true', help="Telnet")
parser.add_argument("-p", "--ports", type=str, help="Port range (20,21,22 ...)")
parser.add_argument("-s", "--silent", action='store_true', help="Silent mode")

args = parser.parse_args()


class Gui:
    def start_text():
        Gui.print_space_text('Simple web scanner \n -d Web/IP -p ports 80,21,20...')

    def print_space_text(text):
        print("-" * 60)
        print(text)
        print("-" * 60)


class DomainCheck:
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

class FileIO:
    def domain_check_to_file(self, website):
        DomainCheck.get_remote_ports(website)
        Gui.print_space_text("Robots.txt : ")
        DomainCheck.read_robots_txt(website)
        Gui.print_space_text("Whos : ")
        DomainCheck.whos_lookup(website)


class Telnet:
    def connect_telnet(self, ip, port):
        pass

    def read_telnet(self):
        pass


if __name__ == "__main__":
    Gui.start_text()

    if args.ports:
        ports = args.ports.split(',')
        ports = list(map(int, ports))
        print(ports)
        DomainCheck(args.destination, ports)

    if args.output:
        sys.stdout = open("Output.txt", "a")
        DomainCheck(args.destination, ports)
        sys.stdout.close()

    if args.telnet:
        print("WIP")

    # print("Use -h --help")
