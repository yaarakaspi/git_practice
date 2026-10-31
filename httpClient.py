import socket
import os

SERVER_PORT = 80
SERVER_IP = "127.0.0.1"


def main():
    client_socket = socket.socket()
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
    except Exception as e:
        client_socket.close()
        exit(f"Disconnected due to {str(e)}")
    while True:
        choice = input("Please choose: 1 - secret message, 2 - image, 3 - exit: ")  # getting user choice

        if choice not in ["1", "2", "3"]:
            print("Invalid input, please try again :(")
            continue

        if choice == "1":
            msg = input("Please enter your secret message to send: ")
            req = f"POST /cyberServ?secret HTTP/1.1\r\nContent-length: {len(msg.encode())}\r\n\r\n{msg}".encode()

        elif choice == "2":
            file_path = input("Please enter your image file path: ")

            # Check if file exists
            if not os.path.exists(file_path):
                print(f"File {file_path} does not exist, please try again :(")
                continue

            # Get name file
            file_name = os.path.basename(file_path)

            # Read image
            with open(file_path, "rb") as f:
                image_data = f.read()

            req = f"POST /cyberServ?img_name={file_name} HTTP/1.1\r\nContent-length: {len(image_data)}\r\n\r\n".encode()
            req += image_data  # adding image data separately because it's already encoded

        else:
            print("See you later!")
            break

        try:
            client_socket.send(req)
            response = client_socket.recv(1024).decode()
            print("\nServer reply:\n" + response)
        except Exception as e:
            print(f"Disconnected due to {str(e)}")
            break

        client_socket.close()


if __name__ == "__main__":
    main()

