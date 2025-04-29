# chain.py
# Core blockchain implementation: block structure, proof-of-work, validation, persistence, and mempool.

import time
import datetime
import json
import hashlib
import struct
from typing import List, Dict, Optional, Tuple
from config import DIFFICULTY, CHAIN_LOG

# ECDSA crypto for signing/verification
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature, encode_dss_signature
)
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature


class Block:
    """
    Represents a single block in the chain.

    Fields:
      - index: int
      - timestamp: int       # ms since epoch
      - previous_hash: str   # hex string
      - nonce: int
      - merkle_root: str     # hex string
      - transactions: List[dict]
      - hash: str            # hex string
    """
    def __init__(
        self,
        index: int,
        timestamp: int,
        previous_hash: str,
        nonce: int,
        merkle_root: str,
        transactions: List[dict],
        hash: Optional[str] = None
    ):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.merkle_root = merkle_root
        self.transactions = transactions
        self.hash = hash

    def header_bytes(self) -> bytes:
        """
        Serialize (index, timestamp, previous_hash, merkle_root, nonce) for hashing.
        """
        return struct.pack(
            '=IQ32s32sI',
            self.index,
            self.timestamp,
            bytes.fromhex(self.previous_hash),
            bytes.fromhex(self.merkle_root),
            self.nonce
        )


# in-memory data structures
chain: List[Block] = []                 # confirmed blocks
orphans: Dict[str, Block] = {}         # blocks whose parent is missing
pending_proposals: Dict[str, Block] = {}  # proposed but unconfirmed blocks
mempool: Dict[str, dict] = {}          # pending transactions


# ---------------------------------------------------------------------------
# Key management

def generate_key_pair():
    """
    Generates ECDSA key pair (secp256k1).  
    Returns: (private_pem, public_pem) in PEM format.
    """
    private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem


# ---------------------------------------------------------------------------
# Hashing & Merkle

def compute_hash(data):
    """
    SHA-256 hash of bytes or string. Returns hex digest.
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def merkle_root(leaves: List[bytes]) -> str:
    """
    Compute Merkle root of a list of byte-leaves.
    TODO: implement full Merkle tree logic here.
    """
    if not leaves:
        return compute_hash(b'')
    # stub; real implementation would pairwise-hash up the tree
    return compute_hash(leaves[0])


# ---------------------------------------------------------------------------
# Fixed-width field formatting

def format_field(value, size: int, data_type: str) -> str:
    """
    - data_type="int":  zero-padded hex string width=size
    - data_type="str":  left-justified, truncated/padded to size
    """
    if data_type == "int":
        s = f"{value:0{size}x}"
        return s[-size:]
    elif data_type == "str":
        return f"{value:<{size}}"[:size]
    else:
        raise ValueError(f"Unknown data_type {data_type}")


def restore_field(raw: str, data_type: str):
    """
    Reverse of format_field: parse hex to int or strip padding from str.
    """
    if data_type == "int":
        return int(raw, 16)
    elif data_type == "str":
        return raw.rstrip('\x00')
    else:
        return raw


# ---------------------------------------------------------------------------
# Block serialization / inspection

def read_block(block_str: str):
    """
    Parse a serialized block string into its components.
    Returns (index, status, timestamp, chain_size, prev_hash, data, nonce, hash).
    """
    idx       = restore_field(block_str[0:4],   "int")
    status    = restore_field(block_str[4:5],   "int")
    timestamp = restore_field(block_str[5:25],  "str")
    chain_sz  = restore_field(block_str[25:29], "int")
    prev_hash = restore_field(block_str[29:37], "str")
    dsize     = restore_field(block_str[37:41], "int")
    data      = restore_field(block_str[41:41+dsize], "str")
    nonce     = restore_field(block_str[41+dsize:49+dsize], "int")
    bhash     = restore_field(block_str[49+dsize:], "str")
    return idx, status, timestamp, chain_sz, prev_hash, data, nonce, bhash


# ---------------------------------------------------------------------------
# Block creation & Proof-of-Work

def create_block(transactions: Dict[str, dict], b_index: int,
                 c_size: int, p_hash: str, private_pem: bytes) -> str:
    """
    Build a new block from transactions dict, then mine it.
    Returns the full serialized block string.
    """
    block_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    block_dict = {
        "b_index":      b_index,
        "block_status": 2,   # 2 = proposed
        "block_time":   block_time,
        "c_size":       c_size,
        "p_hash":       p_hash,
        "data":         transactions,
        "nonce":        0,
        "private_pem":  private_pem
    }
    return proof_of_work(block_dict, b_index, c_size, p_hash)


def proof_of_work(block_dict: dict, b_index: int, c_size: int, p_hash: str) -> str:
    """
    Iterate nonce until SHA-256(block_bytes) has DIFFICULTY leading zeros.
    Then sign the hash with ECDSA, append hash+signature, and return full block string.
    """
    nonce = 0
    start = time.time()
    print("Mining…", end="")

    while True:
        bstr = (
            format_field(b_index,  4, "int") +
            format_field(block_dict["block_status"], 1, "int") +
            format_field(block_dict["block_time"], 20, "str") +
            format_field(c_size,       4, "int") +
            format_field(p_hash,       8, "str") +
            format_field(len(json.dumps(block_dict["data"])), 4, "int") +
            format_field(json.dumps(block_dict["data"]),
                         len(json.dumps(block_dict["data"])), "str") +
            format_field(nonce,       8, "int")
        )
        bhash = hashlib.sha256(bstr.encode('utf-8')).hexdigest()

        if bhash.startswith('0' * DIFFICULTY):
            bstr += format_field(bhash, 64, "str")

            # sign
            priv = serialization.load_pem_private_key(
                block_dict["private_pem"], password=None, backend=default_backend()
            )
            der = priv.sign(bhash.encode('utf-8'), ec.ECDSA(hashes.SHA256()))
            r, s = decode_dss_signature(der)
            sig_bytes = r.to_bytes(32, 'big') + s.to_bytes(32, 'big')
            bstr += sig_bytes.hex()

            elapsed = round(time.time() - start, 3)
            print(f"\nMined in {elapsed}s @ difficulty {DIFFICULTY}")
            return bstr

        if nonce % 2000 == 0:
            print(".", end="", flush=True)
        nonce += 1


def is_valid_proof(block_str: str, public_pem: bytes) -> bool:
    """
    Verifies that the embedded hash meets DIFFICULTY and that the ECDSA signature checks out.
    """
    raw_sig  = bytes.fromhex(block_str[-128:])
    embedded = block_str[-192:-128]
    body     = block_str[:-192]

    recalc = hashlib.sha256(body.encode('utf-8')).hexdigest()
    if not recalc.startswith('0' * DIFFICULTY):
        print("Invalid PoW")
        return False

    r = int.from_bytes(raw_sig[:32], 'big')
    s = int.from_bytes(raw_sig[32:], 'big')
    der = encode_dss_signature(r, s)

    pub = serialization.load_pem_public_key(public_pem, backend=default_backend())
    try:
        pub.verify(der, recalc.encode('utf-8'), ec.ECDSA(hashes.SHA256()))
        return True
    except InvalidSignature:
        print("Invalid signature")
        return False


# ---------------------------------------------------------------------------
# Mempool operations

def mempool_push(tx: dict):
    """
    Add a transaction dict to the mempool.
    """
    mempool[tx["TransID"]] = tx


def mempool_pull() -> Tuple[Optional[str], Optional[dict]]:
    """
    Pull the oldest tx with Status="Ready", mark it Processing, and return it.
    """
    for tid, entry in mempool.items():
        if entry.get("Status") == "Ready":
            entry["Status"] = "Processing"
            return tid, entry
    return None, None


def ready_blocks() -> Dict[str, dict]:
    """
    Drain all Ready transactions into a dict for block creation.
    """
    out = {}
    while True:
        tid, tx = mempool_pull()
        if tid is None:
            break
        out[tid] = tx
    return out


# ---------------------------------------------------------------------------
# Stubbed functions (to be implemented later)

def is_valid_block(new_block: Block, previous_block: Block) -> bool:
    """Checks parent linkage, index continuity, and PoW validity."""
    pass  # TODO

def add_block(new_block: Block) -> bool:
    """Append or orphan or fork based on parent existence."""
    pass  # TODO

def resolve_fork() -> None:
    """Adopt the heaviest branch among forks."""
    pass  # TODO

def handle_incoming_block(raw_data: bytes) -> None:
    """Deserialize, validate, broadcast approval/rejection."""
    pass  # TODO

def save_block_to_disk(block: Block) -> None:
    """Append serialized block to CHAIN_LOG."""
    pass  # TODO

def load_chain_from_disk() -> None:
    """Read CHAIN_LOG and rebuild in-memory chain."""
    pass  # TODO

def print_chain() -> None:
    """Debug: print index, hash, tx count for each block."""
    pass  # TODO

def get_chain_height() -> int:
    """Return current tip height."""
    return len(chain) - 1

def find_block_by_hash(hash_value: str) -> Optional[Block]:
    """Locate a block by its hash in chain or orphans."""
    pass  # TODO
