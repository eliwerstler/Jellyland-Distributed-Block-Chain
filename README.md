## CSEE 4119 Spring 2025, Term Group Project
## Blockchain Demo


Block Format & Message Types
----------------------------

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


Passenger Arrival/Departure Message
-----------------------------------

passenger.gui will send a message type '40' to airport.py with a dictionary in its
payload with the following fields ready for adding to the blockchain:

{'Action': 'Arrival', 'TimeDate': '2025-04-24 08:06:28', 'Airport': 'Quaintville', 'Name': 'Eden Plunkera', 'PassportNo': '78834414', 'Nationality': 'Atlantis', 'DoB': '1991-11-30', 'Expiry': '2027-12-15', 'Visa': 'Yes'}

Command lines for testing
-------------------------

Run scripts in the following order:
1. tracker.py 
2. airport.py - you do not have to run all 6.
3. passenger_gui.py picks up the airport names from tracker.py
   and only displays the online airports, 
   refreshing the list each time a new passenger wants to check in.

python3 tracker.py 60000

Up to 6 instances of airports, each in its own terminal.
Their city names are hard-coded so you must use those:

python3 airport.py 50001 Jellyopolis 60000 127.0.0.1
python3 airport.py 50002 Seaville 60000 127.0.0.1
python3 airport.py 50003 Lovelytown 60000 127.0.0.1
python3 airport.py 50004 Busyham 60000 127.0.0.1
python3 airport.py 50005 Quaintville 60000 127.0.0.1
python3 airport.py 50006 Smokeville 60000 127.0.0.1

python3 passenger_gui.py 50010 60000 127.0.0.1

When passenger_gui.py executes an arrival or departure, it sends
the arrival/departure message to the airport.py corresponding 
to the airport they selected.  Airports are identified by their
listening TCP port.






