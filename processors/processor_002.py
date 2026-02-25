"""Processor module 2: processor_002."""


def processor_002_transform(input_data):
    """Transform data for processor_002."""
    return {"processor": "processor_002", "output": input_data}


def processor_002_filter(records, criteria=None):
    """Filter records for processor_002."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_002"]


class Processor002:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_002"

    def run(self, data):
        return processor_002_transform(data)
