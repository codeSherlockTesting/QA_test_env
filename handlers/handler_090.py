"""Handler module 90: handler_090."""


def handler_090_handle(event):
    """Handle event for handler_090."""
    return {"handler": "handler_090", "event": event, "handled": True}


def handler_090_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_090", "all"]


class Handler090:
    def __init__(self):
        self.name = "handler_090"

    def process(self, event):
        return handler_090_handle(event)
