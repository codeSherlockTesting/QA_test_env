"""Handler module 111: handler_111."""


def handler_111_handle(event):
    """Handle event for handler_111."""
    return {"handler": "handler_111", "event": event, "handled": True}


def handler_111_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_111", "all"]


class Handler111:
    def __init__(self):
        self.name = "handler_111"

    def process(self, event):
        return handler_111_handle(event)
