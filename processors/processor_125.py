"""Processor module 125: processor_125."""


def processor_125_transform(input_data):
    """Transform data for processor_125."""
    return {"processor": "processor_125", "output": input_data}


def processor_125_filter(records, criteria=None):
    """Filter records for processor_125."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_125"]


class Processor125:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_125"

    def run(self, data):
        return processor_125_transform(data)
