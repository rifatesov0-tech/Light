version = "0.3"
versionType = "Alpha"

print(f"Light {version} {versionType} - Created by wisted13\n")

print("Starting program...")

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
else:
    pass

print(f"Your username: {username}")

try:
    mode = int(input("\nEnter program mode (1 for Server, 2 for Client): "))
    
    if mode == 1:
        print("\nLoading module...")
        from server_mode import server_mode
        print("Module successfully loaded.\n")
        server_mode(username)
        exit()
    elif mode == 2:
        print("\nLoading module...")
        from client_mode import client_mode
        print("Module successfully loaded.\n")
        client_mode(username)
        exit()
    else:
        print("\nUnknown mode.")
        exit()
except ImportError:
    print("Error loading module.")
    exit()
except ValueError:
    print("\nInvalid input. Please enter a number.")
    exit()
except Exception as e:
    print(f"\nError: {e}")
    exit()