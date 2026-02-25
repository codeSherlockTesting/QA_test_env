"""Handler module 130: handler_130."""


def handler_130_handle(event):
    """Handle event for handler_130."""
    return {"handler": "handler_130", "event": event, "handled": True}


def handler_130_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_130", "all"]


class Handler130:
    def __init__(self):
        self.name = "handler_130"

    def process(self, event):
        return handler_130_handle(event)
