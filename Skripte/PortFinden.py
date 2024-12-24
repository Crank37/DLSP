import socket
import random

def find_unused_port():
    while True:
        port = random.randint(49152, 65535)  # Dynamischer Port-Bereich
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("192.168.2.81", port))
                return port  # Port ist unbenutzt
            except OSError:
                continue  # Port ist belegt, erneut versuchen

random_unused_port = find_unused_port()
print(f"Random unused port: {random_unused_port}")