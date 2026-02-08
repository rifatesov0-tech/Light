import socket
import threading

def client_messages(connect):
    while True:
        try:
            message = connect.recv(1024)
            if not message:
                print(f"Client has disconnected.")
                break
            print(message.decode())
        except Exception as e:
            print(f"Error: {e}")
            break
    print(f"\nChatting stopped.")
    exit()

def server_messages(connect, username):
    while True:
        message = input()
        if message == "/exit":
            break
        final_message = f"<{username}> {message}"
        connect.send(final_message.encode())
    print(f"\nChatting stopped.")
    exit()

def server_mode(username):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9777))

    server.listen(1)
    print("Waiting for a connection...")
    connect, address = server.accept()
    print(f"{address} has connected.")

    server_msg = threading.Thread(target=server_messages, args=(connect, username))
    client_msg = threading.Thread(target=client_messages, args=(connect,), daemon=True)

    server_msg.start()
    client_msg.start()

    server_msg.join()
    client_msg.join()