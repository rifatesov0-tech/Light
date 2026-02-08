import socket
import threading

def server_messages(client, address):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                print(f"Connection to {address} closed.")
                break
            print(f"<{address}> {message.decode()}")
        except Exception as e:
            print(f"Error: {e}")
            break
    client.close()
    print(f"\nChatting stopped.")

def client_messages(client):
    while True:
        message = input("> ")
        if message == "/exit":
            break
        client.send(message.encode())
    client.close()
    print(f"\nChatting stopped.")

def client_mode():
    address = input("Enter server address: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((address, 9777))
        print(f"Connected to {address}.")
    except ConnectionRefusedError:
        print(f"Connection to {address} refused.")
        exit()
    
    server_msg = threading.Thread(target=server_messages, args=(client, address), daemon=True)
    client_msg = threading.Thread(target=client_messages, args=(client,), daemon=True)

    server_msg.start()
    client_msg.start()

    server_msg.join()
    client_msg.join()