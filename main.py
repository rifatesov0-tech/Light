version = "0.3"
versionType = "Alpha"

print(f"Light {version} {versionType} - Created by wisted13\n")

print("Starting program...")

try:
    print("Loading modules...")
    from server_mode import server_mode
    from client_mode import client_mode
    print("Modules successfully loaded.\n")
except ImportError:
    print("Error loading modules.")
    exit()
except Exception as e:
    print(f"Error: {e}\n")
    exit()

try:
    print("Checking username...")
    with open("username.txt", "r") as f:
        username = f.read()
except FileNotFoundError:
    username = None
except Exception as e:
    print(f"Error: {e}\n")
    username = input("Enter your username: ")
    
if username == None:
    username = input("Enter your username: ")
    with open("username.txt","a") as f:
        f.write(username)

print(f"Your username: {username}")

try:
    while True:
        try:
            mode = int(input("\nEnter program mode (0, for exit,1 for Server, 2 for Client): "))
    
            if mode == 1:
                server_mode(username)
            elif mode == 2:
                client_mode(username)
            elif mode == 0:
                print("\nExiting program...")
                exit()
            else:
                print("\nUnknown mode.")
        except ValueError:
            print("\nInvalid input. Please enter a number.")
except Exception as e:
    print(f"\nError: {e}")
    exit()