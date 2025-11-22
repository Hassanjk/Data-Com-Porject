"""
Server - Intermediate Node and Data Corruptor
Receives data from Client 1, corrupts it, and forwards to Client 2
"""

import socket
import sys
import os
import threading

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from utils.packet_handler import parse_packet, create_packet
from utils.logger_utils import (
    Logger, print_header, print_section, print_colored,
    print_success, print_error, print_info, print_packet_info
)
from error_injector import get_error_injector


class Server:
    """Server - Intermediate Node with Error Injection"""
    
    def __init__(self):
        """Initialize Server"""
        self.logger = Logger('Server', 'server.log')
        self.client1_socket = None
        self.client2_socket = None
        self.running = False
        
    def start(self):
        """Start the server"""
        print_header("Server - Intermediate Node & Data Corruptor")
        
        try:
            # Create socket for Client 1
            self.client1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client1_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.client1_socket.bind((config.SERVER_HOST, config.SERVER_TO_CLIENT1_PORT))
            self.client1_socket.listen(1)
            
            print_success(f"Server listening for Client 1 on port {config.SERVER_TO_CLIENT1_PORT}")
            self.logger.info(f"Server started on port {config.SERVER_TO_CLIENT1_PORT}")
            
            self.running = True
            self.accept_connections()
            
        except Exception as e:
            print_error(f"Failed to start server: {e}")
            self.logger.error(f"Server start failed: {e}")
    
    def accept_connections(self):
        """Accept connections from Client 1"""
        print_info("Waiting for Client 1 to connect...")
        
        while self.running:
            try:
                conn, addr = self.client1_socket.accept()
                print_success(f"Client 1 connected from {addr}")
                self.logger.info(f"Client 1 connected: {addr}")
                
                # Handle client in a separate thread
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print_error(f"Error accepting connection: {e}")
                    self.logger.error(f"Connection accept error: {e}")
    
    def select_error_injection(self):
        """
        Select error injection method
        
        Returns:
            Error injection function
        """
        print_section("Select Error Injection Method")
        for key, value in config.ERROR_INJECTION_TYPES.items():
            print(f"  {key}. {value}")
        print()
        
        choice = input("Select injection method (1-8) [default: 1]: ").strip()
        
        if not choice:
            choice = '1'
        
        if choice not in config.ERROR_INJECTION_TYPES:
            print_error("Invalid choice, using BIT_FLIP")
            choice = '1'
        
        injection_type = config.ERROR_INJECTION_TYPES[choice]
        print_info(f"Selected: {injection_type}")
        
        return get_error_injector(injection_type), injection_type
    
    def corrupt_data(self, data, injector_func, injection_type):
        """
        Apply error injection to data
        
        Args:
            data: Original data
            injector_func: Error injection function
            injection_type: Name of injection type
            
        Returns:
            Corrupted data
        """
        try:
            corrupted = injector_func(data)
            
            print_section("Data Corruption")
            print(f"  Original:  {data}")
            print(f"  Corrupted: {corrupted}")
            print(f"  Method:    {injection_type}")
            
            self.logger.info(f"Applied {injection_type}: '{data}' -> '{corrupted}'")
            return corrupted
        except Exception as e:
            print_error(f"Error during corruption: {e}")
            self.logger.error(f"Corruption failed: {e}")
            return data
    
    def forward_to_client2(self, packet):
        """
        Forward packet to Client 2
        
        Args:
            packet: Packet object to forward
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Connect to Client 2
            client2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client2_socket.connect((config.SERVER_HOST, config.SERVER_TO_CLIENT2_PORT))
            
            # Send packet
            packet_string = packet.to_string()
            client2_socket.sendall(packet_string.encode(config.ENCODING))
            
            print_success("Packet forwarded to Client 2")
            self.logger.info(f"Forwarded to Client 2: {packet_string}")
            
            client2_socket.close()
            return True
            
        except Exception as e:
            print_error(f"Failed to forward to Client 2: {e}")
            self.logger.error(f"Forward failed: {e}")
            return False
    
    def handle_client(self, conn, addr):
        """
        Handle communication with Client 1
        
        Args:
            conn: Socket connection
            addr: Client address
        """
        try:
            while True:
                # Receive data
                data = conn.recv(config.BUFFER_SIZE)
                
                if not data:
                    print_info("Client 1 disconnected")
                    break
                
                # Parse packet
                packet_string = data.decode(config.ENCODING)
                print_packet_info({'data': packet_string, 'method': 'RAW', 'control_info': 'N/A'}, 
                                "Received from Client 1")
                
                packet = parse_packet(packet_string)
                
                # Select error injection method
                injector_func, injection_type = self.select_error_injection()
                
                # Corrupt data
                corrupted_data = self.corrupt_data(packet.data, injector_func, injection_type)
                
                # Create new packet with corrupted data
                corrupted_packet = create_packet(corrupted_data, packet.method, packet.control_info)
                
                print_packet_info(corrupted_packet, "Packet to Forward")
                
                # Forward to Client 2
                self.forward_to_client2(corrupted_packet)
                
                print_colored("\n" + "-" * 60 + "\n", 'cyan')
                
        except Exception as e:
            print_error(f"Error handling client: {e}")
            self.logger.error(f"Client handling error: {e}")
        finally:
            conn.close()
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if self.client1_socket:
            self.client1_socket.close()
        print_info("Server stopped")
        self.logger.info("Server stopped")


def main():
    """Main entry point"""
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        print_info("\n\nServer interrupted by user")
        server.stop()
    except Exception as e:
        print_error(f"Server error: {e}")


if __name__ == "__main__":
    main()
