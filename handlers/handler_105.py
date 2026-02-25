"""Handler module 105: handler_105."""


def handler_105_handle(event):
    """Handle event for handler_105."""
    return {"handler": "handler_105", "event": event, "handled": True}


def handler_105_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_105", "all"]


class Handler105:
    def __init__(self):
        self.name = "handler_105"

    def process(self, event):
        return handler_105_handle(event)
