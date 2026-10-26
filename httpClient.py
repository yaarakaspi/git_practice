import socket

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
        choice = input("Please choose: 1 - secret message, 2 - image, 3 - exit")
        # getting
        if choice not in ["1", "2", "3"]:
            print("Invalid input, please try again :(")
            continue
        if choice == "1":
            msg = input("Please enter your secret message to send: ")
            req = f"POST /cyberServ?secret HTTP/1.1\r\nContent-length: {len(msg)}\r\n\r\n{msg}".encode()
        elif choice == "2":
            msg = input("Please enter your image file path: ")
            #TODO check if file is valid then send
        else:
            print("See you later!")
            break


    client_socket.close()



if __name__ == "__main__":
    main()

