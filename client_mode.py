import socket
import threading

def server_messages(client, address):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                print(f"Connection to {address} closed.")
                break
            print(message.decode())
        except Exception as e:
            print(f"Error: {e}")
            break
    print(f"\nChatting stopped.")
    exit()

def client_messages(client, username):
    while True:
        message = input()
        if message == "/exit":
            break
        final_message = f"<{username}> {message}"
        client.send(final_message.encode())
    print(f"\nChatting stopped.")
    exit()

def client_mode(username):
    address = input("Enter server address: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((address, 9777))
        print(f"Connected to {address}.")
    except ConnectionRefusedError:
        print(f"Connection to {address} refused.")
        exit()
    
    client_msg = threading.Thread(target=client_messages, args=(client, username))
    server_msg = threading.Thread(target=server_messages, args=(client, address), daemon=True)

    client_msg.start()
    server_msg.start()

    client_msg.join()
    server_msg.join()