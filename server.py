import threading
import socket


host = '127.0.0.1'  # Local host
port = 59000  # Random free port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []  # Each connection (i.e user) will have its own alias


def broadcast(message):
    """
    params ->
        1. message: The message to broadcast to all connected clients.

    note ->
        Function iterating through all connected clients, sending the message.
    """
    for client in clients:
        client.send(message)


# Function to handle clients' connections
def handle_client(client):
    """
    params  ->
        1. client: The client who is initiating a connection to the server.

    note ->
        Looping in a while loop.
        Wrapping code in Try - Catch block.

    """
    while True:
        try:
            # 1024 is maximus number of bytes  for a message the server may receive from a client
            message = client.recv(1024)

            # After successfully receiving the message from a client, we broadcast it to all connected users.
            broadcast(message)

        # In any case of errors, we wish to index the client who has the errors.
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()  # Closing the connection with the specific client.

            alias = aliases[index]
            aliases.remove(alias)  # Removing the alias as well.

            # Optionally, Announcing the leaving of a user.
            broadcast(f'{alias} has been disconnected!'.encode('utf-8'))
            break


# Main function to receive the clients connection
def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()  # Server waits for new connection.
        print(f'connection is established with {str(address)}')

        # Fetching new user's alias.
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)

        # Updating Aliases and Clients lists.
        aliases.append(alias)
        clients.append(client)

        # On server side, announcing the new fresh Rhino address, and it's alias
        print(f'The alias of {str(address)} is {alias}'.encode('utf-8'))

        # Broadcast to all users about the new baby rhino.
        broadcast(f'{alias} has connected! '.encode('utf-8'))

        # Sending connection message to the new baby rhino.
        client.send('you are now connected!'.encode('utf-8'))

        # Allocating new thread for new user. (Each user has its own thread)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
