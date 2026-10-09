# initialize a doubly linked list node
class Node:
    def __init__(self , k , v):
        self.key , self.value = k , v;
        self.prev = self.next = None;

# LRU cache class
class LRUcache:
    def __init__(self , capacity):
        self.cap = capacity;
        # hashtable dist
        self.cache = {};
        self.left , self.right = Node(0,0) , Node(0,0);
        self.left.next , self.right.prev = self.right , self.left;

    # insert in the doubly linked list at the MRU pos
    def insert(self, node):
        prev , next = self.right.prev, self.right;
        prev.next = next.prev = node;
        node.next , node.prev = next , prev;

    # remove from the doubly linked list at the LRU pos
    def remove(self , node):
        prev , next = node.prev , node.next;
        prev.next , next.prev = next , prev;

    # read from the cache
    def get(self , key: int) -> int:
        if key in self.cache:
            self.remove(self.cache[key]);
            self.insert(self.cache[key]);
            print("cache hit");
            return self.cache[key].value;
        return "cache miss";

    # write/update the cache
    def put(self , key: int , value:int):
        if key in self.cache:
            self.remove(self.cache[key]);
        self.cache[key] = Node(key , value);
        self.insert(self.cache[key]);

        if len(self.cache) > self.cap:
            lru = self.left.next;
            print("evicted" , lru.key);
            self.remove(lru);
            del self.cache[lru.key];



lru = LRUcache(3)

lru.put(1, 100)
lru.put(2, 200)
lru.put(3, 300)

print(lru.get(1))

lru.put(4, 400)

print(lru.get(2))
print(lru.get(3))
print(lru.get(1))
print(lru.get(4))