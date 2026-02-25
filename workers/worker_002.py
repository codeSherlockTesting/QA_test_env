"""Worker module 2: worker_002."""

import asyncio


async def worker_002_run(task_data):
    """Execute worker task for worker_002."""
    await asyncio.sleep(0.01)
    return {"worker": "worker_002", "status": "done", "result": task_data}


async def worker_002_health_check():
    """Health check for worker_002."""
    return {"worker": "worker_002", "healthy": True}


class Worker002:
    def __init__(self):
        self.name = "worker_002"
        self.running = False

    async def start(self):
        self.running = True

    async def stop(self):
        self.running = False
