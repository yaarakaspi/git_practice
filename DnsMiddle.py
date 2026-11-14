import socket
from zoneinfo import reset_tzpath

MID_IP = "127.0.0.1"
MID_PORT = 53

MASTER_IP = "127.0.0.1"
MASTER_PORT = 531

dns_dict = {"nbc.com": "2.21.109.123", "cnn.com": "151.101.195.5", "google.com": "142.250.75.78"}


def get_ip(name, soc):
    """
    Returns the ip address of a dns record of exists in memory
    :param name: the domain name to check
    :param soc: the socket used to send to upper dns server
    :return: IP address if exists, None otherwise
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

    return None


def get_domain(ip, soc):
    """
    Returns the domain name of a dns record of exists in memory
    :param ip: the ip address to check
    :param soc: the socket used to send to upper dns server
    :return: domain name if exists, None otherwise
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

    return None


def main():
    mid_soc = socket.socket()

    try:
        mid_soc.connect((MASTER_IP, MASTER_PORT))
    except Exception as e:
        print(f"Disconnected due to {str(e)}")

    master_soc = socket.socket()
    master_soc.bind((MID_IP, MID_PORT))
    master_soc.listen(1)

    start_soc, addr = mid_soc.accept()

    while True:
        try:
            # getting length of message from start dns
            data_len = int(start_soc.recv(4).decode())

            # getting actual message
            data = start_soc.recv(data_len).decode()
        except Exception as e:
            exit(f"Disconnected due to {str(e)}")

        # splitting to get choice and the actual value
        choice, val = data.split(":", 1)

        if choice == "1":
            ans = get_domain(val, mid_soc)
        elif choice == "2":
            ans = get_ip(val, mid_soc)
        else:
            ans = None

        if ans:
            reply = ans
        else:
            reply = "NOT FOUND"

        try:
            # sending the length first
            start_soc.send(str(len(reply)).zfill(4).encode())
            # sending actual message
            start_soc.send(reply.encode())
        except Exception as e:
            print(f"Disconnected due to {str(e)}")
            break

    start_soc.close()
    mid_soc.close()
    master_soc.close()

if __name__ == "__main__":
    main()
