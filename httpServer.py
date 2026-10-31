# https://github.com/yaarakaspi/git_practice

import socket
import os


def check_get(answer):
    """
    checks if answer is of type get
    :param answer: the message to check
    :return: true if get, false otherwise
    """
    params = answer.split(' ')
    if len(params) == 3 and params[0] == "GET" and params[2] == "HTTP/1.1":
        return True
    return False


def check_post(answer):
    """
    checks if answer is of type post
    :param answer: the message to check
    :return: true if post, false otherwise
    """
    params = answer.split(' ')
    if len(params) == 3 and params[0] == "POST" and params[2] == "HTTP/1.1":
        return True
    return False


def get_url(answer):
    """
    gets url from http message
    :param answer: the http message
    :return: the url
    """
    params = answer.split(' ')
    url = None
    if check_get(answer) or check_post(answer):
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
    if "image?img_name=" in path:
        file_name = path.split("img_name=")[1]

        # checking if img was already saved
        if os.path.exists(file_name):
            with open(file_name, "rb") as f:
                data = f.read()
            length = len(data)
            extra = f"Content-Length: {str(length)}\r\n\r\n".encode()
            extra += data
            command_type = "200 OK"
        else:
            command_type = "404 NOT FOUND"
    elif "calculate-area?" in path:
        command_type = "200 OK"
        if "height=" in path and "width=" in path and "&" in path:
            cords = path.split("&")
            if len(cords) > 2:
                msg = "Invalid use of function 'calculate-area'"
                extra = f"Content-Length: {len(msg.encode())}\r\n\r\n".encode() + msg.encode()
            else:
                num1 = cords[0].split("=")[1]
                num2 = cords[1].split("=")[1]
                extra = calculate_area(num1, num2)
        else:
            msg = "Invalid use of function 'calculate-area'"
            extra = f"Content-Length: {len(msg.encode())}\r\n\r\n".encode() + msg.encode()
    elif "calculate-next" == path:
        command_type = "200 OK"
        extra = calculate_next("4")
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
            data = client_soc.recv(1024)  # not decoding because might be image
        except Exception as e:
            print(f"Error in receive {str(e)}")
            client_soc.close()
            continue

        if data:
            # splitting headers and body
            if "\r\n\r\n".encode() in data:
                data_split = data.split("\r\n\r\n".encode(), 1)
                headers = data_split[0]
                body = data_split[1]

                headers = headers.decode()
                lines = headers.split('\r\n')
                url = get_url(lines[0])

                content_len = 0
                for line in lines:
                    if line.lower().startswith("content-length:"):
                        content_len = int(line.split(":")[1].strip())

                # keep receiving until end of post
                while len(body) < content_len:
                    body += client_soc.recv(1024)

                if check_post(lines[0]):
                    if url and "cyberServ?secret" in url:
                        secret_msg = body.decode()
                        print(f"Secret message: {secret_msg}\n")

                        # adding to file
                        with open("secret_messages.txt", "a") as f:
                            f.write(secret_msg + "\n")
                        ans = "HTTP/1.1 200 OK\r\nContent-length: 0\r\n\r\n".encode()

                    elif url and "cyberServ?img_name=" in url:
                        file_name = url.split("img_name=")[1]
                        print(f"File name: {file_name}\n")

                        with open(file_name, "wb") as f:
                            f.write(body)
                        ans = "HTTP/1.1 200 OK\r\nContent-length: 0\r\n\r\n".encode()

                    else:
                        ans = "HTTP/1.1 404 NOT FOUND\r\n\r\n".encode()
                else:
                    if url:
                        ans = build_reply(url)
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
