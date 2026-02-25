"""Handler module 193: handler_193."""


def handler_193_handle(event):
    """Handle event for handler_193."""
    return {"handler": "handler_193", "event": event, "handled": True}


def handler_193_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_193", "all"]


class Handler193:
    def __init__(self):
        self.name = "handler_193"

    def process(self, event):
        return handler_193_handle(event)
