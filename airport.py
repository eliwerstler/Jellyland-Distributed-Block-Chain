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
    Receives a message from the remote tracker
    """
    response = b''
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as rx_socket:
            rx_socket.settimeout(2)
            rx_socket.bind(('', airport_port_no))
            rx_socket.listen(1)
            conn, addr = rx_socket.accept()
            remote_ip, remote_src_port = addr
            response = conn.recv(2048)
    except socket.timeout:
        pass
    except socket.error as e:
        print(f"\nSocket error: {e}\n")
        sys.exit()
    finally:
        rx_socket.close()

    if response:
        payload = response[struct.calcsize('=9s20sIIIB'):]
        unpacked = struct.unpack('=9s20sIIIB', response[:struct.calcsize('=9s20sIIIB')])
        node_name   = unpacked[1].decode('utf-8').strip('\x00')
        tcp_rcv_port= unpacked[2]
        seq_no      = unpacked[3]
        ack_no      = unpacked[4]
        msg_type    = unpacked[5]
        return seq_no, ack_no, node_name, tcp_rcv_port, remote_ip, msg_type, payload
    else:
        return None, None, None, None, None, None, None

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
