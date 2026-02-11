import socket
import threading
import json

file_lock = threading.Lock()

def chat_messages(client, address):
    while True:
        try:
            recv_data = client.recv(1024)

            if not recv_data:
                print(f"Connection to {address} closed.")
                break

            data = json.loads(recv_data.decode("utf-8"))

            print(f"<{data['color']}{data['username']}\033[0m> {data['message']}")

            save(data["message"], data["username"])
        except ConnectionAbortedError:
            print(f"Connection to {address} closed.")
            break
        except Exception as e:
            print(f"Error: {e}")
            break
    save("\n---[CHATTING STOPPED]---\n\n")
    print("\nChatting stopped.")

def send_message(client, username):
    while True:
        message = input()

        if message == "/exit":
            break

        data = {
            "username": username,
            "message": message,
        }

        client.send(json.dumps(data).encode("utf-8"))

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

def client_mode(username):
    address = input("Enter server address: ")
    try:
        port = int(input("Enter server port: "))
    except ValueError:
        print("Invalid port number.")
        exit()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((address, port))
        print(f"Connected to {address}.")
    except ConnectionRefusedError:
        print(f"Connection to {address} refused.")
        exit()
    except Exception as e:
        print(f"Error: {e}")
    
    client_msg = threading.Thread(target=send_message, args=(client, username))
    server_msg = threading.Thread(target=chat_messages, args=(client, address), daemon=True)

    client_msg.start()
    server_msg.start()

    client_msg.join()