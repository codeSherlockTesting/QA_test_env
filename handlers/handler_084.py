"""Handler module 84: handler_084."""


def handler_084_handle(event):
    """Handle event for handler_084."""
    return {"handler": "handler_084", "event": event, "handled": True}


def handler_084_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_084", "all"]


class Handler084:
    def __init__(self):
        self.name = "handler_084"

    def process(self, event):
        return handler_084_handle(event)
