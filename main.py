from directory import *
from domain import *

if __name__ == "__main__":
    print("Type website : ")
    website = input()
    get_remote_ports(website)
    print("-" * 60)
    print("Robots.txt : ")
    print("-" * 60)
    #read_robots_txt(website)
    print("-" * 60)
    print("Who is : ")
    print("-" * 60)
    whos_lookup(website)
