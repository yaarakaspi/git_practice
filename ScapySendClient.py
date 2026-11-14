# git: https://github.com/yaarakaspi/git_practice

from scapy.all import *
from scapy.layers.inet import UDP, IP

MY_IP = "10.100.102.246"
PORT = 9270


def main():
    while True:
        msg = " "

        # getting message to send to server
        while len(msg) != 5:
            msg = input("Please enter your 5 character message(or 'exit!' to exit): ")
            if len(msg) != 5:
                print("\n5 characters only!\n")

        # change to current computers ip
        p = IP(src=MY_IP, dst=MY_IP)/UDP(dport=PORT)/Raw(load=msg)
        send(p, verbose=False)  # added verbose to get rid of scapy "sending"

        if msg == "exit!":
            print("\nGoodbye!\n")
            break


if __name__ == "__main__":
    main()
