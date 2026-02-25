"""Handler module 122: handler_122."""


def handler_122_handle(event):
    """Handle event for handler_122."""
    return {"handler": "handler_122", "event": event, "handled": True}


def handler_122_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_122", "all"]


class Handler122:
    def __init__(self):
        self.name = "handler_122"

    def process(self, event):
        return handler_122_handle(event)
