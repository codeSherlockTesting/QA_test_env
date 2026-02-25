"""Handler module 135: handler_135."""


def handler_135_handle(event):
    """Handle event for handler_135."""
    return {"handler": "handler_135", "event": event, "handled": True}


def handler_135_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_135", "all"]


class Handler135:
    def __init__(self):
        self.name = "handler_135"

    def process(self, event):
        return handler_135_handle(event)
