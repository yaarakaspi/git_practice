import socket

dns_dict = {"nbc.com": "2.21.109.123", "cnn.com": "151.101.195.5",
            "google.com": "142.250.75.78", "github.com": "20.217.135.5",
            "facebook.com": "31.13.86.36", "applemusic.com": "17.253.142.4"}

MID_IP = "127.0.0.1"
MID_PORT = 531


def get_ip(name):
    """
    Returns IP address if exists in memory
    :param name: the domain name to check
    :return: the ip if found, else None
    """
    if name in dns_dict:
        return dns_dict[name]
    return None


def get_domain(ip):
    """
    Returns the domain name of a dns record of exists in memory
    :param ip: the ip address to check
    :return: domain name if exists, None otherwise
    """
    for key, value in dns_dict.items():
        if value == ip:
            return key
    return None


def main():
    mid_soc = socket.socket()
    mid_soc.bind((MID_IP, MID_PORT))
    mid_soc.listen(1)

    client_soc, addr = mid_soc.accept()

    while True:
        try:
            data_len = int(client_soc.recv(4).decode())
            data = client_soc.recv(data_len).decode()

            choice, val = data.split(":", 1)
        except Exception as e:
            print(f"Disconnected due to {str(e)}")
            break

        if choice == "1":
            ans = get_domain(val)
        elif choice == "2":
            ans = get_ip(val)
        else:
            ans = None

        if ans:
            reply = ans
        else:
            reply = "NOT FOUND"

        try:
            client_soc.send(str(len(reply)).zfill(4).encode())
            client_soc.send(reply.encode())
        except Exception as e:
            print(f"Disconnected due to {str(e)}")
            break

    client_soc.close()
    mid_soc.close()


if __name__ == "__main__":
    main()
