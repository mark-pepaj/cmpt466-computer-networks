from socket import *
import time

server_name = 'localhost'
server_port = 21002

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(1)

for seq in range(1, 11):
    message = f'Ping {seq}'
    print(f'Message: {message}')

    send_time = time.time()

    client_socket.sendto(message.encode(), (server_name, server_port))
    try:
        response_message, server_address = client_socket.recvfrom(2048)
        RTT = time.time() - send_time
        print(f'Round Trip Time: {RTT} seconds')
    except:
        print("Request timed out")
client_socket.close()

