import random
from socket import *

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', 21002))

print("Server ready to receive requests")

# the sequence number expected for next message
expected_seq = 1
while True:
    # receive a message from the client
    message, address = server_socket.recvfrom(1024)

    # 30% chance the message is lost
    if random.random() < 0.30: continue

    # get the sequence number
    parts = message.decode().split(' ', 2)
    seq = int(parts[1])
    
    # if the sequence number is the one we expect then its correct
    if seq == expected_seq:
        print(f"Delivered: {message.decode()}")
        # increment the expected sequence only if the sequence number of the client's message was the same as the sequence number we expected to get
        expected_seq += 1
    else:
        # if the sequence is not equal, then the ACK was lost and the message was sent again from the client
        # in this case we can just ignore the message
        print(f"Duplicate ignored: SEQ {seq}")


    # 20% chance the ACK is lost
    if random.random() < 0.20: continue
    server_socket.sendto(("ACK " + str(seq)).encode(), address)
