## CSEE 4119 Spring 2025, Term Group Project  
## Trisha, Eli, Michael  
## Blockchain Demo  

### Project Overview  
Our project is to design an entry/exit (arrival/departure) record for use at airports and other ports of entry for the Republic of Jellyland.  It is vital that these records are maintained immutably to ensure that every entry and exit is complementary or interdependent. This ensures that two people don't use the same passport for entry or exit into a country.  When we refer to 'ports' we are referring to physical ports of entry e.g. an airport, not a TCP/IP port (with the exception of where we are specifically talking about TCP ports!).  All communication in our system is TCP.

### Block Format  
Our block is a binary string with the following fields:  
- Index : 4 characters (hex-encoded integer)
- Block Status : 1 character (hex-encoded integer)
- Timestamp : 20 characters (formatted string)
- Chain Size : 4 characters (hex-encoded integer)
- Previous Hash : 8 characters (hex-encoded string)
- Data Size : 4 characters (hex-encoded integer)
- Data : Variable length (stringified JSON of transactions)
- Nonce : 8 characters (hex-encoded integer)
- Hash : 64 characters (SHA-256 hash in hex)
- Signature : 128 characters (concatenated r and s components from ECDSA, 64 bytes total)

The data section includes the following fields:  
Date of Record, Name, Date of Birth, Nationality, Date of transaction, Visa, Warrant, Status, Action

### Private/Public Key
We generate a key pair using the python cryptography library and ECDSA (secp256k1 curve). The keys are stored in PEM format. The public key is submitted to the tracker when each airport peer registers.

### Block(chain) process

A block is created by concatenating the fields listed above and iterating through nonce values until the SHA-256 hash has the required number of leading zeros (set by DIFFICULTY). Once found, the block is signed using the peer’s private key. The hash and the ECDSA signature are appended to finalize the block. The signature uses the raw 64-byte r||s format.

### Multiple Transactions per Block  
Multiple transactions can be included in a block by draining the mempool and serializing the combined data as JSON. All transactions are packed into the data field of the block. A Merkle tree is not currently used.

---

### tracker.py  
`tracker.py` acts as the central registry for peer airports and the GUI. A peer registers itself with the tracker, which stores its TCP port, IP, and public key. This list is returned to any new peer or GUI client upon request.
**Syntax:** `python3 tracker.py <Tracker TCP port>`

**Tracker Receives messages from `airport.py`:**  
- `10  REGISTER`   - Peer Port joining the network  
- `20  DEREGISTER` - Peer Port leaving the network  
- `30  DIRECTORY`  - Request for airport directory (from peer or GUI)

---

### airport.py  
Each instance of airport.py represents a peer (airport) node in the network.
**Syntax:** `python3 airport.py <Tracker ip> <Tracker port> <Airport port> <airport name>`  

On startup, the peer registers with the tracker and receives the current list of all peers. A key pair is generated on each run, and a Genesis block is created if the local blockchain is empty.

Peers mine new blocks containing transactions and send them to all other peers via TCP. Peers receiving proposed blocks validate their structure, proof-of-work, and digital signature before accepting. 

**`airport.py` sends these messages to all peers:**  
- `50  PROPOSAL` - Propose a new block  
- `60  APPROVAL` - Approve a proposed block
- `70  REJECTION` - Reject a proposed block
- `80  BLOCK` - Broadcast a confirmed block
- `99 ANOMOLY` - Notify about a chain mismatch

---

### Sharing New Blocks  
A newly mined block is proposed to all known peers. Peers receiving the block validate the hash and signature. If valid, the block is added to the local blockchain. Consensus approval logic is not currently enforced — blocks are accepted on a per-peer basis.

---

### Fork Resolution  
If two nodes add a block simultaneously on top of the same previous block, a fork occurs.  

Process/Resolution: Each peer tracks the cumulative work (i.e., number of valid blocks) associated with each tip. The longest (heaviest) chain is selected, and the in-memory chain is reorganized accordingly. Orphaned blocks are retained for possible reorganization if needed later.

---

### Passenger Transactions 
A separate graphical application, passenger_gui.py, allows users to select an airport and initiate a transaction indicating whether they are arriving or departing Jellyland.

Each transaction includes:
- Name
- Date of Birth
- Nationality
- Passport Number
- Expiry Date
- Visa Status
- Timestamp
- Arrival or Departure flag

Transactions are sent over TCP to the selected airport peer, where they are stored in the mempool. These transactions are then mined into blocks.

---

## Genesis & Chain Synchronization  
- **Genesis Block**: The first peer creates a block with `index = 0`, `previous_hash = '0'*64`, a fixed timestamp, and no transactions.  
- **Startup Sync**: On launch, a new peer sends a `GET_CHAIN` request to any existing peer.  
- **Chain Response**: Existing peers reply with `CHAIN_RESPONSE` containing the full validated chain. The newcomer verifies each block before appending.

---

## Block Validation 
All peers enforce consistent rules when validating each block’s transactions:  
1. Index increments by 1
2. Previous hash matches 
3. SHA-256 hash satisfies difficulty
4. Signature is valid using the sender's public key

---

## Persistence  
- The chain resides **in memory** during runtime for fast access.  
- Each finalized block is serialized and appended to an **append-only log file** (`chain.log`).  
- On restart, peers read `chain.log` to reconstruct the in-memory chain before accepting new blocks.

---

_End of DESIGN.md_
