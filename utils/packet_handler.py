"""
Packet Handler utility for creating and parsing packets
Packet Format: DATA|METHOD|CONTROL_INFO
"""

import config


class Packet:
    """Packet class for handling data transmission"""
    
    def __init__(self, data=None, method=None, control_info=None):
        """Initialize packet with data, method, and control information"""
        self.data = data
        self.method = method
        self.control_info = control_info
    
    def to_string(self):
        """
        Convert packet to string format for transmission
        
        Returns:
            String in format: DATA|METHOD|CONTROL_INFO
        """
        delimiter = config.PACKET_DELIMITER
        return f"{self.data}{delimiter}{self.method}{delimiter}{self.control_info}"
    
    @classmethod
    def from_string(cls, packet_string):
        """
        Parse packet string into Packet object
        
        Args:
            packet_string: String in format DATA|METHOD|CONTROL_INFO
            
        Returns:
            Packet object
        """
        try:
            parts = packet_string.split(config.PACKET_DELIMITER)
            if len(parts) != 3:
                raise ValueError("Invalid packet format")
            
            return cls(data=parts[0], method=parts[1], control_info=parts[2])
        except Exception as e:
            raise ValueError(f"Failed to parse packet: {e}")
    
    def __str__(self):
        """String representation of packet"""
        return (f"Packet(data='{self.data}', method='{self.method}', "
                f"control_info='{self.control_info}')")
    
    def is_valid(self):
        """
        Check if packet has all required fields
        
        Returns:
            True if valid, False otherwise
        """
        return (self.data is not None and 
                self.method is not None and 
                self.control_info is not None)


def create_packet(data, method, control_info):
    """
    Create a packet object
    
    Args:
        data: Data to transmit
        method: Error detection method
        control_info: Control information (parity, CRC, etc.)
        
    Returns:
        Packet object
    """
    return Packet(data, method, control_info)


def parse_packet(packet_string):
    """
    Parse packet string into components
    
    Args:
        packet_string: String in format DATA|METHOD|CONTROL_INFO
        
    Returns:
        Packet object
    """
    return Packet.from_string(packet_string)


def validate_packet(packet):
    """
    Validate packet structure
    
    Args:
        packet: Packet object or string
        
    Returns:
        True if valid, False otherwise
    """
    if isinstance(packet, str):
        try:
            packet = Packet.from_string(packet)
        except ValueError:
            return False
    
    return packet.is_valid()
