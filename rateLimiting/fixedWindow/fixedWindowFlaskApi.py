import time;
import threading;
from collections import defaultdict;
from flask import Flask, jsonify, request;

class FixedwindowRateLimiter:
    def __init__(self , limit, windowSize):
        self.limit= limit;
        self.windowSize= windowSize;
        self.lock= threading.Lock();
        self.counters= defaultdict(lambda: {"windowStart":0 , "count": 0});

    def isAllowed(self , userId):
        with self.lock:
            currentTime= int(time.time());
            windowStart= currentTime - (currentTime % self.windowSize);
            userData= self.counters[userId];
            if userData["windowStart"]!= windowStart:
                userData["windowStart"]= windowStart;
                userData["count"]=0;
            if userData["count"]<self.limit:
                userData["count"]+=1;
                return True;
            return False;

app = Flask(__name__);
limiter= FixedwindowRateLimiter(5, 60);

@app.route("/api/health", methods=["GET"])
def protected_endpoint():
    userId= request.headers.get("userId", "anonoymous");
    if not limiter.isAllowed(userId):
        return jsonify({"error" : "rate limit exceeded"}), 429;
    return jsonify({"message":"success"});

if __name__ == "__main__":
    app.run(debug=True)