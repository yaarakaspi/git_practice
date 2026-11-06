from scapy.all import *
conf.iface = r"\Device\NPF_Loopback"

active_iface = conf.route.route("8.8.8.8")[0]  # sniff wasn't working and I tried many different things but
# kept not working, so I asked gemini what I could do and it offered this


def HTTPFilter(p):
    """
    filters http packets only
    :param p: the packet to filter
    :return: True or False
    """
    return TCP in p and Raw in p and b'GET' in p[Raw].load


def HTTPrint(p):
    """
    prints the url from http message
    :param p: the packet to print from
    :return: none
    """
    data = p[Raw].load.decode()
    url = data.split('Host: ')[1].split('\r\n')[0] + data.split(' ')[1]
    print(url)


p = sniff(iface=active_iface, count=10, lfilter=HTTPFilter, prn=HTTPrint)

