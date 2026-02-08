import socket
import threading

def client_messages(connect, address):
    while True:
        try:
            message = connect.recv(1024)
            if not message:
                print(f"{address} has disconnected.")
                break
            print(f"<{address}> {message.decode()}")
        except Exception as e:
            print(f"Error: {e}")
    connect.close()
    print(f"\nChatting stopped.")

def server_messages(connect):
    while True:
        message = input("> ")
        if message == "/exit":
            break
        connect.send(message.encode())
    connect.close()
    print(f"\nChatting stopped.")

def server_mode():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9777))

    server.listen(1)
    print("Waiting for a connection...")
    connect, address = server.accept()
    print(f"{address} has connected.")

    client_msg = threading.Thread(target=client_messages, args=(connect, address), daemon=True)
    server_msg = threading.Thread(target=server_messages, args=(connect,), daemon=True)

    client_msg.start()
    server_msg.start()

    client_msg.join()
    server_msg.join()