"""Handler module 73: handler_073."""


def handler_073_handle(event):
    """Handle event for handler_073."""
    return {"handler": "handler_073", "event": event, "handled": True}


def handler_073_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_073", "all"]


class Handler073:
    def __init__(self):
        self.name = "handler_073"

    def process(self, event):
        return handler_073_handle(event)
