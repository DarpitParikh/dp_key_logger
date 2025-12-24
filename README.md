# ⌨️ Keylogger Monitor

A real-time keyboard activity monitoring application built with Streamlit. Track, analyze, and log keyboard input with an intuitive web-based interface.

**⚠️ EDUCATIONAL PURPOSE ONLY** - This tool is designed for legitimate monitoring on systems you own or have explicit permission to monitor.

---

## ✨ Features

- 🎯 **Real-time Keystroke Capture** - Monitor keyboard input as it happens
- 📊 **Live Statistics** - View keystroke counts, typing speed, and activity metrics
- 💾 **Log Export** - Save captured keystrokes to JSON format
- 📝 **Text Reconstruction** - View reconstructed text from captured keys
- 🔄 **Session Management** - Track multiple logging sessions
- 🎨 **Modern UI** - Clean, responsive Streamlit interface
- 🔐 **Session Isolation** - Each session has a unique ID

---

## 📋 System Requirements

### **Supported Platforms:**
- ✅ **Windows** (7+)
- ✅ **macOS** (10.5+)
- ✅ **Linux** (with GUI/X Server)

### **Requirements:**
- Python 3.8 or higher
- Physical keyboard connected to the system
- Display/GUI environment (not headless)
- 50MB free disk space

### **Not Supported:**
- ❌ Cloud platforms (Streamlit Cloud, Hugging Face Spaces)
- ❌ Docker containers (headless)
- ❌ SSH sessions without X11 forwarding
- ❌ Virtual machines without proper input devices

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/darpit28/dp_key_logger.git
cd dp_key_logger
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 💻 Usage Guide

### Starting the Logger
1. Open the application in your browser
2. Click the **"▶️ Start"** button in the sidebar
3. Success message confirms logging has begun

### Monitoring Activity
- View real-time keystroke statistics in the main dashboard
- Watch live logs update as you type
- Monitor typing speed and key frequency

### Saving Logs
1. Click **"💾 Save Logs"** button
2. Logs are automatically saved to the `logs/` directory
3. Format: `keylogger_YYYYMMDD_HHMMSS.json`

### Clearing Logs
- Click **"🗑️ Clear Logs"** to remove all captured data
- This action cannot be undone

### Stopping the Logger
1. Click the **"⏹️ Stop"** button
2. Logging will pause immediately
3. Existing logs are preserved

---

## 📁 Project Structure

```
dp_key_logger/
├── app.py                 # Main Streamlit application
├── keylogger.py          # Core keylogger backend
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── logs/                # Directory for saved keystroke logs
    └── keylogger_*.json # Individual session logs
```

---

## 🔧 Configuration

### Dependencies (requirements.txt)
```
streamlit==1.31.0   # Web framework
pynput==1.7.6       # Keyboard input library
pandas==2.2.0       # Data manipulation
```

### Log Directory
Logs are automatically saved to `./logs/` directory with timestamp-based filenames.

---

## 🐛 Troubleshooting

### **Error: "X Server Not Available" (Linux)**
**Problem:** Application fails on headless Linux system
**Solution:** 
- Run on a Linux system with GUI installed
- Or enable X11 forwarding if using SSH: `ssh -X username@host`
- Or install virtual X server: `sudo apt-get install xvfb`

### **Error: "pynput" ImportError**
**Problem:** pynput library not installed
**Solution:**
```bash
pip install --upgrade pynput
```

### **Application Won't Start**
**Problem:** Port 8501 already in use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### **Logging Not Capturing Keys**
**Problem:** No keystrokes being recorded
**Checks:**
- Ensure application window is focused
- Verify "Start" button was clicked (success message should appear)
- Check if running in a virtual machine (may need additional configuration)
- Make sure keyboard is properly connected

### **Permission Denied Errors**
**Problem:** Cannot access logs directory
**Solution:**
```bash
# Windows
icacls logs /grant:r "%username%":F

# Linux/macOS
chmod 755 logs
```

---

## 📊 Log Format

Captured keystrokes are saved as JSON:

```json
{
  "timestamp": "2024-12-24T15:30:07.123456",
  "key": "a",
  "type": "regular",
  "session": "20241224_153007"
}
```

**Types:**
- `regular` - Alphanumeric characters
- `special` - Function keys, Enter, Shift, etc.
- `error` - Capture errors

---

## ⚖️ Legal & Ethical Guidelines

### ✅ **LEGAL USE:**
- Monitor your own computer
- Monitor devices you own
- Parental monitoring on owned devices (check local laws)
- Security research on authorized systems
- Personal usage statistics tracking

### ❌ **ILLEGAL USE:**
- Monitoring others without consent
- Capturing passwords on shared systems
- Workplace monitoring without authorization
- Unauthorized access to devices

**⚠️ CHECK YOUR LOCAL LAWS** - Keylogging regulations vary by jurisdiction. Always ensure you have explicit legal and ethical justification.

---

## 🔐 Privacy & Security

- **No data collection** - All logs stored locally on your machine
- **No cloud uploads** - No external server communication
- **Offline operation** - Works completely offline
- **Local processing** - All data processing happens on your device

---

## 📝 License

This project is for **educational purposes only**. Users are responsible for ensuring their use complies with local laws and regulations.

---

## 👨‍💻 Author

**Darpit** - Educational Project  
GitHub: [@darpit28](https://github.com/darpit28)

---

## 🤝 Contributing

Found a bug? Have a suggestion?
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check troubleshooting section above
- Verify system requirements are met

---

## 🎓 Educational Notes

This project is designed to teach:
- Keyboard event handling in Python
- Real-time data capture and processing
- Streamlit web application development
- File I/O and JSON serialization
- Threading and concurrent programming

---

**Last Updated:** December 24, 2025  
**Python Version:** 3.8+  
**Status:** ✅ Active & Maintained
