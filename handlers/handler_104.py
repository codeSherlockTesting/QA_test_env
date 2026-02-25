"""Handler module 104: handler_104."""


def handler_104_handle(event):
    """Handle event for handler_104."""
    return {"handler": "handler_104", "event": event, "handled": True}


def handler_104_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_104", "all"]


class Handler104:
    def __init__(self):
        self.name = "handler_104"

    def process(self, event):
        return handler_104_handle(event)
