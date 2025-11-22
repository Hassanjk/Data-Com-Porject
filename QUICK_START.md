# Quick Start Guide

## 🚀 Running the Project

### Step 1: Open Three Terminals (Command Prompts)

You need to run three programs simultaneously. Open 3 separate Command Prompt windows.

### Step 2: Run in Order

**IMPORTANT:** Your required packages are already installed in system Python, so you can run directly OR use the virtual environment (recommended for best practice).

#### Option A: Direct Run (Works because packages are in system Python)

**Terminal 1 - Start Server:**
```cmd
cd "c:\Users\ThinkMaster\Documents\Andy\socket_error_detection"
python server\server.py
```

**Terminal 2 - Start Client 2 (Receiver):**
```cmd
cd "c:\Users\ThinkMaster\Documents\Andy\socket_error_detection"
python client2\client2.py
```

**Terminal 3 - Start Client 1 (Sender):**
```cmd
cd "c:\Users\ThinkMaster\Documents\Andy\socket_error_detection"
python client1\client1.py
```

#### Option B: Using Virtual Environment (Best Practice)

**Terminal 1 - Start Server:**
```cmd
cd "c:\Users\ThinkMaster\Documents\Andy\socket_error_detection"
venv\Scripts\activate.bat
python server\server.py
```

**Terminal 2 - Start Client 2 (Receiver):**
```cmd
cd "c:\Users\ThinkMaster\Documents\Andy\socket_error_detection"
venv\Scripts\activate.bat
python client2\client2.py
```

**Terminal 3 - Start Client 1 (Sender):**
```cmd
cd "c:\Users\ThinkMaster\Documents\Andy\socket_error_detection"
venv\Scripts\activate.bat
python client1\client1.py
```

### Step 3: Test the System

In **Client 1 terminal**:
1. Type some text (e.g., "Hello World")
2. Select error detection method (1-5)

In **Server terminal**:
- Select error injection type (1-8)

In **Client 2 terminal**:
- View the results automatically

## 📝 Example Test Run

### Test 1: Parity Bit with Bit Flip
- Client 1: Enter "Test" → Select "1" (PARITY)
- Server: Select "1" (BIT_FLIP)
- Client 2: Will show if corruption detected

### Test 2: CRC with No Error
- Client 1: Enter "Network" → Select "3" (CRC)
- Server: Select "8" (NO_ERROR)
- Client 2: Should show NO CORRUPTION

### Test 3: Hamming with Character Substitution
- Client 1: Enter "Hello" → Select "4" (HAMMING)
- Server: Select "2" (CHAR_SUBSTITUTION)
- Client 2: Will detect corruption

## 🛠️ If You Get Errors

### "Address already in use"
Someone is already using the port. Either:
- Close the other program using that port
- OR change ports in `config.py`

### "Connection refused"
Make sure you started programs in correct order:
1. Server FIRST
2. Client 2 SECOND
3. Client 1 LAST

### Import errors
- If using system Python: Packages are already installed
- If using venv: Make sure you activated it with `venv\Scripts\activate.bat`
- If packages are missing: Run `pip install -r requirements.txt`

## 📊 Understanding the Output

### Client 1 shows:
- Data you're sending
- Method selected
- Generated control information

### Server shows:
- Original data received
- Corrupted data
- Method of corruption

### Client 2 shows:
- Received data
- Received control info
- Calculated control info
- ✓ or ✗ corruption status

## 💡 Tips

1. **To quit Client 1:** Type "quit" when asked for data
2. **To stop Server or Client 2:** Press Ctrl+C
3. **Multiple tests:** Keep all programs running and send multiple messages from Client 1
4. **Try all methods:** Test each error detection method (1-5) with different error injections (1-8)

## 🎯 Assignment Requirements Tested

✅ All 5 error detection methods implemented  
✅ All 8 error injection types working  
✅ Packet format: DATA|METHOD|CONTROL_INFO  
✅ Client 1 → Server → Client 2 communication  
✅ Error detection and reporting  

---

**Ready to test! Start with Server, then Client 2, then Client 1.**
