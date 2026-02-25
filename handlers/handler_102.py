"""Handler module 102: handler_102."""


def handler_102_handle(event):
    """Handle event for handler_102."""
    return {"handler": "handler_102", "event": event, "handled": True}


def handler_102_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_102", "all"]


class Handler102:
    def __init__(self):
        self.name = "handler_102"

    def process(self, event):
        return handler_102_handle(event)
