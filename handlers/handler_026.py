"""Handler module 26: handler_026."""


def handler_026_handle(event):
    """Handle event for handler_026."""
    return {"handler": "handler_026", "event": event, "handled": True}


def handler_026_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_026", "all"]


class Handler026:
    def __init__(self):
        self.name = "handler_026"

    def process(self, event):
        return handler_026_handle(event)
