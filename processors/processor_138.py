"""Processor module 138: processor_138."""


def processor_138_transform(input_data):
    """Transform data for processor_138."""
    return {"processor": "processor_138", "output": input_data}


def processor_138_filter(records, criteria=None):
    """Filter records for processor_138."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_138"]


class Processor138:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_138"

    def run(self, data):
        return processor_138_transform(data)
