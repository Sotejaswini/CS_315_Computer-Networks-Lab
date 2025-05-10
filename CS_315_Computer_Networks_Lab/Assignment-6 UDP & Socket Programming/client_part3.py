import socket
import ssl
from base64 import b64encode

# User information 
userEmail = "220010012@iitdh.ac.in"
userPassword = "uqxr oyer xnkb nvzi"   # Use the generated app password
userDestinationEmail = input("Enter Email Destination: ")
userSubject = input("Enter Subject: ")
userBody = input("Enter Message: ")
msg = '{}.\r\n I love computer networks!'.format(userBody)

# Choose a mail server (e.g., Google mail server) and call it mailserver
mailserver = "smtp.gmail.com"
mailport = 587  # Gmail SMTP port for sending emails (587 is for TLS)

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((mailserver, mailport))

# Receive server response (220)
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Account authentication
clientSocket.send("STARTTLS\r\n".encode())  # Start TLS encryption
clientSocket.recv(1024)
sslClientSocket = ssl.wrap_socket(clientSocket)  # Wrap the socket to use SSL/TLS

sslClientSocket.send("AUTH LOGIN\r\n".encode())  # Send AUTH LOGIN to authenticate
print(sslClientSocket.recv(1024))  # Print server response
sslClientSocket.send(b64encode(userEmail.encode()) + "\r\n".encode())  # Send email in base64
print(sslClientSocket.recv(1024))  # Print server response
sslClientSocket.send(b64encode(userPassword.encode()) + "\r\n".encode())  # Send password in base64
print(sslClientSocket.recv(1024))  # Print server response

# Send MAIL FROM command and print server response
mailFromCommand = f"MAIL FROM:<{userEmail}>\r\n"
sslClientSocket.send(mailFromCommand.encode())
recv2 = sslClientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response
rcptToCommand = f"RCPT TO:<{userDestinationEmail}>\r\n"
sslClientSocket.send(rcptToCommand.encode())
recv3 = sslClientSocket.recv(1024).decode()
print(recv3)
if recv3[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response
sslClientSocket.send("DATA\r\n".encode())
recv4 = sslClientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '354':
    print('354 reply not received from server.')

# Send message data
message = f"Subject: {userSubject}\r\nTo: {userDestinationEmail}\r\n{msg}\r\n"
sslClientSocket.send(message.encode())

# Message ends with a single period
sslClientSocket.send(".\r\n".encode())
recv5 = sslClientSocket.recv(1024).decode()
print(recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response
sslClientSocket.send("QUIT\r\n".encode())
recv6 = sslClientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '221':
    print('221 reply not received from server.')

# Close the socket
sslClientSocket.close()
