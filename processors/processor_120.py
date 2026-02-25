"""Processor module 120: processor_120."""


def processor_120_transform(input_data):
    """Transform data for processor_120."""
    return {"processor": "processor_120", "output": input_data}


def processor_120_filter(records, criteria=None):
    """Filter records for processor_120."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_120"]


class Processor120:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_120"

    def run(self, data):
        return processor_120_transform(data)
