"""
Client 1 - Data Sender
Sends data with error detection codes to the server
"""

import socket
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from utils.error_detection import get_error_detector
from utils.packet_handler import create_packet
from utils.logger_utils import (
    Logger, print_header, print_section, print_colored,
    print_success, print_error, print_info, print_packet_info
)


class Client1:
    """Client 1 - Data Sender"""
    
    def __init__(self):
        """Initialize Client 1"""
        self.logger = Logger('Client1', 'client1.log')
        self.socket = None
        
    def connect_to_server(self):
        """Establish connection to server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((config.SERVER_HOST, config.SERVER_TO_CLIENT1_PORT))
            print_success(f"Connected to server at {config.SERVER_HOST}:{config.SERVER_TO_CLIENT1_PORT}")
            self.logger.info("Connected to server")
            return True
        except Exception as e:
            print_error(f"Failed to connect to server: {e}")
            self.logger.error(f"Connection failed: {e}")
            return False
    
    def display_menu(self):
        """Display error detection method menu"""
        print_section("Select Error Detection Method")
        for key, value in config.ERROR_DETECTION_METHODS.items():
            print(f"  {key}. {value}")
        print()
    
    def get_user_input(self):
        """
        Get user input for data and error detection method
        
        Returns:
            tuple: (data, method_name) or (None, None) if user wants to quit
        """
        print_section("Data Input")
        
        # Get data from user
        data = input("Enter data to send (or 'quit' to exit): ").strip()
        
        if data.lower() == 'quit':
            return None, None
        
        if not data:
            print_error("Data cannot be empty!")
            return None, None
        
        # Display and select error detection method
        self.display_menu()
        method_choice = input("Select method (1-5): ").strip()
        
        if method_choice not in config.ERROR_DETECTION_METHODS:
            print_error("Invalid method selection!")
            return None, None
        
        method_name = config.ERROR_DETECTION_METHODS[method_choice]
        return data, method_name
    
    def generate_control_info(self, data, method_name):
        """
        Generate control information using selected error detection method
        
        Args:
            data: Data string
            method_name: Name of error detection method
            
        Returns:
            Control information string
        """
        try:
            detector_class = get_error_detector(method_name)
            if not detector_class:
                raise ValueError(f"Unknown method: {method_name}")
            
            control_info = detector_class.generate(data)
            self.logger.info(f"Generated {method_name} control info: {control_info}")
            return control_info
        except Exception as e:
            print_error(f"Failed to generate control info: {e}")
            self.logger.error(f"Control info generation failed: {e}")
            return None
    
    def send_packet(self, packet):
        """
        Send packet to server
        
        Args:
            packet: Packet object
            
        Returns:
            True if successful, False otherwise
        """
        try:
            packet_string = packet.to_string()
            self.socket.sendall(packet_string.encode(config.ENCODING))
            
            print_success("Packet sent successfully!")
            print_packet_info(packet, "Sent Packet")
            
            self.logger.info(f"Sent packet: {packet_string}")
            return True
        except Exception as e:
            print_error(f"Failed to send packet: {e}")
            self.logger.error(f"Send failed: {e}")
            return False
    
    def close_connection(self):
        """Close connection to server"""
        if self.socket:
            try:
                self.socket.close()
                print_info("Connection closed")
                self.logger.info("Connection closed")
            except Exception as e:
                self.logger.error(f"Error closing connection: {e}")
    
    def run(self):
        """Main execution loop for Client 1"""
        print_header("Client 1 - Data Sender")
        
        # Connect to server
        if not self.connect_to_server():
            return
        
        try:
            while True:
                # Get user input
                data, method_name = self.get_user_input()
                
                if data is None:
                    print_info("Exiting...")
                    break
                
                # Generate control information
                control_info = self.generate_control_info(data, method_name)
                if control_info is None:
                    continue
                
                # Create packet
                packet = create_packet(data, method_name, control_info)
                
                # Send packet
                if not self.send_packet(packet):
                    break
                
                print_colored("\n" + "-" * 60 + "\n", 'cyan')
                
        except KeyboardInterrupt:
            print_info("\n\nInterrupted by user")
        except Exception as e:
            print_error(f"Error: {e}")
            self.logger.error(f"Runtime error: {e}")
        finally:
            self.close_connection()


def main():
    """Main entry point"""
    client = Client1()
    client.run()


if __name__ == "__main__":
    main()
