"""Handler module 177: handler_177."""


def handler_177_handle(event):
    """Handle event for handler_177."""
    return {"handler": "handler_177", "event": event, "handled": True}


def handler_177_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_177", "all"]


class Handler177:
    def __init__(self):
        self.name = "handler_177"

    def process(self, event):
        return handler_177_handle(event)
