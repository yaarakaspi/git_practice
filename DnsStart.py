import socket

dns_dict = {"nbc.com": "2.21.109.123", "cnn.com": "151.101.195.5", "google.com": "142.250.75.78"}

MID_IP = "127.0.0.1"
MID_PORT = 53


def get_ip(name, soc):
    """
    Returns the ip address of a dns record of exists in memory
    :param name: the domain name to check
    :param soc: the socket used to send to upper dns server
    :return: IP address if exists, "NOT FOUND" otherwise
    """
    if name in dns_dict:
        return dns_dict[name]

    # if not in personal dictionary, goes here
    try:
        msg = f"2:{name}"  # sending 2 for domain name -> IP
        # sending length
        soc.send(str(len(msg)).zfill(4).encode())
        # sending message itself
        soc.send(msg.encode())

        # getting len of answer from server
        data_len = int(soc.recv(4).decode())
        # getting data itself using length from server
        data = soc.recv(data_len).decode()

        if data != "NOT FOUND":
            dns_dict[name] = data
            return data
    except Exception as e:
        exit(f"Disconnected due to {str(e)}")

    return "NOT FOUND"


def get_domain(ip, soc):
    """
    Returns the domain name of a dns record of exists in memory
    :param ip: the ip address to check
    :param soc: the socket used to send to upper dns server
    :return: domain name if exists, "NOT FOUND" otherwise
    """
    for key, value in dns_dict.items():
        if value == ip:
            return key

    # if not in personal dictionary, goes here
    try:
        msg = f"1:{ip}"
        # sending length first
        soc.send(str(len(msg)).zfill(4).encode())
        # sending actual message
        soc.send(msg.encode())

        # getting reply length from server
        data_len = int(soc.recv(4).decode())
        # getting actual reply
        data = soc.recv(data_len).decode()

        if data != "NOT FOUND":
            dns_dict[data] = ip
            return data
    except Exception as e:
        exit(f"Disconnected due to {str(e)}")

    return "NOT FOUND"


def main():
    start_soc = socket.socket()

    try:
        start_soc.connect((MID_IP, MID_PORT))
    except Exception as e:
        exit(f"Disconnected due to {str(e)}")

    choice = "1"

    while choice in ["1", "2"]:
        choice = input("\n1. ip -> domain name\n2. domain name -> ip\n3. exit\nPlease choose: ")
        if choice == "1":
            ip = input("Please enter the ip address: ")
            domain_name = get_domain(ip, start_soc)
            print(domain_name)
        if choice == "2":
            domain_name = input("Please enter the domain name to check: ")
            ip = get_ip(domain_name, start_soc)
            print(ip)

    print("\n\nSee you later...")
    start_soc.close()


if __name__ == "__main__":
    main()
