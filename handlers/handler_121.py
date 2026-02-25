"""Handler module 121: handler_121."""


def handler_121_handle(event):
    """Handle event for handler_121."""
    return {"handler": "handler_121", "event": event, "handled": True}


def handler_121_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_121", "all"]


class Handler121:
    def __init__(self):
        self.name = "handler_121"

    def process(self, event):
        return handler_121_handle(event)
