"""Handler module 200: handler_200."""


def handler_200_handle(event):
    """Handle event for handler_200."""
    return {"handler": "handler_200", "event": event, "handled": True}


def handler_200_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_200", "all"]


class Handler200:
    def __init__(self):
        self.name = "handler_200"

    def process(self, event):
        return handler_200_handle(event)
