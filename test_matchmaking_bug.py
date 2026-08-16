#!/usr/bin/env python3
"""
Test script to reproduce BUG #1: matchmaking creates room with ['a', 'a']
This script simulates two clients logging in and requesting matchmaking.
"""

import socket
import json
import time
import threading

class TestClient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.socket = None
        self.responses = []
        
    def connect(self, host='localhost', port=5000):
        """Connect to server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketct((host, port))
        print(f"[{self.username}] Connected to server")
        
    def send_message(self, msg_type, data=None):
        """Send message to server"""
        message = {
            "type": msg_type,
            "data": data or {}
        }
        json_msg = json.dumps(message) + "\n"
        self.socket.send(json_msg.encode('utf-8'))
        print(f"[{self.username}] Sent: {msg_type}")
        
    def receive_responses(self):
        """Receive messages from server"""
        buffer = ""
        while True:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if not data:
                    break
                buffer += data
                
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        msg = json.loads(line)
                        self.responses.append(msg)
                        print(f"[{self.username}] Received: {msg.get('type')} - {msg.get('data')}")
            except Exception as e:
                break
                
    def login(self):
        """Login with username and password"""
        self.send_message("login", {
            "username": self.username,
            "password": self.password
        })
        
    def request_match(self):
        """Request matchmaking"""
        self.send_message("match", {})
        
    def close(self):
        """Close connection"""
        if self.socket:
            self.socket.close()

# Main test
if __name__ == "__main__":
    print("\n" + "="*60)
    print("BUG #1 Reproduction Test: Matchmaking Identity Bug")
    print("="*60 + "\n")
    
    # Create two clients
    client1 = TestClient("test", "12")
    client2 = TestClient("a", "5")
    
    try:
        # Connect both clients
        client1.connect()
        client2.connect()
        
        # Start receiver threads
        t1 = threading.Thread(target=client1.receive_responses, daemon=True)
        t2 = threading.Thread(target=client2.receive_responses, daemon=True)
        t1.start()
        t2.start()
        
        # Both clients login
        print("\n--- STEP 1: Both clients login ---")
        client1.login()
        client2.login()
        time.sleep(1)
        
        # Both request matchmaking
        print("\n--- STEP 2: Both clients request matchmaking ---")
        client1.request_match()
        time.sleep(0.5)
        client2.request_match()
        time.sleep(2)
        
        print("\n--- STEP 3: Check server output for 'ROOM PLAYERS' ---")
        print("If bug exists, server should log: ROOM PLAYERS: ['a', 'a']")
        print("If fixed, server should log: ROOM PLAYERS: ['test', 'a']")
        
        time.sleep(2)
        
    finally:
        client1.close()
        client2.close()
        print("\n" + "="*60)
        print("Test completed. Check server output above.")
        print("="*60 + "\n")
