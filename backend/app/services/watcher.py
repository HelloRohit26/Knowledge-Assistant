from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Timer

from app.core.config import settings
from app.services.incremental_indexer import run_incremental_indexing


class KnowledgeBaseWatcher(FileSystemEventHandler):

    def __init__(self):
        self.timer = None

    def trigger(self):

        if self.timer:
            self.timer.cancel()

        self.timer = Timer(
            2,
            run_incremental_indexing
        )

        self.timer.start()

    def on_created(self, event):

        if not event.is_directory:
            self.trigger()

    def on_modified(self, event):

        if not event.is_directory:
            self.trigger()

    def on_deleted(self, event):

        if not event.is_directory:
            self.trigger()


def start_watcher():

    observer = Observer()

    observer.schedule(
        KnowledgeBaseWatcher(),
        settings.DATA_FOLDER,
        recursive=True
    )

    observer.daemon = True

    observer.start()

    return observer