import sys
import socket
import urllib.request
import argparse
import os

from ipwhois import IPWhois
from datetime import datetime, time
from pprint import pprint
parser = argparse.ArgumentParser()


parser.add_argument("-d", "--destination", type=str, help="Type website or IP (ex. google.com)")
parser.add_argument("-o", "--output", help="Output to file", action='store_true')
parser.add_argument("-p", "--ports", type=str, help="Port range (20,1,22 ...)")
parser.add_argument("-r", "--robots", action='store_true', help="Robots.txt")
parser.add_argument("-w", "--whois", action='store_true', help="Site WhoIs")

args = parser.parse_args()

class Gui(object):
    @staticmethod
    def start_text():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        Gui.print_space_text('SWC (Simple web scanner!) -h --help \n \n' + str(datetime.now()))

    def print_space_text(text):
        print("-" * 60)
        print(text)
        print("-" * 60)

    def beep_Done(os):
        print('\n')
        print('Local system : ' + os)
        return os


class DomainCheck(object):
    def __init__(self, website, ports):
        DomainCheck.get_remote_ports(website, ports)
        Gui.print_space_text("Robots.txt : ")
        DomainCheck.get_remote_robotsTxt(website)
        Gui.print_space_text("Whos : ")
        DomainCheck.get_remote_whos(website)

    @staticmethod
    def get_remote_IP(url):
        ip_address = socket.gethostbyname(url)
        return ip_address

    def get_remote_ports(url, ports):
        try:
            ip_address = DomainCheck.get_remote_IP(url)
            Gui.print_space_text('IP address: ' + ip_address + ' ' + args.destination)
            print("Please wait, scanning remote host", ip_address)

            t1 = datetime.now()
            for port in ports:

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((ip_address, int(port)))

                if result == 0:
                    print("Port {}:      Open".format(port))
                else:
                    print("Port {}:      Close".format(port))
                    sock.close()

                t2 = datetime.now()

                total = t2 - t1

            print('Scanning Completed in: ', total)

        except socket.error as err_msg:
            print("%s: %s" % (url, err_msg))

    def get_remote_robotsTxt(url, https = ''):
        try:
            with urllib.request.urlopen("http"+https+"://" + url + "/robots.txt") as url:
                s = url.read()
                for x in s.splitlines():
                    print("     " + x)
        except socket.error:
            print("No connection .. Robots.txt")

    def get_remote_whos(url):
        try:
            obj = IPWhois(DomainCheck.get_remote_IP(url))
            results = obj.lookup_rdap(depth=1)
            pprint(results)
        except socket.error:
            print("Error no connection .. WHOS")

def main():
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
        DomainCheck.get_remote_robotsTxt(args.destination)

    if args.whois:
        Gui.print_space_text("WhoIs")
        DomainCheck.get_remote_whos(args.destination)
        pass

    Gui.beep_Done(os.name)

if __name__ == "__main__":
    main()
