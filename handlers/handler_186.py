"""Handler module 186: handler_186."""


def handler_186_handle(event):
    """Handle event for handler_186."""
    return {"handler": "handler_186", "event": event, "handled": True}


def handler_186_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_186", "all"]


class Handler186:
    def __init__(self):
        self.name = "handler_186"

    def process(self, event):
        return handler_186_handle(event)
