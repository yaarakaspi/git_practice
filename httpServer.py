# https://github.com/yaarakaspi/git_practice

import socket
import os


def get_url(answer):
    """
    gets url from http message
    :param answer: the http message
    :return: the url
    """
    lines = answer.split('\r\n')
    params = lines[0].split(' ')
    url = None
    if len(params) == 3 and params[0] == "GET" and params[2] == "HTTP/1.1":
        url = params[1]
    return url[1:]

def build_reply(path):
    """
    builds reply to send
    :param path: the file path
    :return: full reply
    """
    extra = None
    if os.path.exists(path):
        with open(path, "rb") as file:
            data = file.read()
        length = len(data)
        extra = f"Content-Length: {str(length)}\r\n\r\n".encode()
        extra += data
        command_type = "200 OK"
    else:
        command_type = "404 NOT FOUND"

    #building message
    ans = f"HTTP/1.1 {command_type}\r\n".encode()
    if extra:
        ans += extra  # data is already encoded

    return ans

#def get_command_type():

def main():
    server_soc = socket.socket()
    server_soc.bind(("0.0.0.0", 80))
    server_soc.listen(3)

    while True:
        client_soc, addr = server_soc.accept()
        print(f"{addr[0]} connected")

        try:
            data = client_soc.recv(1024).decode()
        except Exception as e:
            print(f"Error in receive {str(e)}")
        else:
            print(data)

            url = get_url(data)
            if url:
                # checking if file is valid
                ans = build_reply(url) # building reply

                try:
                    client_soc.send(ans)
                except Exception as e:
                    print(f"Error in send: {e}")

                #disconnecting client
                print(f"Disconnecting client: {addr[0]}")
                client_soc.close()
            else:
                # disconnecting client
                print(f"Disconnecting client: {addr[0]}")
                client_soc.close()

if __name__ == "__main__":
    main()
