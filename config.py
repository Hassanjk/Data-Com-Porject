"""
Configuration file for Socket Error Detection Project
Contains network settings and project parameters
"""

# Network Configuration
SERVER_HOST = 'localhost'
SERVER_TO_CLIENT1_PORT = 5001  # Server listens for Client 1
SERVER_TO_CLIENT2_PORT = 5002  # Server forwards to Client 2

# Socket Configuration
BUFFER_SIZE = 4096
SOCKET_TIMEOUT = 300  # 5 minutes
ENCODING = 'utf-8'

# Packet Format
PACKET_DELIMITER = '|'
PACKET_FORMAT = 'DATA|METHOD|CONTROL_INFO'

# Error Detection Methods
ERROR_DETECTION_METHODS = {
    '1': 'PARITY',
    '2': '2D_PARITY',
    '3': 'CRC',
    '4': 'HAMMING',
    '5': 'CHECKSUM'
}

# Error Injection Types (for Server)
ERROR_INJECTION_TYPES = {
    '1': 'BIT_FLIP',
    '2': 'CHAR_SUBSTITUTION',
    '3': 'CHAR_DELETION',
    '4': 'CHAR_INSERTION',
    '5': 'CHAR_SWAP',
    '6': 'MULTIPLE_BIT_FLIPS',
    '7': 'BURST_ERROR',
    '8': 'NO_ERROR'  # For testing without corruption
}

# CRC Configuration
CRC_POLYNOMIAL = 0x107  # CRC-8 polynomial (x^8 + x^2 + x + 1)
CRC_POLYNOMIAL_16 = 0x11021  # CRC-16 CCITT
CRC_POLYNOMIAL_32 = 0x104C11DB7  # CRC-32

# 2D Parity Configuration
PARITY_MATRIX_ROWS = 4
PARITY_MATRIX_COLS = 8

# Logging Configuration
LOG_DIRECTORY = 'logs'
LOG_LEVEL = 'INFO'
ENABLE_FILE_LOGGING = True
ENABLE_CONSOLE_LOGGING = True

# Colors for console output (using colorama)
COLORS_ENABLED = True
