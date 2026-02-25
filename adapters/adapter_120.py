"""Adapter module 120: adapter_120."""


class Adapter120:
    """Adapter for adapter_120 integration."""

    def __init__(self, endpoint=None):
        self.endpoint = endpoint or "http://localhost"
        self.name = "adapter_120"

    def connect(self):
        return {"adapter": "adapter_120", "connected": True}

    def fetch(self, query):
        return {"adapter": "adapter_120", "query": query, "results": []}

    def push(self, data):
        return {"adapter": "adapter_120", "pushed": True, "count": len(data) if data else 0}
