"""
Test cases for packet handler
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from utils.packet_handler import Packet, create_packet, parse_packet, validate_packet


class TestPacket:
    """Test cases for Packet class"""
    
    def test_create_packet(self):
        """Test packet creation"""
        packet = Packet("Hello", "PARITY", "1")
        assert packet.data == "Hello"
        assert packet.method == "PARITY"
        assert packet.control_info == "1"
    
    def test_packet_to_string(self):
        """Test packet serialization"""
        packet = Packet("Test", "CRC", "10101")
        packet_string = packet.to_string()
        assert packet_string == "Test|CRC|10101"
    
    def test_packet_from_string(self):
        """Test packet deserialization"""
        packet_string = "Hello|PARITY|1"
        packet = Packet.from_string(packet_string)
        assert packet.data == "Hello"
        assert packet.method == "PARITY"
        assert packet.control_info == "1"
    
    def test_packet_is_valid(self):
        """Test packet validation"""
        valid_packet = Packet("Data", "CRC", "1010")
        assert valid_packet.is_valid() == True
        
        invalid_packet = Packet("Data", None, "1010")
        assert invalid_packet.is_valid() == False
    
    def test_invalid_packet_format(self):
        """Test parsing invalid packet format"""
        with pytest.raises(ValueError):
            Packet.from_string("Invalid|Format")


class TestPacketFunctions:
    """Test packet utility functions"""
    
    def test_create_packet_function(self):
        """Test create_packet function"""
        packet = create_packet("Test", "HAMMING", "0101")
        assert isinstance(packet, Packet)
        assert packet.data == "Test"
    
    def test_parse_packet_function(self):
        """Test parse_packet function"""
        packet = parse_packet("Data|CHECKSUM|abcd")
        assert packet.data == "Data"
        assert packet.method == "CHECKSUM"
        assert packet.control_info == "abcd"
    
    def test_validate_packet_string(self):
        """Test validate_packet with string"""
        assert validate_packet("Data|CRC|1010") == True
        assert validate_packet("Invalid") == False
    
    def test_validate_packet_object(self):
        """Test validate_packet with Packet object"""
        valid = Packet("Data", "PARITY", "1")
        assert validate_packet(valid) == True
        
        invalid = Packet(None, "PARITY", "1")
        assert validate_packet(invalid) == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
