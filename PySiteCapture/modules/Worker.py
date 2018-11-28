"""
Description:
    Sub module of PySiteCapture used to create workers to execute jobs.

Usage:
    This should not be called outside of the main entry point, unless you know what you're doing.
"""

class Worker:
    def __init__(self, worker_id, job):
        self.id = worker_id
        self.active_job = job

    def start_job(self, page):
        page.