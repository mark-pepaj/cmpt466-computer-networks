import time
from socket import *

server_name = "localhost"
server_port = 21002

client_socket = socket(AF_INET, SOCK_DGRAM)
client_socket.settimeout(0.5)


# number of packets sent
packets_sent = 0

# timeout count and limit
timeouts = 0
max_attempts = 10

# number of messages to send
n = 10

# sequence number starts at 1
seq = 1

# the time at the start of the program
start_time = time.time()

# while loop from 1 to n
while seq <= n:
    message = f"Ping {seq}"
    print(f"Message: {message}")

    send_time = time.time()

    # send the message to the server
    client_socket.sendto(message.encode(), (server_name, server_port))
    packets_sent += 1
    try:
        # receive the response from the server
        response_message, _ = client_socket.recvfrom(2048)
        RTT = time.time() - send_time

        # only increment the sequence if the ACK was received
        seq += 1
        
        # zero the timeout counter
        timeouts = 0

        # print the response message
        print(f"response: {response_message.decode()}")
        print(f"RTT: {RTT:.6f}s")
    except:
        # increment the timeout counter
        timeouts += 1

        # if the message has no ACK after 10 attempts then stop the program
        if timeouts == max_attempts:
            print("Giving up\n")
            break

        # if timeouts is less than 10 we can make another attempt, printing that there was a timeout
        print("Timed out, resending")
    print("")

print("Summary:")
print(f"Number of messages: {n}")
print(f"Number of packets Sent: {packets_sent}")
print(f"Number of packets retransmitted: {packets_sent - n}")
print(f"Total Time: {time.time() - start_time:.6f}s")
client_socket.close()

