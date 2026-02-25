"""Handler module 36: handler_036."""


def handler_036_handle(event):
    """Handle event for handler_036."""
    return {"handler": "handler_036", "event": event, "handled": True}


def handler_036_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_036", "all"]


class Handler036:
    def __init__(self):
        self.name = "handler_036"

    def process(self, event):
        return handler_036_handle(event)
