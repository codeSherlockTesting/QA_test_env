"""Processor module 123: processor_123."""


def processor_123_transform(input_data):
    """Transform data for processor_123."""
    return {"processor": "processor_123", "output": input_data}


def processor_123_filter(records, criteria=None):
    """Filter records for processor_123."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_123"]


class Processor123:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_123"

    def run(self, data):
        return processor_123_transform(data)
