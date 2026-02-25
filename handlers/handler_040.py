"""Handler module 40: handler_040."""


def handler_040_handle(event):
    """Handle event for handler_040."""
    return {"handler": "handler_040", "event": event, "handled": True}


def handler_040_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_040", "all"]


class Handler040:
    def __init__(self):
        self.name = "handler_040"

    def process(self, event):
        return handler_040_handle(event)
