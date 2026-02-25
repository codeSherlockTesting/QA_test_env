"""Handler module 139: handler_139."""


def handler_139_handle(event):
    """Handle event for handler_139."""
    return {"handler": "handler_139", "event": event, "handled": True}


def handler_139_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_139", "all"]


class Handler139:
    def __init__(self):
        self.name = "handler_139"

    def process(self, event):
        return handler_139_handle(event)
