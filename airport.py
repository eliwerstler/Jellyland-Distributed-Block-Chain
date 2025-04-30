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

    #Check if the correct number of arguments are provided
    if len(sys.argv) != 5:
        print("\nUsage: python airport_register.py <airport_port_no> <airport_name> <tracker_port> <tracker_addr>\n")
        sys.exit(1)
    # Get the command line arguments
    airport_port_no = int(sys.argv[1])
    airport_name = sys.argv[2]
    tracker_port = int(sys.argv[3])
    tracker_addr = sys.argv[4]
    # Set some default variables / constants
    airport_connected = False  # Set True once airport 
    seq_no = random.randint(0, 2**32 - 1)  # Random sequence number
    ack_no = 0  # Initial acknowledgement number
    payload = b''  # No payload for registration
    difficulty = 4 # The number of leading zeros in the hash for proof of work
    mempool = {}   # This is a queue of pending passenger transactions; a dictionary of dictionaries
    blockchain = [] # This is a list of dictionaries where we store the chain (multiple blocks) - A LIST NOW NOT A DICT
    block_index = 0  # Starting block index (height)

    # Generate key pair
    private_pem, public_pem = generate_key_pair()  # Generate public/private key pair   
    airport_directory = { }    # Create a dictionary to hold the peers/airport information which tracker.py sends us
                          # 'airport_name': airport_name
                          # 'airport_port': airport_port    
                          # 'airport_ip': airport_ip   
                          # 'public_key': public_pem.decode('utf-8')  # Public key in PEM format 
    
    print(f"\n\033[37;42;1m [ Airport Peer Initialind : {airport_name}/{airport_port_no}. Tracker: {tracker_port} ] \033[0m\n")

    register(airport_name, airport_port_no, public_pem, "register")   # Register airport with tracker.py
  
    # TODO: Placeholder to request existing blockchain from any peer

    # NOTE : Incoming messages may be concatenated, so we need to split them if
    # more than one comes in at once due to TCP streading. Each message starts with
    # the JELLYLAND header and ends with a newline character.

    # Now the main program listening loop:
    while True:  # listen for new messages and check mempool for any new transactions
   
        #response = b''  # Initialize response variable
        # Listen to TCP socket for incoming messages.  
        seq_no, ack_no, node_name, remote_port, remote_ip, msg_type, payload=receive_message()
        blockchain_size = len(blockchain)  # Get the height/size of the blockchain (number of blocks)
        if msg_type != None:            
            received_message = payload.decode("utf-8").rstrip("\n")  # Removes \n and converts bytes string to string
            #print(f"Received: {received_message}\n")   # Debug only

            if msg_type == 30:  # Directory message so update local airport directory
                received_message = payload.decode("utf-8")  # Converts bytes string to string
                airport_directory = ast.literal_eval(received_message)  
                airport_count = print_airports()  # Print the updated directory to terminal

            if msg_type == 40:  # Passenger Arrival or Departure
                received_message = payload.decode("utf-8")  # Converts bytes string to string.    NOTE - ELI SWAPPED THIS LINE WITH THE NEXT AROUND... ??
                passenger_trans = ast.literal_eval(received_message)  # Convert the passenger data back into a dictionary
                mempool_push(passenger_trans)  # Add the transaction to the mempool

            if msg_type == 50:  # Block proposal from another airport   
                # Check if the block is valid - signature okay, hash okay, 
                # If valid, add it to the blockchain but how do we mark it as 'probation' ??
                # If invalid, just drop it?
                block = payload.decode("utf-8")
                print(f"Received block proposal from {node_name.rstrip()}")
                             

            # Pull all transactions from mempool with status 'Ready' and create a new proposed block:
            mem_ready = ready_blocks()  # Pull all 'Ready' transactions from mempool
            if len(mem_ready) > 0: 
                block = create_block(mem_ready)  
                idx, status, btime, csz, ph, data, nonce, bhash = read_block(block_str)
                print(f"\nBlock added to blockchain: {idx}")
                # Right now we don't record which block each transaction goes into. We might need to in 
                # case a bloack is rejected/dropped and we need to add the included transactions again.
                blockchain.append(block)
                propose_block(block) # Propose new block to all other peer airports

                
  
