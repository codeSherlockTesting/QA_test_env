"""Handler module 5: handler_005."""


def handler_005_handle(event):
    """Handle event for handler_005."""
    return {"handler": "handler_005", "event": event, "handled": True}


def handler_005_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_005", "all"]


class Handler005:
    def __init__(self):
        self.name = "handler_005"

    def process(self, event):
        return handler_005_handle(event)
