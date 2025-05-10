import socket

SERVER_IP = '127.0.0.1'  
PORT = 12345
BUFFER_SIZE = 1024
FILE_PATH = "alice.txt"

def send_file():
    """Connects to the server and sends the file."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_IP, PORT))
        print("Connected to server.")

        with open(FILE_PATH, "rb") as file:
            while chunk := file.read(BUFFER_SIZE):
                client_socket.sendall(chunk)

        # Close writing to indicate end of file
        client_socket.shutdown(socket.SHUT_WR)

        print("File sent. Waiting for server response...")

        # Receive response from server
        data = b""
        while True:
            chunk = client_socket.recv(BUFFER_SIZE)
            if not chunk:
                break
            data += chunk

        print("\nReceived from server:\n")
        print(data.decode())

if __name__ == "__main__":
    send_file()
