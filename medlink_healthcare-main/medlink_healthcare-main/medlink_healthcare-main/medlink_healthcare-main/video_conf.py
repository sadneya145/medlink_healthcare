from vidstream import CameraClient
from vidstream import StreamingServer
import threading 
import time

# Replace phone numbers with your actual phone numbers 192.168.174.1
receiving = StreamingServer('192.168.174.1', 9999) 
sending =CameraClient('192.168.174.1', 9999) 


t1 = threading.Thread(target=receiving.start_server) 
t1.start()

time.sleep(2)

t2 = threading.Thread(target=sending.start_stream) 
t2.start()

while input("") != "STOP":
    continue

receiving.stop_server()
sending.stop_stream()
