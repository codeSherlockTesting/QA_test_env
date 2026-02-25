"""Handler module 134: handler_134."""


def handler_134_handle(event):
    """Handle event for handler_134."""
    return {"handler": "handler_134", "event": event, "handled": True}


def handler_134_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_134", "all"]


class Handler134:
    def __init__(self):
        self.name = "handler_134"

    def process(self, event):
        return handler_134_handle(event)
