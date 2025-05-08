# config.py
# Global configuration and tunable parameters for the blockchain system

import os

#  Consensus Settings

# Proof-of-Work difficulty: number of leading zeros required in block hash
DIFFICULTY: int = 2  # TODO: tune difficulty based on demo hardware


# Persistence Settings

# File path to append and read chain blocks
CHAIN_LOG: str = os.path.join(os.path.dirname(__file__), 'chain.log')  # TODO: ensure write permissions
