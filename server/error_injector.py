"""
Error injection methods for simulating transmission errors
"""

import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class ErrorInjector:
    """Class containing various error injection methods"""
    
    @staticmethod
    def bit_flip(data, num_flips=1):
        """
        Flip random bits in the data
        
        Args:
            data: Input string
            num_flips: Number of bits to flip
            
        Returns:
            Corrupted data
        """
        if not data:
            return data
        
        # Convert to binary
        binary = ''.join(format(ord(char), '08b') for char in data)
        binary_list = list(binary)
        
        # Flip random bits
        for _ in range(num_flips):
            if len(binary_list) > 0:
                pos = random.randint(0, len(binary_list) - 1)
                binary_list[pos] = '0' if binary_list[pos] == '1' else '1'
        
        # Convert back to string
        binary_str = ''.join(binary_list)
        chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
        
        try:
            result = ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)
            return result
        except ValueError:
            return data
    
    @staticmethod
    def char_substitution(data):
        """
        Replace a random character with another random character
        
        Args:
            data: Input string
            
        Returns:
            Corrupted data
        """
        if len(data) < 1:
            return data
        
        data_list = list(data)
        pos = random.randint(0, len(data_list) - 1)
        
        # Random ASCII printable character
        new_char = chr(random.randint(33, 126))
        data_list[pos] = new_char
        
        return ''.join(data_list)
    
    @staticmethod
    def char_deletion(data):
        """
        Delete a random character
        
        Args:
            data: Input string
            
        Returns:
            Corrupted data
        """
        if len(data) < 1:
            return data
        
        pos = random.randint(0, len(data) - 1)
        return data[:pos] + data[pos+1:]
    
    @staticmethod
    def char_insertion(data):
        """
        Insert a random character at a random position
        
        Args:
            data: Input string
            
        Returns:
            Corrupted data
        """
        if not data:
            return data
        
        pos = random.randint(0, len(data))
        new_char = chr(random.randint(33, 126))
        
        return data[:pos] + new_char + data[pos:]
    
    @staticmethod
    def char_swap(data):
        """
        Swap two adjacent characters
        
        Args:
            data: Input string
            
        Returns:
            Corrupted data
        """
        if len(data) < 2:
            return data
        
        pos = random.randint(0, len(data) - 2)
        data_list = list(data)
        data_list[pos], data_list[pos + 1] = data_list[pos + 1], data_list[pos]
        
        return ''.join(data_list)
    
    @staticmethod
    def multiple_bit_flips(data, num_flips=3):
        """
        Flip multiple random bits
        
        Args:
            data: Input string
            num_flips: Number of bits to flip
            
        Returns:
            Corrupted data
        """
        return ErrorInjector.bit_flip(data, num_flips)
    
    @staticmethod
    def burst_error(data, burst_length=3):
        """
        Introduce a burst error (consecutive bit flips)
        
        Args:
            data: Input string
            burst_length: Number of consecutive bits to flip
            
        Returns:
            Corrupted data
        """
        if not data:
            return data
        
        # Convert to binary
        binary = ''.join(format(ord(char), '08b') for char in data)
        binary_list = list(binary)
        
        if len(binary_list) < burst_length:
            burst_length = len(binary_list)
        
        # Choose random starting position
        start_pos = random.randint(0, len(binary_list) - burst_length)
        
        # Flip consecutive bits
        for i in range(start_pos, start_pos + burst_length):
            binary_list[i] = '0' if binary_list[i] == '1' else '1'
        
        # Convert back to string
        binary_str = ''.join(binary_list)
        chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
        
        try:
            result = ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)
            return result
        except ValueError:
            return data
    
    @staticmethod
    def no_error(data):
        """
        Return data without any corruption (for testing)
        
        Args:
            data: Input string
            
        Returns:
            Original data unchanged
        """
        return data


def get_error_injector(injection_type):
    """
    Get error injection function based on type
    
    Args:
        injection_type: Name of error injection type
        
    Returns:
        Error injection function
    """
    injectors = {
        'BIT_FLIP': ErrorInjector.bit_flip,
        'CHAR_SUBSTITUTION': ErrorInjector.char_substitution,
        'CHAR_DELETION': ErrorInjector.char_deletion,
        'CHAR_INSERTION': ErrorInjector.char_insertion,
        'CHAR_SWAP': ErrorInjector.char_swap,
        'MULTIPLE_BIT_FLIPS': ErrorInjector.multiple_bit_flips,
        'BURST_ERROR': ErrorInjector.burst_error,
        'NO_ERROR': ErrorInjector.no_error
    }
    
    return injectors.get(injection_type.upper())
