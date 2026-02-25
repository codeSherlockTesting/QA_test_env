"""Handler module 129: handler_129."""


def handler_129_handle(event):
    """Handle event for handler_129."""
    return {"handler": "handler_129", "event": event, "handled": True}


def handler_129_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_129", "all"]


class Handler129:
    def __init__(self):
        self.name = "handler_129"

    def process(self, event):
        return handler_129_handle(event)
