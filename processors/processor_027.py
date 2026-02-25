"""Processor module 27: processor_027."""


def processor_027_transform(input_data):
    """Transform data for processor_027."""
    return {"processor": "processor_027", "output": input_data}


def processor_027_filter(records, criteria=None):
    """Filter records for processor_027."""
    if not criteria:
        return records
    return [r for r in records if r.get("type") == "processor_027"]


class Processor027:
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.name = "processor_027"

    def run(self, data):
        return processor_027_transform(data)
