"""Processor module 87: processor_087."""


def processor_087_transform(input_data):
    """Transform data for processor_087."""
    return {"processor": "processor_087", "output": input_data}


def processor_087_filter(records, criteria=None):
    """Filter records for processor_087."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_087"]


class Processor087:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_087"

    def run(self, data):
        return processor_087_transform(data)
