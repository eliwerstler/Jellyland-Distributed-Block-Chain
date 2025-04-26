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


def encode_msg(airport_name, tcp_rcv_port, seq_no, ack_no, msg_type, payload):
    """
    Convert fields into binary message format ready to send as TCP messages
    """
    format_string = '=9s20sIIIB'  # Format for struct
    # Packet header format (struct format).  
    # Different message types do not use all fields.
    # =   : This forces the struct to actual size, not memory aligned
    # 9s  : JELLYLAND                      (9-byte string) Immutable
    # 20s : Airport Name                   (20-byte string)
    # I   : TCP Listening Port             (4-byte unsigned integer)
    # I   : Sequence No.                   (4-byte unsigned integer)
    # I   : Acknowledgement No.            (4-byte unsigned integer)      
    # B   : Message Type                   (1 Byte unsigned integer) 
    #       10  REGISTER        - Peer Airport joining the network (airport.py -> tracker.py)
    #       20  DEREGISTER      - Peer airport leaving the network (airport.py -> tracker.py)
    #       30  DIRECTORY       - Peer directory Send ( tracker.py -> airport.py ). 
    #                             Also used by passenger_gui.py to request directory.
    #       40  PASSENGER       - Passenger Transaction (Arrival/Departure) GUI -> airport.py
    #       50  PROPOSAL        - Airport proposing a new block ( airport.py -> all other airport.py peers)
    #       60  APPROVAL        - Approve proposed block ( airport.py -> all other airport.py peers)
    #       70  REJECTION       - Reject proposed block ( airport.py -> all other airport.py peers)
    #       80  BLOCK           - Block ( airport.py -> all other airport.py peers)
    #       99  ANOMALY         - Mismatch in Chain (fork)  ( airport.py -> all other airport.py peers )
    # Payload (variable length)
 
    jellyland = b"JELLYLAND" # Make a bytes object
    airport_name_b = airport_name.encode('utf-8').ljust(20)[:20]  # Ensure airport name is 20 byte bytes object
    message =  struct.pack(format_string, jellyland, airport_name_b, tcp_rcv_port, seq_no, ack_no, msg_type)  # Newline added to indicate end message
    message += payload # Append payload to the string
    # Add a newline character to the end of the message
    #message += b'\n'  # Newline character to indicate end of message
    return message

def print_airports():
    """
    Print the current directory of airports to terminal
    """
    # Print the updated dictionary of airports to terminal
    print(f"\033[92mUpdated Airport Directory\n---------------------------------------\033[0m ")
    count = 1
    for airport, info in airport_directory.items():
        print(f"{count}) {airport.rstrip()} IP: {info['airport_ip']}/{info['airport_port']}")
        count += 1
    print(f"\033[92m---------------------------------------\033[0m ")

def register(airport_name, airport_port_no, action):
    """
    Registers the airport with the tracker
    Paramters:
    airport_name: Name of the airport
    airport_port_no: Port number of the airport
    action: Action to be performed (register or deregister)
    returns : True / False (action_okay)
    """
    action_okay = False   # Flag if the action succeeds
    global airport_directory, airport_connected, seq_no, ack_no
    payload = b''  # No payload for registration

    # Compile the message:
    msg_type = 10  # Reigster
    encoded_msg = encode_msg(airport_name, airport_port_no, seq_no, ack_no, msg_type, payload)
    print(f"Send {action} message to tracker.")

    # Create a TCP socket and send the registration message
    try:       
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_socket:   # Create a TCP socket
            send_socket.connect((tracker_addr, tracker_port)) # Connect to the tracker
            send_socket.sendall(encoded_msg) # Send the encoded message to the tracker                    
    except socket.error as e:   # Belongs to the 'try'
        print(f"\033[91m\nSocket error: {e}\nTracker not reachable at {tracker_addr}:{tracker_port}.\033[0m\n")
        sys.exit()


    # We should receive the directory back from the tracker
    seq_no, ack_no, node_name, tcp_rcv_port, tracker_ip, msg_type, payload=receive_message()

    if seq_no == None:
        print(f"\n\033[91mNo {action} response from tracker.\033[0m\n")
    else:
        print(f"\n\033[92mReceived response {msg_type} from tracker. \033[0m\n")

    # If we are registering, check the airport's name is now in the directory
    if msg_type == 30:  # Directory message

        if action == "register":
            # Check if the airport name has been added to the directory
            received_message = payload.decode("utf-8")  # Converts bytes string to string
            airport_directory = ast.literal_eval(received_message)            
            print_airports()  # Print the updated directory to terminal

            if airport_name.ljust(20)[:20] in airport_directory:
                print(f"\n\033[92m{airport_name.rstrip()} registered with tracker.\033[0m\n")    
                airport_connected = True
                return True
            else:
                print(f"\n\033[91mError: {airport_name.rstrip()} not in directory after registration.\033[0m\n")
                return False
        
        if action == "deregister":
            # Check if the airport name has been removed from the directory
            received_message = payload.decode("utf-8")  # Converts bytes string to string
            airport_directory = ast.literal_eval(received_message)            
            print_airports()  # Print the updated directory to terminal
            
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
    Returns seq_no, ack_no, node_name, tcp_rcv_port, msg_type, payload 
    This is a blocking function which is only used in the registration phase as 
    receiving messages is handled in the main loop by a threaded function.
    Do not enable threading until airport_connected is True.
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
        #print(f"\nPAYLOAD{payload.decode('utf-8')}\n")  # debug
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

    airport_connected = False  # Set True once airport 
    seq_no = random.randint(0, 2**32 - 1)  # Random sequence number

    ack_no = 0  # Initial acknowledgement number
    payload = b''  # No payload for registration

    # Create a dictionary to hold the peers/airport information which tracker.py sends us
    airport_directory = { }    
                          # 'airport_name': airport_name
                          # 'airport_port': airport_port    
                          # 'airport_ip': airport_ip    
    
    print(f"\n\033[37;42;1m [ Airport Passport Control Starting Up : {airport_name}/{airport_port_no}. Tracker: {tracker_port} ] \033[0m\n")
    register(airport_name, airport_port_no, "register")   # Register airport with tracker.py

    # Now the main program listening loop:
    # ***** This code is temporary !   
    # Needs to have a threading RX function that puts incoming data into a queue

    while True:  # Infinite loop to continuously listen for new messages
    # This is a placeholder loop - Need to add different responses to different message types (e.g. 30, 40, 50, 60, 70, 80)    
        response = b''  # Initialize response variable
        seq_no, ack_no, node_name, remote_port, remote_ip, msg_type, payload=receive_message()
        if msg_type != None:            
            received_message = payload.decode("utf-8")  # Converts bytes string to string
            if msg_type == 30:  # Directory message so update local airport directory
                received_message = payload.decode("utf-8")  # Converts bytes string to string
                airport_directory = ast.literal_eval(received_message)  
                print_airports()
            if msg_type == 40:  # Passenger Arrival or Departure
                print(f"AIRPORT NEEDS TO ADD TO BLOCKCHAIN: {received_message}\n")    

