"""Handler module 125: handler_125."""


def handler_125_handle(event):
    """Handle event for handler_125."""
    return {"handler": "handler_125", "event": event, "handled": True}


def handler_125_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_125", "all"]


class Handler125:
    def __init__(self):
        self.name = "handler_125"

    def process(self, event):
        return handler_125_handle(event)
