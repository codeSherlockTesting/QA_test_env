"""Handler module 120: handler_120."""


def handler_120_handle(event):
    """Handle event for handler_120."""
    return {"handler": "handler_120", "event": event, "handled": True}


def handler_120_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_120", "all"]


class Handler120:
    def __init__(self):
        self.name = "handler_120"

    def process(self, event):
        return handler_120_handle(event)
