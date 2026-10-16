import socket

SRC_IP = "0.0.0.0"
SRC_PORT = 1450


def remove_layer5(data):
    """
    removes layer 5 from the data
    :param data: the received message
    :return: the message without layer 5
    """
    layer = 'last' * 10
    if data.endswith(layer):
        return data[:-len(layer)]
    return data


def remove_layer4(data):
    """
    removes layer 4 from the data
    :param data: the received message
    :return: the message without layer 4
    """
    layer = 'HaHa' * 10
    if data.endswith(layer):
        return data[:-len(layer)]
    return data


def remove_layer3(data):
    """
    removes layer 3 from the data
    :param data: the received message
    :return: the message without layer 3
    """
    layer = '1111111' * 10
    if data.endswith(layer):
        return data[:-len(layer)]
    return data


def remove_layer2(data):
    """
    removes layer 2 from the data
    :param data: the received message
    :return: the message without layer 2
    """
    layer = '-----' * 10
    if data.endswith(layer):
        return data[:-len(layer)]
    return data


def remove_layer1(data):
    """
    removes layer 1 from the data
    :param data: the received message
    :return: the message without layer 1
    """
    layer = 'layer1' * 10
    if data.endswith(layer):
        return data[:-len(layer)]
    return data


server_soc = socket.socket()
server_soc.bind((SRC_IP, SRC_PORT))
server_soc.listen(3)

while True:
    client_soc, addr = server_soc.accept()
    print(f"{addr[0]} - connected")

    while True:
        try:
            length_data = client_soc.recv(4)
        except Exception as e:
            print(f"Error: {str(e)}")
            client_soc.close()
            break
        else:
            if not length_data:
                print(f"client {addr[0]} disconnected")
                client_soc.close()
                break

            msg_length = int(length_data.decode())

            try:
                msg = client_soc.recv(msg_length)
            except Exception as e:
                print(f"Error: {str(e)}")
                client_soc.close()
                break
            else:
                if not msg:
                    print(f"client {addr[0]} disconnected")
                    client_soc.close()
                    break

                msg = msg.decode()

                if msg == 'q':
                    print(f"client {addr[0]} disconnected")
                    client_soc.close()
                    break

                # unwrapping message
                unwrapped_msg = remove_layer5(msg)
                unwrapped_msg = remove_layer4(unwrapped_msg)
                unwrapped_msg = remove_layer3(unwrapped_msg)
                unwrapped_msg = remove_layer2(unwrapped_msg)
                unwrapped_msg = remove_layer1(unwrapped_msg)

                print(f"Original message: {unwrapped_msg}")


