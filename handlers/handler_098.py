"""Handler module 98: handler_098."""


def handler_098_handle(event):
    """Handle event for handler_098."""
    return {"handler": "handler_098", "event": event, "handled": True}


def handler_098_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_098", "all"]


class Handler098:
    def __init__(self):
        self.name = "handler_098"

    def process(self, event):
        return handler_098_handle(event)
