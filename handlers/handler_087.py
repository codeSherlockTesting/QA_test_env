"""Handler module 87: handler_087."""


def handler_087_handle(event):
    """Handle event for handler_087."""
    return {"handler": "handler_087", "event": event, "handled": True}


def handler_087_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_087", "all"]


class Handler087:
    def __init__(self):
        self.name = "handler_087"

    def process(self, event):
        return handler_087_handle(event)
