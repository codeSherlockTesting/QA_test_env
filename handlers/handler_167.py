"""Handler module 167: handler_167."""


def handler_167_handle(event):
    """Handle event for handler_167."""
    return {"handler": "handler_167", "event": event, "handled": True}


def handler_167_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_167", "all"]


class Handler167:
    def __init__(self):
        self.name = "handler_167"

    def process(self, event):
        return handler_167_handle(event)
