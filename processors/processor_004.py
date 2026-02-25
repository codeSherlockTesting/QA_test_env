"""Processor module 4: processor_004."""


def processor_004_transform(input_data):
    """Transform data for processor_004."""
    return {"processor": "processor_004", "output": input_data}


def processor_004_filter(records, criteria=None):
    """Filter records for processor_004."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_004"]


class Processor004:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_004"

    def run(self, data):
        return processor_004_transform(data)
