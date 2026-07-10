import time;
import threading;
from collections import deque;

class SlidingWindowAlgo:
    def __init__(self , windowSize: int, maxRequest: int):
        self.windowSize= windowSize;
        self.maxRequest= maxRequest;
        self.requests= deque();
        self.lock= threading.Lock();

    def isAllowed(self):
        with self.lock:
            now = time.time();
            while self.requests and self.requests[0] <= now- self.windowSize:
                self.requests.popleft();
            if len(self.requests) < self.maxRequest:
                self.requests.append(now);
                return True;
            return False;


slidingWindow= SlidingWindowAlgo(10, 10);
for i in range(20):
    if slidingWindow.isAllowed():
        print(f"[{time.strftime('%X')}] Request {i} allowed");
    else:
         print(f"[{time.strftime('%X')}] Request {i} denied");
    time.sleep(0.8);

        