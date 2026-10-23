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
        url = url[1:]
    return url


def calculate_next(num):
    """
    calculates the next num(if valid)
    :param num: the number to calculate the next of
    :return: returns the "extra"
    """

    # making sure negative numbers will also pass
    pos = num
    if "-" in num:
        pos = num.lstrip('-')

    # checking if valid number
    if pos.isdigit():
        num = str(int(num) + 1)
        extra = f"Content-Length: {len(num.encode())}\r\n\r\n".encode()
        extra += num.encode()
    else:
        msg = "Invalid use of function 'calculate-next'"
        extra = f"Content-Length: {len(msg.encode())}\r\n\r\n".encode() + msg.encode()

    return extra


def calculate_area(num1, num2):
    """
    calculates the area of a triangle with num1 and num2 as height and width
    :param num1: first number for area
    :param num2: second number for area
    :return: the return "extra"
    """
    # checking if input was actually numbers
    if num1.isdigit() and num2.isdigit():
        area = str((1.0 * int(num1) * int(num2)) / 2.0)
        extra = f"Content-Length: {len(area.encode())}\r\n\r\n".encode()
        extra += area.encode()
    else:
        msg = "Invalid use of function 'calculate-area'"
        extra = f"Content-Length: {len(msg.encode())}\r\n\r\n".encode() + msg.encode()

    return extra


def build_reply(path):
    """
    builds reply to send
    :param path: the file path
    :return: full reply
    """
    forbid_files = ['secret1.html', 'secret.png', 'secret3.html']
    moved_files = {"butterfly.png": "https://pngimg.com/uploads/butterfly/butterfly_PNG1037.png", "present.png": "https://thumbs.dreamstime.com/b/d-glossy-yellow-christmas-gift-box-red-bow-png-473178015.jpg?w=768"}
    extra = f"Content-Length: 0\r\n\r\n".encode()
    if "calculate-area?" in path:
        command_type = "200 OK"
        if "height=" in path and "width=" in path and "&" in path:
            cords = path.split("&")
            num1 = cords[0].split("=")[1]
            num2 = cords[1].split("=")[1]
            extra = calculate_area(num1, num2)
        else:
            msg = "Invalid use of function 'calculate-area'"
            extra = f"Content-Length: {len(msg.encode())}\r\n\r\n".encode() + msg.encode()

    elif "calculate-next?num=" in path:
        command_type = "200 OK"
        num = path.split("=")[1]
        # getting the next number in extra
        extra = calculate_next(num)
    elif path == "server":
        command_type = "500 INTERNAL SERVER ERROR"
    elif path in forbid_files:
        command_type = "403 FORBIDDEN"
    elif path in moved_files.keys():
        command_type = "301 MOVED PERMANENTLY"
        extra = f"Location: {moved_files[path]}\r\nContent-Length: 0\r\n\r\n".encode()
    elif os.path.exists(path):

        with open(path, "rb") as file:
            data = file.read()
        length = len(data)
        extra = f"Content-Length: {str(length)}\r\n\r\n".encode()
        extra += data
        command_type = "200 OK"
    else:
        command_type = "404 NOT FOUND"

    # building message
    ans = f"HTTP/1.1 {command_type}\r\n".encode()
    ans += extra  # data is already encoded

    return ans


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
                ans = build_reply(url)  # building reply
            else:
                ans = build_reply("index.html")

            try:
                client_soc.send(ans)
            except Exception as e:
                print(f"Error in send: {e}")

            # disconnecting client
            print(f"Disconnecting client: {addr[0]}")
            client_soc.close()


if __name__ == "__main__":
    main()
