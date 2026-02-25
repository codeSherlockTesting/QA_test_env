"""Handler module 21: handler_021."""


def handler_021_handle(event):
    """Handle event for handler_021."""
    return {"handler": "handler_021", "event": event, "handled": True}


def handler_021_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_021", "all"]


class Handler021:
    def __init__(self):
        self.name = "handler_021"

    def process(self, event):
        return handler_021_handle(event)
