# Socket Error Detection Project

A socket programming implementation demonstrating various error detection methods in data communication. This project simulates data transmission with error injection and detection using methods like Parity Bit, 2D Parity, CRC, Hamming Code, and Internet Checksum.

## 📋 Project Overview

This project consists of three main components:
- **Client 1 (Sender)**: Sends data with error detection codes
- **Server (Intermediate Node)**: Receives data, injects errors, and forwards to Client 2
- **Client 2 (Receiver)**: Receives data and verifies integrity using error detection

## 🔧 Features

### Error Detection Methods
1. **Parity Bit** - Even parity error detection
2. **2D Parity** - Matrix-based parity with row and column checks
3. **CRC (Cyclic Redundancy Check)** - Polynomial-based error detection
4. **Hamming Code** - Error detection with correction capability
5. **Internet Checksum** - IP-style checksum calculation

### Error Injection Methods
1. **Bit Flip** - Flip random bits in data
2. **Character Substitution** - Replace characters with random ones
3. **Character Deletion** - Remove random characters
4. **Character Insertion** - Insert random characters
5. **Character Swapping** - Swap adjacent characters
6. **Multiple Bit Flips** - Flip multiple bits simultaneously
7. **Burst Error** - Consecutive bit errors
8. **No Error** - Pass data without corruption (for testing)

## 📁 Project Structure

```
socket_error_detection/
├── client1/
│   ├── __init__.py
│   └── client1.py          # Data sender
├── client2/
│   ├── __init__.py
│   └── client2.py          # Data receiver and verifier
├── server/
│   ├── __init__.py
│   ├── server.py           # Intermediate node
│   └── error_injector.py   # Error injection methods
├── utils/
│   ├── __init__.py
│   ├── error_detection.py  # Error detection algorithms
│   ├── packet_handler.py   # Packet creation and parsing
│   └── logger_utils.py     # Logging utilities
├── tests/
│   └── (test files)
├── logs/                   # Auto-generated log files
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── setup_env.bat          # Environment setup script
├── run_server.bat         # Server launcher
├── run_client1.bat        # Client 1 launcher
├── run_client2.bat        # Client 2 launcher
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Setup Environment

Double-click `setup_env.bat` or run in command prompt:

```cmd
setup_env.bat
```

This will:
- Create a virtual environment
- Install all dependencies
- Set up the project

### 2. Run the Project

**IMPORTANT: Start in this order:**

#### Step 1: Start the Server
```cmd
run_server.bat
```
Or manually:
```cmd
venv\Scripts\activate.bat
python server\server.py
```

#### Step 2: Start Client 2 (Receiver)
```cmd
run_client2.bat
```
Or manually:
```cmd
venv\Scripts\activate.bat
python client2\client2.py
```

#### Step 3: Start Client 1 (Sender)
```cmd
run_client1.bat
```
Or manually:
```cmd
venv\Scripts\activate.bat
python client1\client1.py
```

## 💻 Usage

### Client 1 (Sender)
1. Enter the data you want to send
2. Select an error detection method (1-5)
3. The program will generate control information and send the packet

### Server (Intermediate Node)
1. Receives packet from Client 1
2. Prompts you to select an error injection method (1-8)
3. Corrupts the data according to selected method
4. Forwards the corrupted packet to Client 2

### Client 2 (Receiver)
1. Automatically receives packets from the server
2. Recalculates control information from received data
3. Compares with original control information
4. Displays whether corruption was detected

## 📊 Example Workflow

```
Client 1 → [Data: "Hello", Method: PARITY, Control: "1"]
    ↓
Server → [Applies BIT_FLIP error]
    ↓
Client 2 → [Receives: "Iello", Calculates: "0", Detects: CORRUPTION]
```

## ⚙️ Configuration

Edit `config.py` to modify:
- Port numbers
- Buffer sizes
- Error detection parameters
- Logging settings

```python
SERVER_HOST = 'localhost'
SERVER_TO_CLIENT1_PORT = 5001
SERVER_TO_CLIENT2_PORT = 5002
BUFFER_SIZE = 4096
```

## 🧪 Testing

Run tests using:
```cmd
venv\Scripts\activate.bat
pytest tests/
```

## 📝 Packet Format

All data is transmitted in the following format:
```
DATA|METHOD|CONTROL_INFO
```

Example:
```
Hello World|CRC|10110101
```

## 🔍 Logging

- Logs are automatically saved in the `logs/` directory
- Each component has its own log file:
  - `client1.log`
  - `server.log`
  - `client2.log`

## 🐛 Troubleshooting

### Port Already in Use
If you get a port error, either:
1. Change port numbers in `config.py`
2. Kill the process using the port

### Import Errors
Make sure you:
1. Activated the virtual environment
2. Installed all dependencies: `pip install -r requirements.txt`

### Connection Refused
Ensure components are started in the correct order:
1. Server first
2. Client 2 second
3. Client 1 last

## 🛠️ Requirements

- Python 3.8 or higher
- Windows OS (batch scripts provided for Windows)
- Dependencies listed in `requirements.txt`

## 📦 Dependencies

```
colorama==0.4.6          # Colored console output
prompt-toolkit==3.0.43   # Enhanced CLI interface
pytest==7.4.3            # Testing framework
pytest-cov==4.1.0        # Test coverage
```

## 🎓 Educational Purpose

This project demonstrates:
- Socket programming concepts
- Client-server architecture
- Error detection algorithms
- Network reliability mechanisms
- Multi-threaded server design

## 📚 References

- Computer Networks (Tanenbaum)
- TCP/IP Protocol Suite
- Error Detection and Correction techniques

## 👤 Author

Created for Socket Programming Assignment - Error Detection Methods

## 📄 License

This project is for educational purposes.

---

## 🎯 Assignment Requirements Checklist

✅ Client 1 implementation (Data Sender)  
✅ Server implementation (Intermediate Node + Corruptor)  
✅ Client 2 implementation (Receiver + Error Checker)  
✅ Parity Bit error detection  
✅ 2D Parity error detection  
✅ CRC error detection  
✅ Hamming Code error detection  
✅ Internet Checksum error detection  
✅ Multiple error injection methods  
✅ Packet format: DATA|METHOD|CONTROL_INFO  
✅ Proper logging and output display  

---

**Happy Error Detecting! 🔍**
