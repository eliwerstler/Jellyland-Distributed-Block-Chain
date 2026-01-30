## CSEE 4119 Spring 2025, Jellyland Distributed Block Chain
## Blockchain Demo

Overview
----------------------------
This project implements a simplified peer-to-peer blockchain system to record passenger arrivals and departures at various airports in the fictional Republic of Jellyland. Each airport runs as an independent node, maintains its own copy of the blockchain, mines blocks containing transactions, and broadcasts block proposals to peers. A tracker maintains the list of active airports. A separate passenger GUI allows users to check in at any available airport.


Features  
----------------------------
- Peer-to-peer TCP network with one tracker and multiple airport peers  
- Blockchain with proof-of-work and digital signature validation (ECDSA)  
- Live transaction logging and block mining at each peer  
- Fork resolution via longest chain rule  
- Orphaned block handling  
- GUI-based passenger interaction (arrival/departure)  
- Persistent storage of blockchain via `chain.log`

Architecture  
----------------------------
- `tracker.py`: Central server that manages peer registration and updates peer lists.
- `airport.py`: Peer node representing an airport that mines blocks and maintains a local chain.
- `passenger_gui.py`: Graphical interface for submitting arrival/departure requests.
- `chain.py`: Core blockchain logic (block format, proof-of-work, fork handling, validation, persistence).
- `config.py`: Global configuration (difficulty, log paths, port defaults).

Block Format & Message Types
----------------------------

| Type | Purpose                            | Sent From → To        |
|------|------------------------------------|------------------------|
| 10   | REGISTER peer                      | airport.py → tracker.py  
| 20   | DEREGISTER peer                    | airport.py → tracker.py  
| 30   | DIRECTORY request/response         | airport.py / GUI ↔ tracker.py  
| 40   | PASSENGER transaction              | passenger_gui.py → airport.py  
| 50   | BLOCK PROPOSAL                     | airport.py → all other airport.py 

Block Format  
----------------------------
Blocks are serialized as strings with the following fields:
- Block Index  
- Timestamp  
- Chain Size  
- Previous Hash (8-char)  
- Data Size  
- Serialized Transaction Dictionary  
- Nonce (8-digit hex)  
- Block Hash (64-character hex)  
- Digital Signature (r||s, 128 hex chars)

Each block is saved to `chain.log`.

Command lines for testing
-------------------------

Run scripts in the following order:
1. tracker.py 
2. airport.py - you do not have to run all 6.
3. passenger_gui.py picks up the airport names from tracker.py
   and only displays the online airports, 
   refreshing the list each time a new passenger wants to check in.

python3 tracker.py 60001

Up to 6 instances of airports, each in its own terminal.
Their city names are hard-coded so you must use those:

python3 airport.py 50001 Jellyopolis 60001 localhost
python3 airport.py 50002 Seaville 60001 localhost
python3 airport.py 50003 Lovelytown 60001 localhost
python3 airport.py 50004 Busyham 60001 localhost
python3 airport.py 50005 Quaintville 60001 localhost
python3 airport.py 50006 Smokeville 60001 localhost

python3 passenger_gui.py 50010 60001 localhost

When passenger_gui.py executes an arrival or departure, it sends
the arrival/departure message to the airport.py corresponding 
to the airport they selected.  Airports are identified by their
listening TCP port.

Blockchain Behavior
----------------------------
### Mining
- Transactions are mined into blocks with a proof-of-work difficulty of DIFFICULTY = 2.
- Each block is signed using ECDSA (secp256k1).
- Mining output is printed in the terminal.
### Fork Handling
- If two peers mine a block simultaneously, a fork may occur.
- The system keeps both forks and selects the one with greater cumulative work (longest chain).
- Nodes reorganize their chain automatically via resolve_fork().
### Orphan Handling
- If a peer receives a block with an unknown parent, it stores it in orphans.
- When the parent later arrives, the orphaned block is validated and added.
### Persistence
- Mined blocks are saved to chain.log.

- On restart, a node reads chain.log to reconstruct its in-memory chain.
