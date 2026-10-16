import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 1450


def layer1(data):
    """
    adds layer 1 to the data
    :param data: the og message
    :return: the message wrapped with layer 1
    """
    return data + ('layer1' * 10)


def layer2(data):
    """
    adds layer 2 to the data
    :param data: the og message
    :return: the message wrapped with layer 2
    """
    return data + ('-----' * 10)


def layer3(data):
    """
    adds layer 3 to the data
    :param data: the og message
    :return: the message wrapped with layer 3
    """
    return data + ('1111111' * 10)


def layer4(data):
    """
    adds layer 4 to the data
    :param data: the og message
    :return: the message wrapped with layer 4
    """
    return data + ('HaHa' * 10)


def layer5(data):
    """
    adds layer 5 to the data
    :param data: the og message
    :return: the message wrapped with layer 5
    """
    return data + ('last' * 10)


client_socket = socket.socket()

try:
    client_socket.connect((SERVER_IP, SERVER_PORT))
except Exception as e:
    print(f"Disconnected due to {str(e)}")
else:
    while True:
        msg = input("Enter message(or q to quit): ")

        if msg == 'q':
            client_socket.send(str(4).encode())
            client_socket.send("q".encode())
            break

        # wrapping message
        wrapped_msg = layer1(msg)
        wrapped_msg = layer2(wrapped_msg)
        wrapped_msg = layer3(wrapped_msg)
        wrapped_msg = layer4(wrapped_msg)
        wrapped_msg = layer5(wrapped_msg)

        # sending length of message
        client_socket.send(str(len(wrapped_msg)).zfill(4).encode())
        # sending actual message
        client_socket.send(wrapped_msg.encode())

client_socket.close()
