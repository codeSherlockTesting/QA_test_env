"""Handler module 124: handler_124."""


def handler_124_handle(event):
    """Handle event for handler_124."""
    return {"handler": "handler_124", "event": event, "handled": True}


def handler_124_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_124", "all"]


class Handler124:
    def __init__(self):
        self.name = "handler_124"

    def process(self, event):
        return handler_124_handle(event)
