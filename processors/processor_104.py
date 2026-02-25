"""Processor module 104: processor_104."""


def processor_104_transform(input_data):
    """Transform data for processor_104."""
    return {"processor": "processor_104", "output": input_data}


def processor_104_filter(records, criteria=None):
    """Filter records for processor_104."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_104"]


class Processor104:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_104"

    def run(self, data):
        return processor_104_transform(data)
