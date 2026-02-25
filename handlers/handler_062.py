"""Handler module 62: handler_062."""


def handler_062_handle(event):
    """Handle event for handler_062."""
    return {"handler": "handler_062", "event": event, "handled": True}


def handler_062_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_062", "all"]


class Handler062:
    def __init__(self):
        self.name = "handler_062"

    def process(self, event):
        return handler_062_handle(event)
