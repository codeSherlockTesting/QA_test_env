"""Handler module 37: handler_037."""


def handler_037_handle(event):
    """Handle event for handler_037."""
    return {"handler": "handler_037", "event": event, "handled": True}


def handler_037_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_037", "all"]


class Handler037:
    def __init__(self):
        self.name = "handler_037"

    def process(self, event):
        return handler_037_handle(event)
