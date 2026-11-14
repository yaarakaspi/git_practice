# git: https://github.com/yaarakaspi/git_practice

from scapy.all import *
from scapy.layers.inet import UDP, IP

MY_IP = "10.100.102.246"
PORT = 9270


def filter_pckt(p):
    """
    filters packets based on the ip and port we're looking for
    :param p: the packet
    :return: true if wanted, false otherwise
    """
    if IP in p and UDP in p:
        if p[IP].dst == MY_IP and p[UDP].dport == PORT:
            return True
    return False


def stop_fil(p):
    """
    stops sniffing when gets "exit!"
    :param p: the packet
    :return: true if wanted, false otherwise
    """
    if Raw in p:
        data = p[Raw].load.decode()
        if data == "exit!":
            print("Exit received, stopping sniffing")
            return True
    return False


def print_msg(p):
    """
    prints the msg in payload from packet
    :param p: the packet
    :return: none
    """
    if Raw in p:
        data = p[Raw].load.decode()
        print(f"Received: {data}")


def main():
    # calling sniffer with functions above to filter, print, and exit
    sniff(iface=r"\Device\NPF_Loopback", lfilter=filter_pckt, prn=print_msg, stop_filter=stop_fil)


if __name__ == "__main__":
    main()
