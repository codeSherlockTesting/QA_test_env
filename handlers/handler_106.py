"""Handler module 106: handler_106."""


def handler_106_handle(event):
    """Handle event for handler_106."""
    return {"handler": "handler_106", "event": event, "handled": True}


def handler_106_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_106", "all"]


class Handler106:
    def __init__(self):
        self.name = "handler_106"

    def process(self, event):
        return handler_106_handle(event)
