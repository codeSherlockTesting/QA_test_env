"""Handler module 20: handler_020."""


def handler_020_handle(event):
    """Handle event for handler_020."""
    return {"handler": "handler_020", "event": event, "handled": True}


def handler_020_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_020", "all"]


class Handler020:
    def __init__(self):
        self.name = "handler_020"

    def process(self, event):
        return handler_020_handle(event)
