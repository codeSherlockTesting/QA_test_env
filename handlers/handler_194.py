"""Handler module 194: handler_194."""


def handler_194_handle(event):
    """Handle event for handler_194."""
    return {"handler": "handler_194", "event": event, "handled": True}


def handler_194_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_194", "all"]


class Handler194:
    def __init__(self):
        self.name = "handler_194"

    def process(self, event):
        return handler_194_handle(event)
