import time;
import threading;

class LeakyBucketAglo:
    def __init__(self, capacity: int, leakRate: float):
        self.capacity= capacity;
        self.leakRate= leakRate; #leak rate in\ req/sec
        self.bucketSize= 0;
        self.lastLeak= time.time();
        self.lock= threading.Lock();

    def leak(self) -> None:
        now= time.time();
        time_elapse= now - self.lastLeak;
        self.bucketSize= max(0, self.bucketSize- time_elapse*self.leakRate);
        self.lastLeak= now;

    def addRequest(self) -> bool:
        with self.lock:  # using locks to make it thread safe
            self.leak();
            if self.bucketSize< self.capacity:
                self.bucketSize+=1;
                return True;
            return False
    
    def getBucketSize(self) -> float:
        with self.lock: #using locks here as well to make it thread safe
            self.leak();  # invoking leak method so that read state is consistent after the time elapsed (even in ms)
            return self.bucketSize;

bucket= LeakyBucketAglo(20, 2);
for i in range(100):
    if bucket.addRequest():
        print(f"Request {i+1} accepted. Bucket size: {bucket.getBucketSize():.2f}");
    else:
         print(f"Request {i+1} discarded. Bucket full.")
    time.sleep(0.3);
