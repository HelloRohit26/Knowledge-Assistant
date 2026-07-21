"""
Application Metrics Tracker

In-memory thread-safe metrics tracker for API requests,
search operations, and indexing events.
"""

import time
from threading import Lock


class MetricsTracker:
    def __init__(self):
        self._lock = Lock()
        self.request_count = 0
        self.error_count = 0
        self.total_latency_ms = 0.0
        self.search_count = 0
        self.chat_count = 0

    def record_request(self, latency_ms: float, is_error: bool = False):
        with self._lock:
            self.request_count += 1
            self.total_latency_ms += latency_ms
            if is_error:
                self.error_count += 1

    def record_search(self):
        with self._lock:
            self.search_count += 1

    def record_chat(self):
        with self._lock:
            self.chat_count += 1

    def get_summary(self):
        with self._lock:
            avg_latency = (
                self.total_latency_ms / self.request_count
                if self.request_count > 0 else 0.0
            )
            return {
                "total_requests": self.request_count,
                "total_errors": self.error_count,
                "avg_latency_ms": round(avg_latency, 2),
                "total_searches": self.search_count,
                "total_chats": self.chat_count
            }


metrics = MetricsTracker()
