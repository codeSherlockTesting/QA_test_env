"""Handler module 112: handler_112."""


def handler_112_handle(event):
    """Handle event for handler_112."""
    return {"handler": "handler_112", "event": event, "handled": True}


def handler_112_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_112", "all"]


class Handler112:
    def __init__(self):
        self.name = "handler_112"

    def process(self, event):
        return handler_112_handle(event)
