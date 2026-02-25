"""Processor module 36: processor_036."""


def processor_036_transform(input_data):
    """Transform data for processor_036."""
    return {"processor": "processor_036", "output": input_data}


def processor_036_filter(records, criteria=None):
    """Filter records for processor_036."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_036"]


class Processor036:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_036"

    def run(self, data):
        return processor_036_transform(data)
