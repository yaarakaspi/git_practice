from scapy.all import *
conf.iface = r"\Device\NPF_Loopback"


def HTTPFilter(p):
    return TCP in p and Raw in p and b'GET' in p[Raw].load


def HTTPrint(p):
    print(p[Raw].load.split(b'\r\n')[0].decode())


p = sniff(iface=r"\Device\NPF_Loopback", count=10, lfilter=HTTPFilter, prn=HTTPrint)

