"""Handler module 93: handler_093."""


def handler_093_handle(event):
    """Handle event for handler_093."""
    return {"handler": "handler_093", "event": event, "handled": True}


def handler_093_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_093", "all"]


class Handler093:
    def __init__(self):
        self.name = "handler_093"

    def process(self, event):
        return handler_093_handle(event)
