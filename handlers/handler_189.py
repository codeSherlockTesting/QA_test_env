"""Handler module 189: handler_189."""


def handler_189_handle(event):
    """Handle event for handler_189."""
    return {"handler": "handler_189", "event": event, "handled": True}


def handler_189_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_189", "all"]


class Handler189:
    def __init__(self):
        self.name = "handler_189"

    def process(self, event):
        return handler_189_handle(event)
