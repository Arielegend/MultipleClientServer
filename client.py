import threading
import socket

# Each new baby Rhino, once logged in, needs to choose an alias.
user_alias = input('Dear rhino, Choose your alias!\n\t')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Random first new available port.
client.connect(('127.0.0.1', 59000))


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(user_alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break


def client_send():
    while True:
        message = f'{user_alias}: {input("")}'
        client.send(message.encode('utf-8'))


# Thread for client receiving messages.
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

# Thread for client sending messages.
send_thread = threading.Thread(target=client_send)
send_thread.start()
