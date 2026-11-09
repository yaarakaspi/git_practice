from scapy.all import *
from scapy.layers.inet import TCP, IP


def main():
    msg = " "

    # getting message to send to server
    while len(msg) != 5:
        msg = input("Please enter your 5 character message: ")
        if len(msg) != 5:
            print("\n5 characters only!\n")

    # change to current computers ip
    p = IP(src="192.168.4.79", dst="192.168.4.79")/TCP()/Raw()
    send(p)

if __name__ == "__main__":
    main()