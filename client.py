import socket
import threading


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

soc.connect(("127.0.0.1", 1233))


def listen_server():
    while True:
        data = soc.recv(1024)
        print(data.decode())


def send_server():
    listen_thread = threading.Thread(target=listen_server)
    listen_thread.start()
    name = input('Enter your name: ').encode()
    soc.send(name)
    while True:
        message = input('Enter message: ').encode()
        soc.send(message)
        

if __name__ == '__main__':
    send_server()
