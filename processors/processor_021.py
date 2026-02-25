"""Processor module 21: processor_021."""


def processor_021_transform(input_data):
    """Transform data for processor_021."""
    return {"processor": "processor_021", "output": input_data}


def processor_021_filter(records, criteria=None):
    """Filter records for processor_021."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_021"]


class Processor021:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_021"

    def run(self, data):
        return processor_021_transform(data)
