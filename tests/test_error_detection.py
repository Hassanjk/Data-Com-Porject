"""
Test cases for error detection methods
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from utils.error_detection import (
    ParityBit, TwoDParity, CRC, HammingCode, InternetChecksum
)


class TestParityBit:
    """Test cases for Parity Bit"""
    
    def test_generate_even_parity(self):
        """Test parity generation"""
        # Test data with even number of 1s
        data = "A"  # 01000001 - one 1, needs parity 1
        parity = ParityBit.generate(data)
        assert parity in ['0', '1']
    
    def test_verify_correct_parity(self):
        """Test parity verification with correct data"""
        data = "Hello"
        parity = ParityBit.generate(data)
        assert ParityBit.verify(data, parity) == True
    
    def test_verify_incorrect_parity(self):
        """Test parity verification with corrupted data"""
        data = "Hello"
        parity = ParityBit.generate(data)
        
        # Corrupt data
        corrupted = "Hallo"
        assert ParityBit.verify(corrupted, parity) == False


class TestTwoDParity:
    """Test cases for 2D Parity"""
    
    def test_generate_2d_parity(self):
        """Test 2D parity generation"""
        data = "Test"
        parity = TwoDParity.generate(data)
        assert isinstance(parity, str)
        assert len(parity) > 0
    
    def test_verify_correct_2d_parity(self):
        """Test 2D parity verification with correct data"""
        data = "Test123"
        parity = TwoDParity.generate(data)
        assert TwoDParity.verify(data, parity) == True
    
    def test_verify_incorrect_2d_parity(self):
        """Test 2D parity verification with corrupted data"""
        data = "Test123"
        parity = TwoDParity.generate(data)
        
        corrupted = "Best123"
        assert TwoDParity.verify(corrupted, parity) == False


class TestCRC:
    """Test cases for CRC"""
    
    def test_generate_crc(self):
        """Test CRC generation"""
        data = "Hello"
        crc = CRC.generate(data)
        assert isinstance(crc, str)
        assert len(crc) > 0
    
    def test_verify_correct_crc(self):
        """Test CRC verification with correct data"""
        data = "Network"
        crc = CRC.generate(data)
        assert CRC.verify(data, crc) == True
    
    def test_verify_incorrect_crc(self):
        """Test CRC verification with corrupted data"""
        data = "Network"
        crc = CRC.generate(data)
        
        corrupted = "Netwark"
        assert CRC.verify(corrupted, crc) == False


class TestHammingCode:
    """Test cases for Hamming Code"""
    
    def test_generate_hamming(self):
        """Test Hamming code generation"""
        data = "AB"
        hamming = HammingCode.generate(data)
        assert isinstance(hamming, str)
        assert len(hamming) > 0
    
    def test_verify_correct_hamming(self):
        """Test Hamming verification with correct data"""
        data = "Test"
        hamming = HammingCode.generate(data)
        assert HammingCode.verify(data, hamming) == True
    
    def test_verify_incorrect_hamming(self):
        """Test Hamming verification with corrupted data"""
        data = "Test"
        hamming = HammingCode.generate(data)
        
        corrupted = "Best"
        assert HammingCode.verify(corrupted, hamming) == False


class TestInternetChecksum:
    """Test cases for Internet Checksum"""
    
    def test_generate_checksum(self):
        """Test checksum generation"""
        data = "Hello World"
        checksum = InternetChecksum.generate(data)
        assert isinstance(checksum, str)
        assert len(checksum) == 4  # Hex representation
    
    def test_verify_correct_checksum(self):
        """Test checksum verification with correct data"""
        data = "Testing"
        checksum = InternetChecksum.generate(data)
        assert InternetChecksum.verify(data, checksum) == True
    
    def test_verify_incorrect_checksum(self):
        """Test checksum verification with corrupted data"""
        data = "Testing"
        checksum = InternetChecksum.generate(data)
        
        corrupted = "Texting"
        assert InternetChecksum.verify(corrupted, checksum) == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
