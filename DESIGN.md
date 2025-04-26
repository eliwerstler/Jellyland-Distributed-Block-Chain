## CSEE 4119 Spring 2025, Term Group Project  
## Trisha, Eli, Michael  
## Blockchain Demo  

### Project Overview  
Our project is to design an entry/exit (arrival/departure) record for use at airports and other ports of entry for the Republic of Jellyland.  It is vital that these records are maintained immutably to ensure that every entry and exit is complementary or interdependent, for example to ensure that two people don't use the same passport for entry or exit into a country.  When we refer to 'ports' we are referring to physical ports of entry e.g. an airport, not a TCP/IP port (with the exception of where we are specifically talking about TCP ports!).  All communication in our system is TCP.

### Block Format  
Our block is a binary string with the following fields:  
- **Block ID** : 4-Byte Unsigned integer (randomized)  
- **Block Size (Height)** including this block : 4-Byte Unsigned integer  
- **Nonce** : 4-Byte Unsigned integer  
- **Hash** : 32 bytes (256 bits)  
- **Previous Hash** : 32 bytes (256 bits)  
- **Data** : Variable Size  

The data section include the following fields:  
Date of Record, Name, Date of Birth, Nationality, Date of transaction, Visa, Warrant, Status, Action

### Multiple Transactions per Block  
If time allows, `airport.py` will wait for multiple new records before writing a new block and then include several records in the block, using a Merkle tree.

---

### tracker.py  
`tracker.py` acts as the central registry for nodes. A peer announces itself to the tracker which maintains a list of active peers which is provided to any new peer joining the network.  Peers can leave the network or be forcefully removed if they timeout when polled.  
**Syntax:** `python3 tracker.py <Tracker TCP port>`

**Tracker Receives messages from `airport.py`:**  
- `10  REGISTER`   - Peer Port joining the network  
- `15  DEREGISTER` - Peer Port leaving the network  
- `20  QUERY`      - Peer Port requesting peer list

---

### airport.py  
Multiple instances of `airport.py` run, each representing a port in Jellyland, which is also a peer.  
**Syntax:** `python3 airport.py <Tracker ip> <Tracker port> <Airport port> <airport name>`  

When run, `airport.py` announces itself to `tracker.py` which adds it to the list of active peers. Announcement contains a binary string of:  
- TCP Port : 4-byte unsigned integer  
- Location : 20 bytes  
- Random peer ID : 2-byte unsigned integer  
- Public Key : 20 bytes  

`airport.py` requests a copy of the current blockchain from any peer (and verifies it). If none exists, it starts blank. Each peer generates its own public/private key pair for use with the hash.  

Once running, `airport.py` displays the Kiosk Front end GUI (see later).  

**`airport.py` sends these messages to all peers:**  
- `30  PROPOSAL` - Port proposing a new block  
- `40  APPROVAL` - Approve  
- `50  ANOMALY`  - Mismatch in Chain (fork)

---

### Sharing New Blocks  
`airport.py` shares its new block proposal with all peers. Each receiving peer checks integrity (proof of work) and hash and approves it (sends to all peers). Any new block is 'pending' until consensus >50% approvals and sufficient time has elapsed to eliminate forks. A dictionary is maintained of new blocks until either approved or discarded. If a block does not reach consensus within X seconds, it is discarded.

---

### Fork Resolution  
If two nodes add a block simultaneously on top of the same previous block, a fork occurs.  Process/Resolution: TBA

---

### Port Transaction (Passengers)  
`airport.py` allows a person to present himself at the border to exit or enter the country. The front end presents a kiosk where the person selects their passport and selects whether they are arriving or departing Jellyland. The logic of the immigration process is to check that any person entering is either a citizen or has a visa and if there are any anomalies in status, send for secondary 'screening'.

A passport contains: Name, DoB, Nationality, Passport Number, Expiry Date, Visa Status  

1. Check if there's a warrant out for the person. Yes?: Screen/Record/Terminate  
2. If they are exiting: if a record for them exists, check previous status is 'In Country'. No?: Screen/Record/Terminate.  
3. If they are entering: check previous status (if any) is 'Out'. No?: Screen/Record/Terminate. If not a citizen, check Visa is valid. No?: Screen/Record/Terminate.  
4. Entry/Record/Terminate.  

See flowchart for full logic.

---

### Methods in airport.py  
`airport.py` calls methods/functions:  
- `network.register`  
- `network.deregister`  
- `chain.WriteBlock`  
- `chain.FindBlock`  
- `chain.ShareBlock`  
- etc.

---

## Genesis & Chain Synchronization  
- **Genesis Block**: The first peer creates a block with `index = 0`, `previous_hash = '0'*64`, a fixed timestamp, and no transactions.  
- **Startup Sync**: On launch, a new peer sends a `GET_CHAIN` request to any existing peer.  
- **Chain Response**: Existing peers reply with `CHAIN_RESPONSE` containing the full validated chain. The newcomer verifies each block before appending.

---

## Transaction Validation Rules  
All peers enforce consistent rules when validating each block’s transactions:  
1. **Warrant Check**: Reject any transaction with `warrant_flag == true`.  
2. **Departure**: Require prior status = `In Country`.  
3. **Arrival**: Require prior status = `Out`; if non-citizen, enforce `visa_status == Yes`.  
4. **Atomicity**: If any individual transaction in a multi-transaction block fails, reject the entire block.

---

## Persistence  
- The chain resides **in memory** during runtime for fast access.  
- Each finalized block is serialized and appended to an **append-only log file** (`chain.log`).  
- On restart, peers read `chain.log` to reconstruct the in-memory chain before accepting new blocks.

---

_End of DESIGN.md_
