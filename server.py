import socket
import threading

all_client = []


def send_message_all(name, data, current_user):
    for user in all_client:
        if current_user != user:
            user.send(f'{name} send: {data}'.encode())


def new_user_in_chat(name, current_user):
    for user in all_client:
        if current_user != user:
            user.send(f'User {name} entered the chat...'.encode())


def listen_user(user):
    name = user.recv(1024).decode()
    new_user_in_chat(name, user)
    while True:
        data = user.recv(2048).decode()
        print(f'LOG INFO: user {name} send new message')
        send_message_all(name, data, user)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 1233))
        s.listen(4)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        while True:
            user_socket, address = s.accept()

            print(f'LOG INFO: User {address} connected')

            all_client.append(user_socket)
            listen_concurrently = threading.Thread(
                target=listen_user,
                args=(user_socket,))
            listen_concurrently.start()


if __name__ == '__main__':
    start_server()
