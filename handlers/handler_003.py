"""Handler module 3: handler_003."""


def handler_003_handle(event):
    """Handle event for handler_003."""
    return {"handler": "handler_003", "event": event, "handled": True}


def handler_003_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_003", "all"]


class Handler003:
    def __init__(self):
        self.name = "handler_003"

    def process(self, event):
        return handler_003_handle(event)
