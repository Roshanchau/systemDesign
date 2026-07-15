# Sliding Window Algorithm (Rate Limiting)

## Overview
The **Sliding Window Algorithm** is a rate-limiting technique that limits the number of requests allowed during a continuously moving time window. Unlike the Fixed Window algorithm, it does not reset counters at fixed intervals, making it much fairer and reducing sudden traffic spikes at window boundaries.

This algorithm is commonly used in API gateways, authentication services, web servers, and distributed systems where smoother request limiting is required.

---

## How It Works

Instead of counting requests inside fixed intervals, the Sliding Window algorithm stores the timestamp of every accepted request.

For each incoming request:

- Remove timestamps that are older than the configured window.
- Count the remaining timestamps.
- If the number of requests is below the limit, accept the request and store its timestamp.
- Otherwise, reject the request.

---

## Key Parameters

- **Window Size (W):** Time period over which requests are counted.
- **Maximum Requests (N):** Maximum requests allowed within the window.
- **Request Queue:** Stores timestamps of accepted requests.

---

## Algorithm Steps

1. Create an empty queue.
2. For every request:
   - Get the current timestamp.
   - Remove timestamps older than `(current_time - window_size)`.
   - If queue size is less than the maximum allowed requests:
     - Add the current timestamp.
     - Allow the request.
   - Otherwise:
     - Reject the request.

---

## Simple Example

- Window Size = 10 seconds
- Maximum Requests = 10

At time 0:
- Queue is empty.

As requests arrive:
- Every accepted request timestamp is stored.

When a new request arrives:
- Any timestamp older than 10 seconds is removed.
- If fewer than 10 timestamps remain, the request is accepted.
- Otherwise, it is denied until older requests expire.

---

## Thread Safety

The provided implementation uses:

```python
self.lock = threading.Lock()
```

and wraps the complete rate-limiting logic inside:

```python
with self.lock:
```

This ensures only one thread can modify the shared request queue at a time.

### Why is a lock necessary?

The `requests` deque is shared by every thread.

Without synchronization, two threads could:

- Remove expired timestamps simultaneously.
- Read the queue size at the same time.
- Both believe another request is allowed.
- Append timestamps concurrently.

This race condition could allow more requests than the configured limit.

### Why are both reading and writing protected?

Although checking the queue size appears to be a read operation, it depends on first removing expired timestamps:

```python
while self.requests and self.requests[0] <= now - self.windowSize:
    self.requests.popleft()
```

The cleanup modifies the queue before its length is checked. Since cleanup, length checking, and appending together form one atomic decision, the entire sequence must be protected by the same lock.

This guarantees:

- Accurate request counting
- No race conditions
- Correct enforcement of the configured limit

---

## Time Complexity

- Removing expired requests: **O(k)**, where **k** is the number of expired timestamps.
- Allow/Deny decision: **O(1)**
- Overall: approximately **O(k)** per request.

---

## Space Complexity

The queue stores at most **Maximum Requests** timestamps.

**Space Complexity:** **O(N)**

---

## Advantages (Pros)

- Fairer than Fixed Window
- Eliminates boundary burst problems
- Simple implementation using a queue
- Accurate rate limiting
- Suitable for APIs and distributed systems

---

## Disadvantages (Cons)

- Stores timestamps for every accepted request
- Slightly higher memory usage
- Cleanup introduces small processing overhead
- Distributed implementations require synchronization across servers

---

## Real-World Usage

The Sliding Window algorithm is commonly used in:

- API Gateways
- Authentication and login services
- Cloud platforms
- Reverse proxies
- Microservices
- Public REST APIs

It is preferred when smoother and fairer rate limiting is required.

---

## System Design Diagram

![Sliding Window System Design](./slidingWindow.png)

---

## Resources

- https://www.geeksforgeeks.org/system-design/rate-limiting-algorithms-system-design/
- https://mjmichael.medium.com/the-sliding-window-counter-algorithm-a-dive-with-python-and-golang-implementations-d2139340b569
