"""Handler module 89: handler_089."""


def handler_089_handle(event):
    """Handle event for handler_089."""
    return {"handler": "handler_089", "event": event, "handled": True}


def handler_089_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_089", "all"]


class Handler089:
    def __init__(self):
        self.name = "handler_089"

    def process(self, event):
        return handler_089_handle(event)
