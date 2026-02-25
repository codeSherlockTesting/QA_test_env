"""Handler module 91: handler_091."""


def handler_091_handle(event):
    """Handle event for handler_091."""
    return {"handler": "handler_091", "event": event, "handled": True}


def handler_091_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_091", "all"]


class Handler091:
    def __init__(self):
        self.name = "handler_091"

    def process(self, event):
        return handler_091_handle(event)
