"""Handler module 27: handler_027."""


def handler_027_handle(event):
    """Handle event for handler_027."""
    return {"handler": "handler_027", "event": event, "handled": True}


def handler_027_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_027", "all"]


class Handler027:
    def __init__(self):
        self.name = "handler_027"

    def process(self, event):
        return handler_027_handle(event)
