"""Handler module 127: handler_127."""


def handler_127_handle(event):
    """Handle event for handler_127."""
    return {"handler": "handler_127", "event": event, "handled": True}


def handler_127_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_127", "all"]


class Handler127:
    def __init__(self):
        self.name = "handler_127"

    def process(self, event):
        return handler_127_handle(event)
