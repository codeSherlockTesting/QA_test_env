"""Handler module 196: handler_196."""


def handler_196_handle(event):
    """Handle event for handler_196."""
    return {"handler": "handler_196", "event": event, "handled": True}


def handler_196_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_196", "all"]


class Handler196:
    def __init__(self):
        self.name = "handler_196"

    def process(self, event):
        return handler_196_handle(event)
