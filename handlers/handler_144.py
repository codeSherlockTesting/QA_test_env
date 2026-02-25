"""Handler module 144: handler_144."""


def handler_144_handle(event):
    """Handle event for handler_144."""
    return {"handler": "handler_144", "event": event, "handled": True}


def handler_144_can_handle(event_type):
    """Check if this handler supports the event type."""
    return event_type in ["handler_144", "all"]


class Handler144:
    def __init__(self):
        self.name = "handler_144"

    def process(self, event):
        return handler_144_handle(event)
