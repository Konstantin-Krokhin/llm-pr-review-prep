# PR Title: Add simple in-memory cache for API responses

import time

class SimpleCache:
    def __init__(self, ttl_seconds=60):
        self.store = {}
        self.ttl = ttl_seconds

    def get(self, key):
        if key in self.store:
            value, expiry = self.store[key]
            if expiry > time.time():
                return value
            else:
                del self.store[key]
                return None
        return None

    def put(self, key, value):
        expiry = time.time() + self.ttl
        self.store[key] = (value, expiry)
