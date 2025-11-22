"""
Utility module for error detection algorithms
Implements: Parity, 2D Parity, CRC, Hamming Code, Internet Checksum
"""

import config


class ErrorDetection:
    """Base class for all error detection methods"""
    
    @staticmethod
    def string_to_binary(text):
        """Convert string to binary representation"""
        return ''.join(format(ord(char), '08b') for char in text)
    
    @staticmethod
    def binary_to_string(binary):
        """Convert binary representation back to string"""
        chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
        return ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)


class ParityBit(ErrorDetection):
    """Parity Bit Error Detection (Even Parity)"""
    
    @staticmethod
    def generate(data):
        """
        Generate parity bit for data
        Returns: parity bit as string '0' or '1'
        """
        binary = ErrorDetection.string_to_binary(data)
        ones_count = binary.count('1')
        # Even parity: parity bit makes total number of 1s even
        parity = '0' if ones_count % 2 == 0 else '1'
        return parity
    
    @staticmethod
    def verify(data, received_parity):
        """
        Verify parity bit
        Returns: True if no error detected, False otherwise
        """
        calculated_parity = ParityBit.generate(data)
        return calculated_parity == received_parity


class TwoDParity(ErrorDetection):
    """2D Parity (Matrix Parity) Error Detection"""
    
    @staticmethod
    def generate(data):
        """
        Generate 2D parity for data
        Returns: parity string containing row and column parities
        """
        binary = ErrorDetection.string_to_binary(data)
        
        # Pad binary to fit matrix
        rows = config.PARITY_MATRIX_ROWS
        cols = config.PARITY_MATRIX_COLS
        total_bits = rows * cols
        
        if len(binary) < total_bits:
            binary = binary.ljust(total_bits, '0')
        else:
            binary = binary[:total_bits]
        
        # Create matrix
        matrix = [binary[i*cols:(i+1)*cols] for i in range(rows)]
        
        # Calculate row parities
        row_parities = ''.join('1' if row.count('1') % 2 == 1 else '0' for row in matrix)
        
        # Calculate column parities
        col_parities = ''
        for col_idx in range(cols):
            col = ''.join(matrix[row_idx][col_idx] for row_idx in range(rows))
            col_parities += '1' if col.count('1') % 2 == 1 else '0'
        
        return row_parities + col_parities
    
    @staticmethod
    def verify(data, received_parity):
        """
        Verify 2D parity
        Returns: True if no error detected, False otherwise
        """
        calculated_parity = TwoDParity.generate(data)
        return calculated_parity == received_parity


class CRC(ErrorDetection):
    """Cyclic Redundancy Check Error Detection"""
    
    @staticmethod
    def generate(data, polynomial=None):
        """
        Generate CRC for data using polynomial division
        Returns: CRC value as binary string
        """
        if polynomial is None:
            polynomial = config.CRC_POLYNOMIAL
        
        # Convert data to binary
        binary = ErrorDetection.string_to_binary(data)
        
        # Polynomial degree
        poly_bin = bin(polynomial)[2:]
        degree = len(poly_bin) - 1
        
        # Append zeros
        padded = binary + '0' * degree
        
        # Perform polynomial division
        padded = list(padded)
        divisor = list(poly_bin)
        
        for i in range(len(binary)):
            if padded[i] == '1':
                for j in range(len(divisor)):
                    padded[i + j] = str(int(padded[i + j]) ^ int(divisor[j]))
        
        # CRC is the remainder
        crc = ''.join(padded[-degree:])
        return crc
    
    @staticmethod
    def verify(data, received_crc, polynomial=None):
        """
        Verify CRC
        Returns: True if no error detected, False otherwise
        """
        calculated_crc = CRC.generate(data, polynomial)
        return calculated_crc == received_crc


class HammingCode(ErrorDetection):
    """Hamming Code Error Detection and Correction"""
    
    @staticmethod
    def generate(data):
        """
        Generate Hamming code for data
        Returns: redundancy bits as string
        """
        binary = ErrorDetection.string_to_binary(data)
        
        # Calculate number of parity bits needed
        m = len(binary)
        r = 0
        while (2 ** r) < (m + r + 1):
            r += 1
        
        # Create hamming code array
        hamming = []
        j = 0
        k = 0
        
        for i in range(1, m + r + 1):
            if i == 2 ** j:
                hamming.append('0')  # Placeholder for parity bit
                j += 1
            else:
                hamming.append(binary[k])
                k += 1
        
        # Calculate parity bits
        for i in range(r):
            parity_pos = 2 ** i
            parity = 0
            for j in range(1, len(hamming) + 1):
                if j & parity_pos:
                    parity ^= int(hamming[j - 1])
            hamming[parity_pos - 1] = str(parity)
        
        # Return only parity bits for transmission
        parity_bits = ''.join(hamming[2**i - 1] for i in range(r))
        return parity_bits
    
    @staticmethod
    def verify(data, received_parity):
        """
        Verify Hamming code
        Returns: True if no error detected, False otherwise
        """
        calculated_parity = HammingCode.generate(data)
        return calculated_parity == received_parity


class InternetChecksum(ErrorDetection):
    """Internet Checksum Error Detection"""
    
    @staticmethod
    def generate(data):
        """
        Generate Internet Checksum
        Returns: checksum as hexadecimal string
        """
        # Convert data to bytes
        data_bytes = data.encode(config.ENCODING)
        
        # Calculate checksum
        checksum = 0
        
        # Process 16-bit words
        for i in range(0, len(data_bytes), 2):
            if i + 1 < len(data_bytes):
                word = (data_bytes[i] << 8) + data_bytes[i + 1]
            else:
                word = data_bytes[i] << 8
            
            checksum += word
            
            # Handle overflow (wrap around)
            if checksum > 0xFFFF:
                checksum = (checksum & 0xFFFF) + (checksum >> 16)
        
        # One's complement
        checksum = ~checksum & 0xFFFF
        
        return format(checksum, '04x')
    
    @staticmethod
    def verify(data, received_checksum):
        """
        Verify Internet Checksum
        Returns: True if no error detected, False otherwise
        """
        calculated_checksum = InternetChecksum.generate(data)
        return calculated_checksum == received_checksum


# Factory function to get error detection instance
def get_error_detector(method_name):
    """
    Get error detection class based on method name
    
    Args:
        method_name: Name of error detection method
        
    Returns:
        Error detection class
    """
    detectors = {
        'PARITY': ParityBit,
        '2D_PARITY': TwoDParity,
        'CRC': CRC,
        'HAMMING': HammingCode,
        'CHECKSUM': InternetChecksum
    }
    
    return detectors.get(method_name.upper())
