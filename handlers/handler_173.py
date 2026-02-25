"""Handler module 173: handler_173."""


def handler_173_handle(event):
    """Handle event for handler_173."""
    return {"handler": "handler_173", "event": event, "handled": True}


def handler_173_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_173", "all"]


class Handler173:
    def __init__(self):
        self.name = "handler_173"

    def process(self, event):
        return handler_173_handle(event)
