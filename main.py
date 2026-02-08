version = "0.1"
versionType = "Alpha"

print(f"Light {version} {versionType} - Created by wisted13\n")

print("Loading modules...")

try:
    from server_mode import server_mode
    from client_mode import client_mode

    print("Modules loaded successfully!")
except ImportError:
    print("Error loading modules.")
    exit()
except Exception as e:
    print(f"Error: {e}")
    exit()

try:
    mode = int(input("\nEnter program mode (1 for Server, 2 for Client): "))
    
    if mode == 1:
        server_mode()
        exit()
    elif mode == 2:
        client_mode()
        exit()
    else:
        print("Unknown mode.")
        exit()
except ValueError:
    print("Invalid input. Please enter a number.")
    exit()
except Exception as e:
    print(f"Error: {e}")
    exit()
