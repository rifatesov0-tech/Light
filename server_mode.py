import socket
import threading
import json

clients = []

file_lock = threading.Lock()

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def chat_messages(connect, address):
    while True:
        try:
            recv_data = connect.recv(1024)

            if not recv_data:
                print(f"{address} has disconnected.")
                break

            data = json.loads(recv_data.decode('utf-8'))

            username = data["username"]
            message = data["message"]
            color = "\033[92m"

            broadcast_data = {
                "username": username,
                "message": message,
                "color": '\033[92m',
            }

            broadcast(json.dumps(broadcast_data).encode("utf-8"), connect)
            
            print(f"<{color}{username}\033[0m> {message}")

            save(message, username)
        except ConnectionAbortedError:
            print(f"{address} has disconnected")
            break
        except Exception as e:
            print(f"Error: {e}")
            break
    save("\n---[CHATTING STOPPED]---\n\n")
    print("\nChatting stopped.")

def send_message(username):
    while True:
        message = input()

        if message == "/exit":
            break

        data = {
            "username": username,
            "message": message,
            "color": '\033[31m',
        }

        broadcast((json.dumps(data).encode("utf-8")), "server")

        save(message, username)
    save("\n---[CHATTING STOPPED]---\n\n")
    print("\nChatting stopped.")

def save(message, sender=None):
    if sender != None:
        with file_lock:
            with open("history.txt","a") as h:
                h.write(f"<{sender}> {message}\n")
                h.flush()
    else:
        with file_lock:
            with open("history.txt","a") as h:
                h.write(message)
                h.flush()

def server_mode(username):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = int(input("Enter server port: "))

    server.bind(('0.0.0.0', port))

    server.listen(1)
    print("Waiting for a connection...")

    threading.Thread(target=send_message, args=(username,), daemon=True).start()

    while True:
        try:
            connect, address = server.accept()
            clients.append(connect)
            print(f"{address} has connected.")
    
            threading.Thread(target=chat_messages, args=(connect, address), daemon=True).start()
        except Exception as e:
            print(f"\nError: {e}")
            break
    server.close()