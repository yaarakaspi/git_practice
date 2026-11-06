from scapy.all import *
from scapy.layers.dns import DNSRR

conf.iface = r"\Device\NPF_Loopback"

active_iface = conf.route.route("8.8.8.8")[0]  # sniff wasn't working and I tried many different things but
# kept not working so I asked gemini what I could do and it offered this


def DNSFilter(p):
    """
    filters for DNS packet responses
    :param p: the packet to filter
    :return: True or False
    """
    return IP in p and DNS in p and p[DNS].qr == 1 and DNSRR in p and p[DNSRR].type == 1


def DNSPrint(p):
    """
    prints the IPv4 from packet
    :param p: the packet to print
    :return: none
    """
    found_ip = p[DNSRR].rdata
    print(f"IP-> {found_ip}")


# iface=r"\Device\NPF_Loopback",
p = sniff(iface=active_iface, count=10, lfilter=DNSFilter, prn=DNSPrint)
