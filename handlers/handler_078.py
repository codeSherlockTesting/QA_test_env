"""Handler module 78: handler_078."""


def handler_078_handle(event):
    """Handle event for handler_078."""
    return {"handler": "handler_078", "event": event, "handled": True}


def handler_078_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_078", "all"]


class Handler078:
    def __init__(self):
        self.name = "handler_078"

    def process(self, event):
        return handler_078_handle(event)
