# chain.py

# heart of the blockchain implementation. Defines in-memory chain structures, the Block type, 
# the proof-of-work mechanism, validation logic, fork handling, and persistence hooks

from typing import List, Dict, Optional
import time
from utils import compute_hash, merkle_root
from config import DIFFICULTY, CHAIN_LOG

class Block:
    """
    Represents a single block in the chain
    
    Fields:
        - index: int
        - timestamp: int # ms since epoch
        - previous_hash: str
        - nonce: int
        - merkle_root: str
        - transactions: List[dict]
        - hash: str
    """
    def __init__(self,
                 index: int,
                 timestamp: int,
                 previous_hash: str,
                 nonce: int,
                 merkle_root: str,
                 transactions: List[dict],
                 hash: Optional[str] = None):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.merkle_root = merkle_root
        self.transactions = transactions
        self.hash = hash

    def header_bytes(self) -> bytes:
        """
        Returns the serialized header fields (index, timestamp, previous_hash,
        merkle_root, and nonce) as bytes for hashing.
        """
        # TODO: pack fields into bytes (e.g., struct.pack)
        pass

# In-memory chain and auxillary pools
chain: List[Block] = []     # confimed blocks, in order
orphans: Dict[str, Block] = {}      # blocks whose parent is missing
pending_proposals: Dict[str, Block] = {}    # proposed but unconfirmed blocks


# ---------------------------------------------------------------------------

# MICHAEL HAS WRITTEN THE FOLLOWING FUNCTIONS:
def format_field(value, size, data_type):
    """
    Formats an int or string to a fixed size string for block header
    """
def restore_field(value, data_type):
    """
    Converts a fixed sized strink back into an int or string
    This reverses the format_field() function
    """
def read_block(block):
    """
    Extract the fields from a block
    Parameters: block: The block to read
    Returns block_index, block_time, chain_size, previous_hash, data
    """
def create_block(data):
    """
    Create a block for the blockchain
    Parameters:  data: The trasaction data from the passenger (arrival/departure info)
    node_name: The name of the airport
    """
def proof_of_work(block: Block) -> Block:
    """
    Generate proof of work on the block.
    Builds the block and adds the hash / finds the right nonce to make all the leading zeros
    Parameters:  block: The block to perform proof of work on
    returns:   final_block : finished block with nonce and hash
    """
def is_valid_proof(block: Block) -> bool:
    """
    Validate the block by checking the proof of work and verifying signature.
    Parameters:     block: The block string to validate
    Returns:     True if valid otherwise False
    """
def generate_key_pair():
    """
    Generates a private and public key pair using ECDSA (secp256k1 curve).
    Returns: private_pem, public_pem: The private/public keys in PEM format
    """

# -----------------------------------------------------------------------------------

def creat_genesis_block() -> Block:
    """
    Creates and returns the genesis (first) block of the chain.
    """
    # TODO:
    #  - index = 0
    #  - previous_hash = '0'*64
    #  - timestamp = fixed or current
    #  - nonce = 0 or proof-of-work skip
    #  - transactions = []
    #  - compute hash
    pass

def proof_of_work(block: Block) -> Block:
    """
    Performs proof-of-work by iterating nonce until the block's hash
    meets the DIFFICULTY target (leading zeros).
    Returns the mined block with hash set.
    """
    # TODO:
    #  - loop nonce
    #  - call block.header_bytes() and compute_hash()
    #  - check prefix zeros
    #  - assign block.hash and return
    pass

def is_valid_proof(block: Block) -> bool:
    """
    Validates the block's proof-of-work using its stored nonce and hash.
    """
    # TODO:
    #  - recompute hash from header_bytes()
    #  - compare to block.hash
    #  - check difficulty
    return False

def is_valid_block(new_block: Block, previous_block: Block) -> bool:
    """
    Checks linkage, index continuity, and proof-of-work validity.
    """
    # TODO:
    #  - new_block.previous_hash == previous_block.hash
    #  - new_block.index == previous_block.index + 1
    #  - is_valid_proof(new_block)
    #  - (optional) validate each transaction
    return False

def add_block(new_block: Block) -> bool:
    """
    Attempts to add a new block to the chain.
    - If it extends the current tip and is valid, append to chain.
    - If parent missing, store in orphans.
    - If it forks an earlier block, hand off to fork resolver.
    Returns True on success.
    """
    # TODO:
    #  - locate parent
    #  - validate via is_valid_block
    #  - append or orphan or fork
    return False

def resolve_fork() -> None:
    """
    Detects and resolves forks using the longest-chain (heaviest) rule.
    """
    # TODO: gather branches from common ancestor, compare cumulative work,
    #       adopt heavy branch, reassign/flush orphans
    pass

def handle_incoming_block(raw_data: bytes) -> None:
    """
    Deserialize, validate, and integrate an incoming block.
    """
    # TODO:
    # - parse raw_data into Block
    # - call add_block()
    # - broadcast APPROVAL or REJECTION messages via network layer
    pass


def save_block_to_disk(block: Block) -> None:
    """
    Appends serialized block to CHAIN_LOG for persistence.
    """
    # TODO: open CHAIN_LOG in append mode, write block data
    pass


def load_chain_from_disk() -> None:
    """
    Reads CHAIN_LOG and rebuilds in-memory chain on startup.
    """
    # TODO: open CHAIN_LOG, deserialize each entry, call add_block()
    pass


def print_chain() -> None:
    """
    Debug helper: prints index, hash, and transaction count for each block.
    """
    # TODO: iterate chain and print summary
    pass


def get_chain_height() -> int:
    """
    Returns current tip height.
    """
    return len(chain) - 1


def find_block_by_hash(hash_value: str) -> Optional[Block]:
    """
    Locate a block in chain or orphans by its hash.
    """
    # TODO: search chain + orphans, return Block or None
    return None


# Initialize chain at import
load_chain_from_disk()
if not chain:
    genesis = create_genesis_block()
    chain.append(genesis)
    save_block_to_disk(genesis)
