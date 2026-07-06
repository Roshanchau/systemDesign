import time;
import threading;

class TokenBucket:
    def __init__(self, capacity: int, refillRate: int):
        self.capacity= capacity;
        self.tokens= capacity;
        self.refillRate= refillRate;
        self.lastFilled= time.time();
        self.lock= threading.Lock();

    def _refill(self):
        now=time.time();
        elapsed= now- self.lastFilled;
        refillAmount= elapsed* self.refillRate;
        self.tokens= min(self.capacity, self.tokens+ refillAmount);
        self.lastFilled= now;

    def allowRequests(self, tokens_needed=1):
        with self.lock:
            self._refill();
            if(self.tokens>= tokens_needed):
                self.tokens-=tokens_needed;
                return True;
            return False;

bucket= TokenBucket(10, 2);
for i in range(20):
    if bucket.allowRequests():
        print(f"[{time.strftime('%X')}] Request {i} allowed");
    else:
         print(f"[{time.strftime('%X')}] Request {i} denied");
    time.sleep(0.1);