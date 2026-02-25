"""Handler module 146: handler_146."""


def handler_146_handle(event):
    """Handle event for handler_146."""
    return {"handler": "handler_146", "event": event, "handled": True}


def handler_146_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_146", "all"]


class Handler146:
    def __init__(self):
        self.name = "handler_146"

    def process(self, event):
        return handler_146_handle(event)
