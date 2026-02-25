"""Handler module 174: handler_174."""


def handler_174_handle(event):
    """Handle event for handler_174."""
    return {"handler": "handler_174", "event": event, "handled": True}


def handler_174_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_174", "all"]


class Handler174:
    def __init__(self):
        self.name = "handler_174"

    def process(self, event):
        return handler_174_handle(event)
