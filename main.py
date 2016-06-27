from directory import *
from domain import *
from gui import printSpaceText

def main():
    print("Type website : ")
    website = input()
    get_remote_ports(website)

    printSpaceText("Robots.txt : ")

    read_robots_txt(website)

    printSpaceText("Whos : ")

    whos_lookup(website)


if __name__ == "__main__":
    main()
