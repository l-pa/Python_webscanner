import telnetlib
import ipaddress
import socket
import subprocess
import sys
import urllib.request
from tld import get_tld
from ipwhois import IPWhois
from datetime import datetime
from pprint import pprint

class Gui:
    def print_space_text(text):
        print("-" * 60)
        print(text)
        print("-" * 60)


class DomainCheck:
    ip = 0

    def get_ip_address(url):
        ip_address = socket.gethostbyname(url)
        ip = ip_address
        return ip_address

    # def get_domain_name(url):
    #     try:
    #        domain_name = get_tld(url)
    #     except ValueError:
    #         print("Probabbly bad URL")
    #         staticURL = url
    #    return domain_name


    def get_remote_ports(url):

        try:
            ip_address = DomainCheck.get_ip_address(url)
            print(ip_address)
            remote_server_ip = ip_address

            print("Please wait, scanning remote host", remote_server_ip)

            t1 = datetime.now()
            print("Start port : ")
            port_one = input()
            print("End port : ")
            port_sec = input()
            if port_one == port_sec:  # ARG
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((remote_server_ip, int(port_one)))
                if result == 0:
                    print("Port {}: 	 Open".format(port_one))
                else:
                    print("Port {}: 	 Close".format(port_one))
                    sock.close()
            else:  # ARG
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
            with urllib.request.urlopen("http://" + url + "/robots.txt") as url:
                s = url.read()
            pprint(s)
        except socket.error:
            print("No connection .. Robots.txt")

    def whos_lookup(url):
        try:
            obj = IPWhois(DomainCheck.get_ip_address(url))
            results = obj.lookup_rdap(depth=1)
            pprint(results)
        except socket.error:
            print("Error no connection .. WHOS")


class Folder:

    def create_dir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def write_file(self, path, data):
        f = open(path, 'w')
        f.write(data)
        f.close()


class Telnet:
    def connect_to(self):
        host = ipaddress.ip_address('192.168.1.1', 21)
        telnet = telnetlib.Telnet(host)
        print(telnet.read_all())

def main():
    print("Type website : ")
    website = input()
    DomainCheck.get_remote_ports(website)

    Gui.print_space_text("Robots.txt : ")

    DomainCheck.read_robots_txt(website)

    Gui.print_space_text("Whos : ")

    DomainCheck.whos_lookup(website)

    Gui.print_space_text("Telnet : #WIP")

    Telnet.connect_to()


if __name__ == "__main__":
    main()