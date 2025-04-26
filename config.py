# config.py
# Global configuration and tunable parameters for the blockchain system

import os

# Network Settings

# Default port where tracker listens for REGISTER/DEREGISTER/DIRECTORY
TRACKER_PORT: int = 60000  # TODO: set tracker port

# Base port for peer airports (each peer adds an offset)
DEFAULT_PEER_PORT: int = 60010  # TODO: choose starting port for peers

# TCP timeout for network operations (seconds)
NETWORK_TIMEOUT: int = 10  # TODO: adjust as needed for environment



#  Consensus Settings

# Proof-of-Work difficulty: number of leading zeros required in block hash
DIFFICULTY: int = 2  # TODO: tune difficulty based on demo hardware

# Time window (seconds) to wait for block approvals before discarding
PROPOSAL_TIMEOUT: int = 15  # TODO: adjust for network latency and size



# Persistence Settings

# File path to append and read chain blocks
CHAIN_LOG: str = os.path.join(os.path.dirname(__file__), 'chain.log')  # TODO: ensure write permissions



# GUI Settings 

# Folder for static assets (images, icons)
IMAGE_DIR: str = os.path.join(os.path.dirname(__file__), 'image')  # TODO: verify correct relative path

# GUI refresh interval (ms)
GUI_REFRESH_MS: int = 500  # TODO: tune for responsiveness



# Miscellaneous Settings 

# Maximum number of orphaned blocks to keep in memory
MAX_ORPHANS: int = 100  # TODO: guard against memory bloat

# Maximum pending proposals stored
MAX_PENDING: int = 50  # TODO: tune based on expected block rate

