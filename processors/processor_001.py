"""Processor module 1: processor_001."""


def processor_001_transform(input_data):
    """Transform data for processor_001."""
    return {"processor": "processor_001", "output": input_data}


def processor_001_filter(records, criteria=None):
    """Filter records for processor_001."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_001"]


class Processor001:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_001"

    def run(self, data):
        return processor_001_transform(data)
