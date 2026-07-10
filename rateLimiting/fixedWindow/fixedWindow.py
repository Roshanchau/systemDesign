import time;
import threading;

class FixedwindowAlgo:
    def __init__(self , windowSize: int, maxRequest: int):
        self.maxRequests= maxRequest;
        self.windowSize = windowSize;
        self.requests = 0;
        self.lock= threading.Lock();
        self.lastChanged= time.time();

    def allowRequest(self) -> bool:
        with self.lock:
            now= time.time();
            if now - self.lastChanged >= self.windowSize:
                self.requests=0;
                self.lastChanged=now;
            
            if self.requests < self.maxRequests:
                self.requests+=1;
                return True;
            else:
                return False;

    def totalRequests(self) -> int:
        with self.lock:
            return self.requests;

fixedWindow = FixedwindowAlgo(10, 10);
for i in range(20):
    if fixedWindow.allowRequest():
        print(f"Request {i+1} accepted , total requests: {fixedWindow.totalRequests()}");
    else:
        print(f"request {i+1} disallowed");
    time.sleep(0.8)

        