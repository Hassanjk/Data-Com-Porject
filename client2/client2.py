"""
Client 2 - Data Receiver and Error Checker
Receives data from server and verifies error detection codes
"""

import socket
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from utils.error_detection import get_error_detector
from utils.packet_handler import parse_packet
from utils.logger_utils import (
    Logger, print_header, print_section, print_colored,
    print_success, print_error, print_info
)


class Client2:
    """Client 2 - Data Receiver and Error Checker"""
    
    def __init__(self):
        """Initialize Client 2"""
        self.logger = Logger('Client2', 'client2.log')
        self.socket = None
        self.server_socket = None
        
    def start_server(self):
        """Start listening for connections from server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((config.SERVER_HOST, config.SERVER_TO_CLIENT2_PORT))
            self.server_socket.listen(1)
            
            print_success(f"Client 2 listening on port {config.SERVER_TO_CLIENT2_PORT}")
            self.logger.info(f"Client 2 started on port {config.SERVER_TO_CLIENT2_PORT}")
            return True
        except Exception as e:
            print_error(f"Failed to start Client 2: {e}")
            self.logger.error(f"Start failed: {e}")
            return False
    
    def verify_data(self, data, method, received_control_info):
        """
        Verify data using error detection method
        
        Args:
            data: Received data
            method: Error detection method name
            received_control_info: Control info from sender
            
        Returns:
            tuple: (calculated_control_info, is_valid)
        """
        try:
            # Get error detector
            detector_class = get_error_detector(method)
            if not detector_class:
                print_error(f"Unknown method: {method}")
                return None, False
            
            # Calculate control info from received data
            calculated_control_info = detector_class.generate(data)
            
            # Verify
            is_valid = detector_class.verify(data, received_control_info)
            
            self.logger.info(f"Verification - Method: {method}, Valid: {is_valid}")
            return calculated_control_info, is_valid
            
        except Exception as e:
            print_error(f"Verification error: {e}")
            self.logger.error(f"Verification failed: {e}")
            return None, False
    
    def display_results(self, packet, calculated_control_info, is_valid):
        """
        Display verification results
        
        Args:
            packet: Received packet
            calculated_control_info: Calculated control information
            is_valid: Whether data is valid
        """
        print_section("Packet Received")
        print(f"  Data:                 {packet.data}")
        print(f"  Method:               {packet.method}")
        print(f"  Received Control:     {packet.control_info}")
        print(f"  Calculated Control:   {calculated_control_info}")
        
        print_section("Verification Result")
        if is_valid:
            print_success("✓ NO CORRUPTION DETECTED - Data integrity verified")
        else:
            print_error("✗ CORRUPTION DETECTED - Data integrity compromised")
        
        # Display in binary for comparison (for debugging)
        if packet.control_info != calculated_control_info:
            print_section("Detailed Comparison")
            print(f"  Expected: {packet.control_info}")
            print(f"  Got:      {calculated_control_info}")
    
    def handle_connection(self, conn, addr):
        """
        Handle incoming connection from server
        
        Args:
            conn: Socket connection
            addr: Server address
        """
        try:
            # Receive data
            data = conn.recv(config.BUFFER_SIZE)
            
            if not data:
                return
            
            # Parse packet
            packet_string = data.decode(config.ENCODING)
            packet = parse_packet(packet_string)
            
            print_colored("\n" + "=" * 60, 'cyan', bold=True)
            print_info(f"Received packet from server ({addr})")
            
            # Verify data
            calculated_control_info, is_valid = self.verify_data(
                packet.data, 
                packet.method, 
                packet.control_info
            )
            
            # Display results
            self.display_results(packet, calculated_control_info, is_valid)
            
            print_colored("=" * 60 + "\n", 'cyan', bold=True)
            
        except Exception as e:
            print_error(f"Error handling connection: {e}")
            self.logger.error(f"Connection handling error: {e}")
        finally:
            conn.close()
    
    def run(self):
        """Main execution loop for Client 2"""
        print_header("Client 2 - Data Receiver & Error Checker")
        
        # Start server
        if not self.start_server():
            return
        
        print_info("Waiting for data from server...\n")
        
        try:
            while True:
                # Accept connection from server
                conn, addr = self.server_socket.accept()
                
                # Handle connection
                self.handle_connection(conn, addr)
                
        except KeyboardInterrupt:
            print_info("\n\nInterrupted by user")
        except Exception as e:
            print_error(f"Error: {e}")
            self.logger.error(f"Runtime error: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
                self.logger.info("Server socket closed")
    
    def stop(self):
        """Stop Client 2"""
        if self.server_socket:
            self.server_socket.close()
        print_info("Client 2 stopped")
        self.logger.info("Client 2 stopped")


def main():
    """Main entry point"""
    client = Client2()
    client.run()


if __name__ == "__main__":
    main()
