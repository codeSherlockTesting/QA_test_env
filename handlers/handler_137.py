"""Handler module 137: handler_137."""


def handler_137_handle(event):
    """Handle event for handler_137."""
    return {"handler": "handler_137", "event": event, "handled": True}


def handler_137_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_137", "all"]


class Handler137:
    def __init__(self):
        self.name = "handler_137"

    def process(self, event):
        return handler_137_handle(event)
