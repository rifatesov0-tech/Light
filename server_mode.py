import socket
import threading
import json

clients = []
usernames = []

file_lock = threading.Lock()

def broadcast(message, sender=None):
        for client in list(clients):
            if client != sender:
                try:
                    client.send(message)
                except:
                    if client in clients:
                        clients.remove(client)
                    client.close()

def chat_messages(connect, address):
    global usernames
    checked_username = False
    current_username = None
    print_error = False
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

            if username == "SERVER":
                connect.send(json.dumps({
                    "username": "SERVER",
                    "message": "Username cannot be 'SERVER'. Please choose another one.",
                    "color": '\033[91m',
                }).encode("utf-8"))
                break

            if not checked_username:
                if username in usernames:
                    connect.send(json.dumps({
                        "username": "SERVER",
                        "message": "Username already taken. Please choose another one.",
                        "color": '\033[91m',
                    }).encode("utf-8"))
                    break
                else:
                    with file_lock:
                        usernames.append(username)
                    current_username = username
                    checked_username = True
            
            if message != None and message != "":
                broadcast_data = json.dumps({
                    "username": username,
                    "message": message,
                    "color": '\033[92m',
                }).encode("utf-8")

                broadcast(broadcast_data, connect)
            
                print(f"<{color}{username}\033[0m> {message}")

                save(message, username)
        except ConnectionAbortedError:
            break
        except Exception as e:
            connect.send(json.dumps({
                "username": "SERVER",
                "message": f"Error: {e}",
                "color": '\033[91m',
            }).encode("utf-8"))
            print_error = True
            if current_username != None:
                print(f"\n{current_username} has disconnected with error: {e}")
            else:
                print(f"\n{address} has disconnected with error: {e}")
            break
    connect.close()

    if connect in clients:
        clients.remove(connect)

    if current_username == None:
        print(f"{address} has left the chat.")
        
        if checked_username:
            broadcast(json.dumps({
                "username": "SERVER",
                "message": f"{address} has left the chat.",
                "color": '\033[91m',
            }).encode("utf-8"), "server")

    else:
        if current_username in usernames:
            with file_lock:
                usernames.remove(current_username)

        save(f"{current_username} has left the chat.")

        if not print_error:
            print(f"{current_username} has left the chat.")

        broadcast(json.dumps({
            "username": "SERVER",
            "message": f"{current_username} has left the chat.",
            "color": '\033[91m',
        }).encode("utf-8"), "server")

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
    usernames.append(username)

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

            broadcast(json.dumps({
                "username": "SERVER",
                "message": f"{address} has connected.",
                "color": '\033[92m',
            }).encode("utf-8"), "server")
    
            threading.Thread(target=chat_messages, args=(connect, address), daemon=True).start()
        except Exception as e:
            print(f"\nError: {e}")
            break
    clients = []
    usernames = [username]
    server.close()