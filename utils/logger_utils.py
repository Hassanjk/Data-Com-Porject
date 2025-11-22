"""
Logging utilities for the socket error detection project
"""

import os
import logging
from datetime import datetime
import config

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


class Logger:
    """Custom logger for the project"""
    
    def __init__(self, name, log_file=None):
        """
        Initialize logger
        
        Args:
            name: Logger name (typically module name)
            log_file: Optional log file name
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, config.LOG_LEVEL))
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Console handler
        if config.ENABLE_CONSOLE_LOGGING:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        
        # File handler
        if config.ENABLE_FILE_LOGGING and log_file:
            # Create logs directory if it doesn't exist
            if not os.path.exists(config.LOG_DIRECTORY):
                os.makedirs(config.LOG_DIRECTORY)
            
            log_path = os.path.join(config.LOG_DIRECTORY, log_file)
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)


def print_colored(message, color='white', bold=False):
    """
    Print colored message to console
    
    Args:
        message: Message to print
        color: Color name (red, green, yellow, blue, magenta, cyan, white)
        bold: Whether to print in bold
    """
    if not COLORAMA_AVAILABLE or not config.COLORS_ENABLED:
        print(message)
        return
    
    color_map = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE
    }
    
    color_code = color_map.get(color.lower(), Fore.WHITE)
    style = Style.BRIGHT if bold else ''
    
    print(f"{style}{color_code}{message}{Style.RESET_ALL}")


def print_header(title):
    """Print a formatted header"""
    print_colored("\n" + "=" * 60, 'cyan', bold=True)
    print_colored(f"  {title}", 'cyan', bold=True)
    print_colored("=" * 60 + "\n", 'cyan', bold=True)


def print_section(title):
    """Print a section separator"""
    print_colored(f"\n--- {title} ---", 'yellow', bold=True)


def print_success(message):
    """Print success message"""
    print_colored(f"✓ {message}", 'green', bold=True)


def print_error(message):
    """Print error message"""
    print_colored(f"✗ {message}", 'red', bold=True)


def print_info(message):
    """Print info message"""
    print_colored(f"ℹ {message}", 'blue')


def print_packet_info(packet, title="Packet Information"):
    """
    Print formatted packet information
    
    Args:
        packet: Packet object or dict with data, method, control_info
        title: Title for the packet info
    """
    print_section(title)
    
    if hasattr(packet, 'data'):
        print(f"  Data:         {packet.data}")
        print(f"  Method:       {packet.method}")
        print(f"  Control Info: {packet.control_info}")
    else:
        print(f"  Data:         {packet.get('data', 'N/A')}")
        print(f"  Method:       {packet.get('method', 'N/A')}")
        print(f"  Control Info: {packet.get('control_info', 'N/A')}")


def log_transmission(source, destination, data, method, control_info):
    """
    Log transmission details
    
    Args:
        source: Source of transmission
        destination: Destination of transmission
        data: Transmitted data
        method: Error detection method
        control_info: Control information
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] Transmission: {source} -> {destination}")
    print(f"  Data:         {data}")
    print(f"  Method:       {method}")
    print(f"  Control Info: {control_info}")
