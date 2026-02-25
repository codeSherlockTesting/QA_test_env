"""Handler module 172: handler_172."""


def handler_172_handle(event):
    """Handle event for handler_172."""
    return {"handler": "handler_172", "event": event, "handled": True}


def handler_172_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_172", "all"]


class Handler172:
    def __init__(self):
        self.name = "handler_172"

    def process(self, event):
        return handler_172_handle(event)
