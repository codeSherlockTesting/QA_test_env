"""Handler module 60: handler_060."""


def handler_060_handle(event):
    """Handle event for handler_060."""
    return {"handler": "handler_060", "event": event, "handled": True}


def handler_060_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_060", "all"]


class Handler060:
    def __init__(self):
        self.name = "handler_060"

    def process(self, event):
        return handler_060_handle(event)
