# pasenger_gui.py
"""
Usage:  passenger_gui.py <tracker_port> <tracker_addr>

This script presents the passenger with a GUI to select which airport they are arriving at or departing from.
and also select their own passport from a list of 8 hardcoded identities of mixed nationalities (citizen of Jellyland or not).
The list of online (available) airports is received over TCP from the tracker with a message type of 25 (PEERLIST).
Once a person and airport is selecting, a TCP message is sent to the airport node to notify it of the passenger's arrival or departure.
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import sys
import struct
import socket
import ast
import time
import json  
import uuid

def send_message(ip, port, msg_type, payload):
    seq_no = 0  # Not used
    ack_no = 0  # Not used
    encoded_msg = encode_msg("GUI", gui_port, seq_no, ack_no, msg_type, payload)
    # Create a TCP socket and send the registration message
    try:       
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_socket:   # Create a TCP socket
            send_socket.connect((ip,port)) # Connect to the tracker
            send_socket.sendall(encoded_msg) # Send the encoded message to the tracker    
            #print(f"Send message to {ip}:{port}: {encoded_msg}.")    # debug only
    except (socket.error, ConnectionResetError, BrokenPipeError, ConnectionRefusedError) as e:   # Belongs to the 'try'
        print(f"\033[91m\nSocket error: {e}\nRemote host not reachable at {ip}:{port}.\033[0m\n")
        return False
    return True

def encode_msg(airport_name, tcp_rcv_port, seq_no, ack_no, msg_type, payload):
    """
    Convert fields into binary message format ready to send as TCP messages
    """
    format_string = '=9s20sIIIB'  # Format for struct
    jellyland = b"JELLYLAND" # Make a bytes object
    airport_name = airport_name.encode('utf-8').ljust(20)[:20]  # Ensure airport name is 20 byte bytes object and encode it        
    message =  struct.pack(format_string, jellyland, airport_name, tcp_rcv_port, seq_no, ack_no, msg_type)  # Newline added to indicate end message
    if payload:   # If payload not empty
        serialised_payload = json.dumps(payload)  # Convert the payload dictionary to a JSON string suitable for sending over TCP
        payload = serialised_payload.encode('utf-8')
    message += payload # Append payload to the string
    message += b'\n'  # Newline character to indicate end of message
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

def get_passports():
    """
    Hardcodes the sample passengers' details. 
    returns : dictionary of passports
    """
    passports = [
        {"Name": "Alice Jones", "PassportNo": "8582658113", "Nationality": "Jellyland", "DoB": "1980-05-01", "Expiry": "2030-02-19", "Visa": "No", "Photo": "id1.png"},
        {"Name": "Bob Jones", "PassportNo": "4868486414", "Nationality": "Jellyland", "DoB": "1982-08-25", "Expiry": "2028-06-21", "Visa": "No", "Photo": "id2.png"},
        {"Name": "Ava Jones", "PassportNo": "2839534414", "Nationality": "Jellyland", "DoB": "2020-11-15", "Expiry": "2025-12-15", "Visa": "No", "Photo": "id3.png"},
        {"Name": "Avi Curbungen", "PassportNo": "U37886414", "Nationality": "Perlumbia", "DoB": "1995-08-25", "Expiry": "2028-06-21", "Visa": "Yes", "Photo": "id4.png"},
        {"Name": "Eden Plunkera", "PassportNo": "78834414", "Nationality": "Atlantis", "DoB": "1991-11-30", "Expiry": "2027-12-15", "Visa": "Yes", "Photo": "id5.png"},
        {"Name": "Sven Dersonwhip", "PassportNo": "8768336414", "Nationality": "Atlantis", "DoB": "1982-08-25", "Expiry": "2031-12-31", "Visa": "Yes", "Photo": "id6.png"},
        {"Name": "Olaf Buntingson", "PassportNo": "107994414T", "Nationality": "Perlumbia", "DoB": "2001-06-19", "Expiry": "2026-12-15", "Visa": "Yes", "Photo": "id7.png"},
        {"Name": "Xhti Gherxxoigh", "PassportNo": "107994414T", "Nationality": "Contestan", "DoB": "1981-07-11", "Expiry": "2032-10-06", "Visa": "Yes", "Photo": "id8.png"},
    ]
    return passports

def process_passenger(data, airport, action):    # Action when arrival button pressed
    """   
    # Action when arrival button pressed
    # Notify relevant airport so it adds to the blockchain
    """
    global airport_ip, airport_port, passenger_name, passenger_no, passenger_nationality, passenger_dob, passenger_expiry, passenger_visa, passenger_airport
    msg_type = 40  # Passenger Transaction message type

    # Payload (dictionary) to send to the airport
    payload = {
        "TransID": str(uuid.uuid4()),
        "Action": action, 
        "TimeDate": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "Airport": airport, 
        "Name": data['Name'], 
        "PassportNo": data['PassportNo'],
        "Nationality": data['Nationality'], 
        "DoB": data['DoB'], 
        "Expiry": data['Expiry'], 
        "Visa": data['Visa']    
    }
    
    sent_ok = send_message(airport_ip, airport_port, msg_type, payload)

    if sent_ok:
        print(f"\n\033[92mProcessed Passenger '{data['Name']}' {action} at {airport}\n") 
        processed_screen(True)  # Show the processed screen
    else:
        print(f"\n\033[91mFailed to processed Passenger '{data['Name']}' {action} at {airport}\n") 
        processed_screen(False)  # Show the processed screen        

def clear_screen():    
    """
    Clear screen (remove all widgets)
    """
    for widget in root.winfo_children():
        widget.destroy()

def welcome_screen():    # Displays the program welcome screen
    clear_screen()
    bg_image = PhotoImage(file="./image/jellyland_frontpage.png")  # Background image filename
    frame = tk.Frame(root, borderwidth=0, relief="solid", padx=0, pady=0)
    image_button = tk.Button(frame, image=bg_image, command=airport_select)
    image_button.pack() 
    frame.pack()
    root.bg_image = bg_image  # Reference to prevent Python garbage collection  

def processed_screen(success):    # Displays the program welcome screen
    clear_screen()
    if success:
        bg_image = PhotoImage(file="./image/success.png")  # Background image filename
    else:    
        bg_image = PhotoImage(file="./image/failure.png")  
    frame = tk.Frame(root, borderwidth=0, relief="solid", padx=0, pady=0)
    image_button = tk.Button(frame, image=bg_image)
    image_button.pack() 
    frame.pack()
    root.bg_image = bg_image  # Reference to prevent Python garbage collection  
    root.after(750, lambda: select_passenger(passenger_airport, airport_ip, airport_port)) # Wait 2 secs and then return to passenger selection 

def select_passenger(airport, air_ip, air_port):    
    """
    Displays all available passports on screen to select from
    """
    global passenger_airport, airport_ip, airport_port, image_anchor
    clear_screen()
    passenger_airport = airport  # Set the global variable to the selected airport
    airport_ip = air_ip
    airport_port = air_port

    root.grid_columnconfigure(0, weight=1)  # Spacer column on the left
    root.grid_columnconfigure(5, weight=1)  # Spacer column on the right 
    root.configure(bg="#FCD106")  # Set the background color to yellow

    # Frame for the title/header row
    header_frame = tk.Frame(root, bg="#FCD106")
    header_frame.grid(row=0, column=1, columnspan=6, pady=10)
    img1 = PhotoImage(file="./image/pcontrol_icon1.png")  # Passport control icon2
    img1_label = tk.Label(header_frame, image=img1, bg="#FCD106").grid(row=0, column=1, padx=10)
    image_anchor[img1] = img1   # Keep references to the images to prevent garbage collection
    header_text = tk.Label(header_frame, text=f"Welcome to {airport} Passport Control\nPlease select passenger", font=("Arial", 20, "bold"), fg = "black", bg="#FCD106").grid(row=0, column=2, padx=10)
    img2 = PhotoImage(file="./image/pcontrol_icon2.png") # Passport control icon2
    img2_label = tk.Label(header_frame, image=img2, bg="#FCD106").grid(row=0, column=3, padx=10)
    image_anchor[img2] = img2  # Keep references to the images to prevent garbage collection
    
    # Loop through all available passports and display them in a grid
    for i, passport in enumerate(passports):
        # Calculate row and column for grid placement
        row = (i // 4) + 1  # Maximum 4 passports per row
        column = (i % 4) + 1
        # Draw the frame cell
        frame = tk.Frame(root, borderwidth=2, relief="solid", padx=10, pady=10)
        frame.grid(row=row, column=column, padx=5, pady=5)
        frame.configure(bg="#FCD106")
        # Display the passport front cover image
        image_path = "./image/" + passport["Nationality"] + ".png"
        img = PhotoImage(file=image_path)
        image_button = tk.Button(frame, image=img, command=lambda data=passport: show_person(data,airport))
        image_button.pack() 
        image_anchor[passport["Name"]] = img   # Assign a variable to the image to prevent Python garbage collection
        disname = tk.Label(frame, text=f"{passport['Name']}", font=("Arial", 12, "bold"), bg="#FCD106", fg = "black").pack()  # Display passenger name 

    tk.Label(root, text="", bg="#FCD106", borderwidth=5).grid(row=row+1, column=0, columnspan=6)  # Add an empty label for spacing
    # Add a button to return to the airport selection screen
    tk.Button(root, text=" Change Airport ", command=airport_select, font=("Arial", 12, "bold"), bg="black", fg="#FCD106", borderwidth=5, relief="sunken").grid(row=row+2, column=0, columnspan=6, pady=10) # Start over back at airport selection       

def show_person(passport_data, airport):   
    """
    Show individual's details after they have been selected and 
    show buttons for 'arrival' 'departure' and 'start over'.
    """
    clear_screen()
    root.configure(bg="#FCD106")  # Set the background color to yellow
    """
    root.grid_columnconfigure(0, weight=0)  # Expands the column to fill the space     
    root.grid_columnconfigure(1, weight=0)  # Expands the column to fill the space   
    root.grid_columnconfigure(2, weight=0)  # Expands the column to fill the space 
    root.grid_columnconfigure(3, weight=0)  # Expands the column to fill the space 
    root.grid_columnconfigure(4, weight=3)  # Expands the column to fill the space 
    """
    
    # Frame for the title/header row
    header_frame = tk.Frame(root, bg="#FCD106")
    header_frame.grid(row=0, column=0, columnspan=6, pady=10)
    img1 = PhotoImage(file="./image/pcontrol_icon1.png")  # Passport control icon2
    img1_label = tk.Label(header_frame, image=img1, bg="#FCD106").grid(row=0, column=0, padx=10)
    image_anchor[img1] = img1   # Keep references to the images to prevent garbage collection
    header_text = tk.Label(header_frame, text=f"Welcome to {airport} Passport Control\nPlease select Arrival or Departure", font=("Arial", 20, "bold"), fg ="black", bg="#FCD106").grid(row=0, column=2, padx=10)
    img2 = PhotoImage(file="./image/pcontrol_icon2.png") # Passport control icon2
    img2_label = tk.Label(header_frame, image=img2, bg="#FCD106").grid(row=0, column=4, padx=10)
    image_anchor[img2] = img2  # Keep references to the images to prevent garbage collection

    middle_frame = tk.Frame(root, bg="#FCD106")
    middle_frame.grid(row=1, column=0, columnspan=6, pady=10)
    # Display the passport front cover
    image_path = "./image/" + passport_data['Photo']
    passport_img = PhotoImage(file=image_path)     
    tk.Label(middle_frame, image=passport_img, bg="#FCD106").grid(row=1, column=3, padx=10, columnspan=3)
    image_anchor["passport_img"] = passport_img 
    # Display passport details (name etc.)
    tk.Label(middle_frame, text=f"Name: {passport_data['Name']} (Born {passport_data['DoB']})", font=("Courier New", 16), bg="#FCD106").grid(row=2, column=3, columnspan=3, padx=10)
    tk.Label(middle_frame, text=f"Passport No: {passport_data['PassportNo']} (Expiry: {passport_data['Expiry']})", font=("Courier New", 14), bg="#FCD106").grid(row=3, column=3, columnspan=3, padx=10)
    tk.Label(middle_frame, text=f"Nationality: {passport_data['Nationality']}   Jellyland Visa: {passport_data['Visa']}", font=("Courier New", 14), bg="#FCD106").grid(row=4, column=3, columnspan=3, padx=10)

    # Display Arrival and Departure buttons
    footer_frame = tk.Frame(root, bg="#FCD106")
    footer_frame.grid(row=3, column=0, columnspan=6, pady=10)
    tk.Button(footer_frame, text=" Arrival ",   command=lambda: process_passenger(passport_data, airport, "Arrival"), font=("Arial", 20, "bold"), bg="green", fg="white").grid(row=0, column=0, columnspan=1, padx=10)
    tk.Button(footer_frame, text="Departure", command=lambda: process_passenger(passport_data, airport, "Departure"), font=("Arial", 20, "bold"), bg="red", fg="white").grid(row=0, column=1, columnspan=1, padx=10)

def airport_select():   
    """
    Displays the available airports in a grid format and allows the user to select one.
    """
    global airport_directory
    global image_anchor
    get_airports(tracker_addr, tracker_port)  # Get the list of available airports from the tracker
    clear_screen()
    root.configure(bg="lightblue")  # Set the main window background color 

    if len(airport_directory) == 0:    # If no airports are available, display a message and a refresh button
        root.grid_columnconfigure(0, weight=1)  # Expands the single column to fill the space so that the buttons/text are centered
        tk.Label(root, text="\nRepublic of Jellyland", font=("Arial", 20, "bold"), fg="black", bg="lightblue").grid(row=0, column=0,  pady=10)
        tk.Label(root, text=" No airports are currently available ", font=("Arial", 20, "bold"), fg="black", bg="lightblue").grid(row=1, column=0,  pady=10)
        tk.Button(root, text="Refresh", command=airport_select, font=("Arial", 20, "bold"), fg="white", bg="blue").grid(row=2, column=0, padx=10, pady=10) 

    else:
        tk.Label(root, text="Republic of Jellyland\nSelect your arrival / departure port", font=("Arial", 20, "bold"), fg="black", bg="lightblue").grid(row=0, column=0, columnspan=5, pady=10)

    airport_images = {}  # Dictionary to hold references to images to avoid garbage collection

    root.grid_columnconfigure(0, weight=1)  # Expands the column to fill the space     
    root.grid_columnconfigure(1, weight=2)  # Expands the column to fill the space  
    root.grid_columnconfigure(2, weight=2)  # Expands the column to fill the space  
    root.grid_columnconfigure(3, weight=2)  # Expands the column to fill the space  
    root.grid_columnconfigure(4, weight=1)  # Expands the column to fill the space     
 
    # Loop through all cities and display them in a grid
    for i, airport in enumerate(airport_directory):        
 
        airport_ip, airport_port = airport_directory[airport]['airport_ip'], airport_directory[airport]['airport_port']  # Get the IP and port of the airport

        #print(f"Airport: {airport} IP: {airport_ip} Port: {airport_port}")  # Print the airport details to terminal

        row = (i // 3) * 2 + 1  # Calculate the row (3 cities per row)
        column = (i % 3) +1     # Calculate the column by the MOD

        # Draw the frame cell
        tk.Frame(root, borderwidth=2, relief="solid", padx=10, pady=10, bg="white").grid(row=row, column=column, padx=5, pady=5)
        # Display a photo of the city
        airport = airport.rstrip()
        image_path = "./image/" + airport + ".png"  # Image filename
        img = PhotoImage(file=image_path)
        image_anchor[airport] = img
        tk.Button(root, image=img, command=lambda airport_name=airport, air_ip=airport_ip, air_port=airport_port: select_passenger(airport_name, air_ip, air_port)).grid(row=row, column=column, padx=5, pady=5)  # Display the city image as a button
        tk.Label(root, text=f"{airport}", font=("Arial", 12, "bold"), bg="lightblue", fg = "black").grid(row=row+1, column=column, padx=5, pady=5) # Display the airport name below the image

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
            rx_socket.bind(('', gui_port))  # Bind to the listening port
            rx_socket.listen(1)  # Listen for incoming connections
            #print(f"Listening for tracker response on port {airport_port_no}.")
            conn, addr = rx_socket.accept()  # Accept an incoming connection
            remote_ip, remote_src_port = addr  # Get the sender's IP address and src. port number
            response = conn.recv(2048)  # Receive the response from the remote host
    except socket.timeout:
        #print("\nSocket Timed Out waiting. Continue to wait.\n ")
        pass
    except socket.error as e:
        print(f"\033[91m\nSocket error: {e}\n")
    finally:
        # Close the socket
        rx_socket.close()

    if response:

        # Unpack the received message
        payload = response[struct.calcsize('=9s20sIIIB'):]  # Extract the payload from the response
        # Unpack the header fields
        unpacked_data = struct.unpack('=9s20sIIIB', response[0:struct.calcsize('=9s20sIIIB')])    
        node_name = unpacked_data[1].decode('utf-8').strip('\x00')  # Decode and strip padding
        tcp_rcv_port = unpacked_data[2]
        seq_no = unpacked_data[3]
        ack_no = unpacked_data[4]
        msg_type = unpacked_data[5]

        return seq_no, ack_no, node_name, tcp_rcv_port, remote_ip, msg_type, payload 
    else:
        return None, None, None, None, None, None  # Return None if no response is received


def get_airports(ip, port):   
    """
    Parameters:  <tracker IP address> <tracker port no>
    This function gets the directory of available airports from the tracker and stores it as a dictionaries.
    Returns :  A list of dictionaries containing the airport name and port number.
    """
    global airport_directory
    # Compile the request message:
    msg_type = 30  # Request Directory
    seq_no = 0  # Not used
    ack_no = 0  # Not used
    payload = b''  # Not used

    encoded_msg = encode_msg("GUI", gui_port, seq_no, ack_no, msg_type, payload)
    print(f"Request Airport directory from tracker.")

    # Create a TCP socket and send the registration message
    try:       
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_socket:   # Create a TCP socket
            send_socket.connect((ip,port)) # Connect to the tracker
            send_socket.sendall(encoded_msg) # Send the encoded message to the tracker                    
    except socket.error as e:   # Belongs to the 'try'
        print(f"\033[91m\nSocket error: {e}\nTracker not reachable at {ip}:{port}.\033[0m\n")
        return

    # Receive message from the tracker.  Blocking call.
    seq_no, ack_no, node_name, tcp_rcv_port, tracker_ip, msg_type, payload=receive_message()

    # Transfer the received payload into the airport directory
    received_message = payload.decode("utf-8")  # Converts bytes string to string
    airport_directory = ast.literal_eval(received_message)    # Global variable to hold the directory of airports      
    #print(f"directory: {airport_directory}")  
    print_airports()  # Print the updated directory to terminal
    

if __name__ == '__main__':

    #Check if the correct number of arguments are provided
    if len(sys.argv) != 4:
        print(f"\n\033[91mInsufficient arguments ({len(sys.argv)})\nUsage: python passenger_gui.py <gui port> <tracker_port> <tracker_addr>\033[0m\n")
        sys.exit(1)

    # Get the command line arguments
    gui_port = int(sys.argv[1])
    tracker_port = int(sys.argv[2])
    tracker_addr = sys.argv[3]   
    airport_ip, airport_port = "", 0  # Initialize airport IP and port variables 

    print(f"\n\033[37;42;1m [ Airport Passport Control Starting Up. Tracker: {tracker_addr}:{tracker_port} ] \033[0m\n")
    
    airport_directory = [ ]  # List of available airports which we get from the tracker
    image_anchor = {} # Dictionary to hold references to images to avoid garbage collection

    # Define some global variables:
    passenger_name = ""
    passenger_no = ""
    passenger_nationality = ""
    passenger_dob = ""
    passenger_expiry = ""
    passenger_visa = ""
    passenger_action = ""
    passenger_airport = ""  

    
    # Get the passports 
    passports = []  # List to hold all passengers' passport details (global)
    passports = get_passports() 

    # Initialise TKinter and create the main window
    root = tk.Tk()
    root.title("Passport Control GUI")
    root.geometry("1000x800")
    welcome_screen() # Run the welcome screen
    root.mainloop() # This is a blocking call which activates tkinter so all other functions will need to be in the background
    root.destroy()  # Close the main window when the application is closed 


