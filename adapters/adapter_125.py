"""Adapter module 125: adapter_125."""


class Adapter125:
    """Adapter for adapter_125 integration."""

    def __init__(self, endpoint=None):
        self.endpoint = endpoint or "http://localhost"
        self.name = "adapter_125"

    def connect(self):
        return {"adapter": "adapter_125", "connected": True}

    def fetch(self, query):
        return {"adapter": "adapter_125", "query": query, "results": []}

    def push(self, data):
        return {"adapter": "adapter_125", "pushed": True, "count": len(data) if data else 0}
