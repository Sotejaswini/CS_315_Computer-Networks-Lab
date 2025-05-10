import socket

HOST = '0.0.0.0'  
PORT = 12345
BUFFER_SIZE = 1024

def extract_lines(filename, num_lines=10):
    """Extracts the first and last `num_lines` lines from a file."""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    first_lines = lines[:num_lines]
    last_lines = lines[-num_lines:] if len(lines) > num_lines else lines
    return first_lines + ['\n'] + last_lines  # Separating with a newline

def start_server():
    """Starts the server and handles client connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Server listening on {HOST}:{PORT}...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")

            # Receive the file and save it
            with open("received.txt", "wb") as file:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        break  # Stop when no more data is received
                    file.write(data)

            print("File received successfully. Extracting required lines...")

            # Read and extract lines
            extracted_lines = extract_lines("received.txt")
            response = "".join(extracted_lines)
            print("Extracted lines:\n", response)  # Debug print

            # Send extracted lines to client
            conn.sendall(response.encode())
            print("Sent extracted lines to client.")

if __name__ == "__main__":
    start_server()

