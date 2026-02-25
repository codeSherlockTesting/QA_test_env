"""Handler module 136: handler_136."""


def handler_136_handle(event):
    """Handle event for handler_136."""
    return {"handler": "handler_136", "event": event, "handled": True}


def handler_136_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_136", "all"]


class Handler136:
    def __init__(self):
        self.name = "handler_136"

    def process(self, event):
        return handler_136_handle(event)
