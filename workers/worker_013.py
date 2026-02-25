"""Worker module 13: worker_013."""

import asyncio


async def worker_013_run(task_data):
    """Execute worker task for worker_013."""
    await asyncio.sleep(0.01)
    return {"worker": "worker_013", "status": "done", "result": task_data}


async def worker_013_health_check():
    """Health check for worker_013."""
    return {"worker": "worker_013", "healthy": True}


class Worker013:
    def __init__(self):
        self.name = "worker_013"
        self.running = False

    async def start(self):
        self.running = True

    async def stop(self):
        self.running = False
