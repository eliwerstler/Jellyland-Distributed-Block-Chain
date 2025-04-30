# Airport Registration PoC
#
# airport.py

import socket 
import random
import struct
import time
import datetime
import sys
import ast
import hashlib
import json
import threading

# Install cryptography extension to use ECDSA: 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature, encode_dss_signature
from cryptography.exceptions import InvalidSignature

# Blockchain core routines now live in chain.py
from chain import (
    generate_key_pair,
    compute_hash,
    format_field,
    restore_field,
    read_block,
    create_block,
    proof_of_work,
    is_valid_proof,
    mempool_push,
    mempool_pull,
    ready_blocks,
)

def encode_msg(airport_name, tcp_rcv_port, seq_no, ack_no, msg_type, payload):
    """
    Convert fields into binary message format ready to send as TCP messages
    """
    format_string = '=9s20sIIIB'  # Format for struct
    jellyland = b"JELLYLAND"
    airport_name_b = airport_name.encode('utf-8').ljust(20)[:20]
    message = struct.pack(format_string,
                          jellyland,
                          airport_name_b,
                          tcp_rcv_port,
                          seq_no,
                          ack_no,
                          msg_type)
    message += payload
    #message += b'\n'
    return message

def print_airports():
    """
    Print the current directory of airports to terminal
    """
    print(f"\033[92mUpdated Airport Directory\n---------------------------------------\033[0m ")
    acount = 0
    for airport, info in airport_directory.items():
        acount += 1
        print(f"{acount}) {airport.rstrip()} IP: {info['airport_ip']}/{info['airport_port']}, Public Key: {info['public_key']}")
    print(f"\033[92m---------------------------------------\033[0m ")
    return acount

def register(airport_name, airport_port_no, payload, action):
    """
    Registers the airport with the tracker
    """
    global airport_directory, airport_connected, seq_no, ack_no
    payload = public_pem

    msg_type = 10  # REGISTER
    encoded_msg = encode_msg(airport_name, airport_port_no, seq_no, ack_no, msg_type, payload)
    print(f"Send {action} message to tracker.")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_socket:
            send_socket.connect((tracker_addr, tracker_port))
            send_socket.sendall(encoded_msg)
    except socket.error as e:
        print(f"\033[91m\nSocket error: {e}\nTracker not reachable at {tracker_addr}:{tracker_port}.\033[0m\n")
        sys.exit()

    seq_no, ack_no, node_name, tcp_rcv_port, tracker_ip, msg_type, payload = receive_message()

    if seq_no is None:
        print(f"\n\033[91mNo {action} response from tracker.\033[0m\n")
    else:
        print(f"\n\033[92mReceived response {msg_type} from tracker. \033[0m\n")

    if msg_type == 30:
        received_message = payload.decode("utf-8")
        airport_directory = ast.literal_eval(received_message)
        print_airports()

        if action == "register":
            if airport_name.ljust(20)[:20] in airport_directory:
                print(f"\n\033[92m{airport_name.rstrip()} registered with tracker.\033[0m\n")
                airport_connected = True
                return True
            else:
                print(f"\n\033[91mError: {airport_name.rstrip()} not in directory after registration.\033[0m\n")
                return False

        if action == "deregister":
            if airport_name.ljust(20)[:20] not in airport_directory:
                print(f"\n\033[92m{airport_name.rstrip()} deregistered from tracker.\033[0m\n")
                airport_connected = False
                return True
            else:
                print(f"\n\033[91mError: {airport_name.rstrip()} still in directory after deregistration.\033[0m\n")
                return False

def receive_message():
    """
    Receives a message from the remote host
    Returns seq_no, ack_no, node_name, tcp_rcv_port, msg_type, payload 
    This is a blocking function which is only used in the registration phase as 
    receiving messages is handled in the main loop by a threaded function.
    """
    response = b''  # Initialize response variable
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as rx_socket:   # Open the TCP socket connection         
            rx_socket.settimeout(2)  # Timeout for receiving airport directory back from tracker, else raises an exception
            rx_socket.bind(('', airport_port_no))  # Bind to the airport's port
            rx_socket.listen(1)  # Listen for incoming connections
            #print(f"Listening for tracker response on port {airport_port_no}.")
            conn, addr = rx_socket.accept()  # Accept an incoming connection
            remote_ip, remote_src_port = addr  # Get the sender's IP address and src. port number
            response = conn.recv(2048)  # Receive the response from the remote host
         
    except socket.timeout:
        #print("\nSocket Timed Out waiting. Continue to wait.\n ")
        pass
    except socket.error as e:
        print(f"\nSocket error: {e}\n")
        sys.exit()   # For Debug only
    finally:
        # Close the socket
        rx_socket.close()

    if response:
        # Unpack the received message
        payload = response[struct.calcsize('=9s20sIIIB'):]  # Extract the payload from the response
        #print(f"\n\033[93mPAYLOAD{payload.decode('utf-8')}\033[0m\n")  # debug
        # Unpack the header fields
        unpacked_data = struct.unpack('=9s20sIIIB', response[0:struct.calcsize('=9s20sIIIB')])    
        node_name = unpacked_data[1].decode('utf-8').strip('\x00')  # Decode and strip padding
        tcp_rcv_port = unpacked_data[2]
        seq_no = unpacked_data[3]
        ack_no = unpacked_data[4]
        msg_type = unpacked_data[5]
        return seq_no, ack_no, node_name, tcp_rcv_port, remote_ip, msg_type, payload 
    else:
        return None, None, None, None, None, None, None   # Return None if no response is received
        
def get_last_hash():
    """
    Get the last hash (the most recently added block) from the blockchain
    Returns: The previous index no. (int) and hash (string)
    """
    if len(blockchain) == 0:
        return 0, "0"  #  First block so no previous block. Will be stored as 64 chars in block.
    else:        
        last_block = blockchain[len(blockchain) - 1]  # Get the last block in the blockchain
        data_size = restore_field(last_block[91:95], "int")   # Need  data field size to locate relative position of hash
        last_hash=restore_field(block[103+data_size:], "str")  # Hash field
        last_index=restore_field(last_block[0:4], "int")   # Index field
        return last_index, last_hash  # Return the hash of the last block
        
def propose_block(block):
    """
    Propose new block to all other airport peers
    Parameters: block
    """
    for airport, info in airport_directory.items():
        ip=info['airport_ip']
        port=info['airport_port']
        if port != airport_port_no:
            # Compile the message:
            msg_type = 50  # Propose block
            seq_no = random.randint(0, 2**32 - 1)  # Random sequence number
            ack_no = 0
            #payload = block.encode('utf-8')  # Convert block to bytes
            encoded_msg = encode_msg(airport_name, airport_port_no, seq_no, ack_no, msg_type, payload)
            print(f"Proposing to : {airport.rstrip()}")
            # Create a TCP socket and send the registration message
            try:       
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_socket:   # Create a TCP socket
                    send_socket.connect((ip, port)) # Connect to the remote peer
                    send_socket.sendall(encoded_msg) # Send the message
            except socket.error as e:   # Belongs to the 'try'
                print(f"\033[91m\nSocket error: {e}\nTracker not reachable at {tracker_addr}:{tracker_port}.\033[0m\n")
        else:
            print("Skipping Self")

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("\nUsage: python airport_register.py <airport_port_no> <airport_name> <tracker_port> <tracker_addr>\n")
        sys.exit(1)

    airport_port_no = int(sys.argv[1])
    airport_name    = sys.argv[2]
    tracker_port    = int(sys.argv[3])
    tracker_addr    = sys.argv[4]

    airport_connected = False
    seq_no = random.randint(0, 2**32 - 1)
    ack_no = 0
    payload = b''

    # Use chain.py’s keygen
    private_pem, public_pem = generate_key_pair()

    airport_directory = {}
    mempool        = {}
    blockchain     = {}
    block_index    = 0

    print(f"\n\033[37;42;1m [ Airport Peer Initialized: {airport_name}/{airport_port_no}. Tracker: {tracker_port} ] \033[0m\n")

    register(airport_name, airport_port_no, public_pem, "register")

    while True:
        seq_no, ack_no, node_name, remote_port, remote_ip, msg_type, payload = receive_message()
        if msg_type is not None:
            if msg_type == 30:
                received_message = payload.decode("utf-8")
                airport_directory = ast.literal_eval(received_message)
                print_airports()

            if msg_type == 40:
                passenger_trans = ast.literal_eval(payload.decode("utf-8"))
                print(f"Received {passenger_trans['Action']} transaction")
                mempool_push(passenger_trans)

            mem_ready = ready_blocks()
            if mem_ready:
                print(f"\nPulled these ready transactions from mempool: {mem_ready}")
                time.sleep(0.5)

                chain_size    = len(blockchain)
                prev_hash     = "EEEE"  # placeholder
                block_str     = create_block(mem_ready, block_index, chain_size, prev_hash, private_pem)
                print(f"\nBlock Created and validated: {is_valid_proof(block_str, public_pem)}")

                idx, status, btime, csz, ph, data, nonce, bhash = read_block(block_str)
                print(f"Block Index: {idx}, Status: {status}. Created: {btime}, Chain Size: {csz}, Previous Hash: {ph}, Block Hash: {bhash}\n")

                blockchain[block_index] = block_str
                block_index += 1
                print(f"\nBlock added to blockchain: {block_index}")
                print(f"Current blockchain: {blockchain}")
