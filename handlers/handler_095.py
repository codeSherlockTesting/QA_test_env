"""Handler module 95: handler_095."""


def handler_095_handle(event):
    """Handle event for handler_095."""
    return {"handler": "handler_095", "event": event, "handled": True}


def handler_095_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_095", "all"]


class Handler095:
    def __init__(self):
        self.name = "handler_095"

    def process(self, event):
        return handler_095_handle(event)
