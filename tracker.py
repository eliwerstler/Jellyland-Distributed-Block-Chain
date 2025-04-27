# tracker.py
# Airport Registration 

import socket 
import random
import struct
import time
import datetime
import sys

def encode_msg(airport_name, tcp_rcv_port, seq_no, ack_no, msg_type, payload):
    """
    Convert fields into binary message format ready to send 
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
    message =  struct.pack(format_string, jellyland, airport_name_b, tcp_rcv_port, seq_no, ack_no, msg_type)
    message += payload # Append payload to the string
    return message

def print_airports():
    """
    Print the current directory of airports to terminal
    """
    # Print the updated dictionary of airports to terminal
    print(f"\033[92mUpdated Airport Directory\n---------------------------------------\033[0m ")
    count = 1
    for airport, info in airport_directory.items():
        print(f"{count}) {airport.rstrip()} ({info['airport_ip']}:{info['airport_port']})")
        count += 1
    print(f"\033[92m---------------------------------------\033[0m ")

def receive_message():
    """
    Receives a message from the TCP socket
    Returns seq_no, ack_no, node_name, tcp_rcv_port, msg_type, payload 
    This is a blocking function which is only used in the registration phase as 
    receiving messages is handled in the main loop by a threaded function.
    Do not enable threading until airport_connected is True.
    """
    global tracker_port
    response = b''  # Initialize response variable
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as rx_socket:   # Open the TCP socket connection         
            #client_socket.connect((tracker_addr, tracker_port)) # Connect to the tracker
            #client_socket.settimeout(5)  # Set a timeout for receiving data
            #response = client_socket.recv(1024)  # Receive the response from the tracker

            rx_socket.settimeout(2)  # Timeout for receiving airport directory back from tracker, else raises an exception
            rx_socket.bind(('', tracker_port))  
            rx_socket.listen(1)  # Listen for incoming connections            
            conn, addr = rx_socket.accept()  # Accept an incoming connection
            remote_ip, remote_src_port = addr  # Get the sender's IP address and src. port number
            response = conn.recv(2048)  # Receive the response from the remote host
    except socket.timeout:
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
        # Unpack the header fields
        unpacked_data = struct.unpack('=9s20sIIIB', response[0:struct.calcsize('=9s20sIIIB')])    
        node_name = unpacked_data[1].decode('utf-8').strip('\x00')  # Decode and strip padding
        remote_port = unpacked_data[2]
        seq_no = unpacked_data[3]
        ack_no = unpacked_data[4]
        msg_type = unpacked_data[5]
        #print(f"\033[92mReceived message:\033[0m {payload.decode('utf-8').strip('\x00')}")  # Decode and strip padding
        return seq_no, ack_no, node_name, remote_port, remote_ip, msg_type, payload 
    else:
        return None, None, None, None, None, None, None  # Return None if no response is received

def send_directory(ip, port):
    """
    Send the current airport directory to one remote host (passenger GUI)
    """
    # Create a TCP socket for sending the message
    try:  # Traps socket errors 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
            send_sock.connect((ip, port))                        
            payload = str(airport_directory).encode('utf-8')  # Convert the dictionary to bytes    
            encoded_msg = encode_msg("Tracker", port, seq_no, ack_no, msg_type, payload)
            print(f"Sending airport directory to {ip}:{port}.")
            send_sock.sendall(encoded_msg)
            return True  # Return True if successful
    except socket.error as e:   # Belongs to the 'try'
        print(f"\n\033[91mSocket Error. Unable to update {ip}:{port}:  {e}.\n\033[0m\n")
        return False  # Return False if unable to connect
    
def update_airports():
    """
    Send the updated airport directory to all peer airports
    in the directory.  This is called when a new airport registers or deregisters
    or when tracker fails to update a peer.
    Returns : True or False (Success or Failure)
    """
    # Check that airport directory isn't empty
    if not airport_directory:    # If the directory is empty, return False
        print("\nNo airports in directory. No updates send.\n")
        return True  # Return True so that the outer loop will exit
        
    print(f"Sending airport directory to: ", end="")    
    # Loop through the airport_directory dictionary and send the updated list to each airport
    msg_type = 30  # message type : DIRECTORY
    acount = 0
    for airport, info in airport_directory.items():
            # Create a TCP socket for sending the message
            try:  # Traps socket errors 
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_sock:
                    send_sock.connect((info['airport_ip'], info['airport_port']))                        
                    payload = str(airport_directory).encode('utf-8')  # Convert the dictionary to bytes    
                    encoded_msg = encode_msg("Tracker", info['airport_port'], seq_no, ack_no, msg_type, payload)
                    print(f"{airport.rstrip()}  ", end="")  
                    send_sock.sendall(encoded_msg)
                    
                    update_okay = True  # Set to True so that outer loop will exit if all updates are successful
            except socket.error as e:   # Belongs to the 'try'                
                print(f"\n\033[91mUnable to update {airport.rstrip()}:  {e}.\nRemoving {airport.rstrip()} from directory.\033[0m\n")
                # Remove the airport from the directory if unable to connect
                del airport_directory[airport]
                return False  # This will hands control back to the outer loop which will imediately call update_airports() again with the updated directory
    print("") #new line        
    return True  # Return True if all updates were successful, False otherwise so that the 


if __name__ == '__main__':

    #Check if the correct number of arguments are provided
    if len(sys.argv) != 2:
        print("\nUsage: python tracker.py <tracker_port_no>\n")
        sys.exit(1)
    # Get the command line arguments
    tracker_port = int(sys.argv[1])

    seq_no = random.randint(0, 2**32 - 1)  # Random sequence number
    ack_no = 0  # Initial acknowledgement number
    payload = b''  # No payload for registration

    # Create a dictionary to hold the peers/airport information
    airport_directory = { }    # Will store peers once they register
                          # 'airport_name': airport_name
                          # 'airport_port': airport_port    
                          # 'airport_ip': airport_ip    }

    print(f"\n\033[37;42;1m [ Tracker Running on Port {tracker_port} ] \033[0m\n")

    # Loop, waiting for airport registration requests
    print(f"Tracker listening on port {tracker_port}.")
    while True:

        seq_no, ack_no, airport_name, airport_port, airport_ip, msg_type, payload = receive_message()  # Receive a message from an airport. Blocking with timeout

        if seq_no is None:
            #print("\nTimed out waiting for message. Continue waiting.\n")
            continue  # No message received, back to top of infinite loop

        print(f"Received Message (Type {msg_type}) from {airport_name.rstrip()}  listening on {airport_ip}:{airport_port}. ")

        # tracker.py will receive one of three types of messages:
        #       10  REGISTER   - Peer Airport joining the network (airport.py -> tracker.py)
        #       20  DEREGISTER - Peer airport leaving the network (airport.py -> tracker.py)
        #       30  QUERY      - Peer list request ( GUI -> tracker.py -> GUI ) (Also reply)

        if msg_type == 10:   #  Airport Registration. Add the airport to the dictionary
            #airport_directory[airport_name] = { 'airport_port': airport_port, 'airport_ip': airport_ip }  # Add the airport to the dictionary}                
            airport_directory[airport_name] = { 'airport_port': airport_port, 'airport_ip': airport_ip, 'public_key': payload }  # Add the airport to the dictionary}                


        if msg_type == 20:   #  Airport De-registration. Remove the airport from the dictionary
            del airport_directory[airport_name]  # Delete the airport from the dictionary}
        
        if msg_type == 30:   #  Directory Request from passenger GUI. Send the directory to the GUI 
            print(f"\n\033[92mReceived directory request from passenger GUI ({airport_ip}:{airport_port})\033[0m\n")
            send_directory(airport_ip, airport_port)   # These are the IP/port of the passenger GUI, not an airport.

        if msg_type != 30:
            print_airports()  # Print the updated dictionary of airports to terminal            
        
        update_okay = False
        while update_okay == False:  # we loop until all updates are okay
            update_okay = update_airports()    

