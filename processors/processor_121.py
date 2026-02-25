"""Processor module 121: processor_121."""


def processor_121_transform(input_data):
    """Transform data for processor_121."""
    return {"processor": "processor_121", "output": input_data}


def processor_121_filter(records, criteria=None):
    """Filter records for processor_121."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_121"]


class Processor121:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_121"

    def run(self, data):
        return processor_121_transform(data)
