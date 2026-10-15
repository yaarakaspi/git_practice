import socket

def getUrl(answer):
    """
    gets url from http message
    :param answer: the http message
    :return: the url
    """
    lines = answer.split('\r\n')
    params = lines[0].split(' ')
    urll = None
    if len(params) == 3 and params[0] == "GET" and params[2] == "HTTP/1.1":
        urll = params[1]
    return urll[1:]

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

        url = getUrl(data)
        ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len(url))}\r\n\r\n{url}"
        try:
            client_soc.send(ans.encode())
        except Exception as e:
            print(f"Error in send: {e}")