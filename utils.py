# utils.py
# Cryptographic and utility functions for the blockchain core

# Nothing else should touch raw hashing--everyone just calls these functions

import hashlib
from typing import List


def compute_hash(data: bytes) -> str:
    """
    Computes SHA-256 hash of the given data and returns the hex digest.
    """
    # TODO: ensure data is in bytes
    # TODO: use hashlib.sha256
    # return hex string (64 chars)
    pass


def merkle_root(leaves: List[bytes]) -> str:
    """
    Computes the Merkle root of a list of 'leaves' (each a byte sequence).
    Returns the hex digest of the root hash.

    If the number of leaves is odd, duplicate the last one.
    """
    # TODO:
    #  if empty leaves, return hash of empty string
    #  while len(leaves) > 1:
    #    pairwise hash: for each adjacent leaves[i], leaves[i+1]
    #    if odd, duplicate last
    #    compute parent hash = compute_hash(left + right)
    #    build new level
    #  return hex digest of final single leaf
    pass
