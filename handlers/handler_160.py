"""Handler module 160: handler_160."""


def handler_160_handle(event):
    """Handle event for handler_160."""
    return {"handler": "handler_160", "event": event, "handled": True}


def handler_160_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_160", "all"]


class Handler160:
    def __init__(self):
        self.name = "handler_160"

    def process(self, event):
        return handler_160_handle(event)
