import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

# duplicate backslashes so program doesn't run into Unicode error
sourceDir = "C:\\Users\\bndy1\\Downloads"
musicDir = "C:\\Users\\bndy1\\Music" 
imageDir = "C:\\Users\\bndy1\\Pictures"
videoDir = "C:\\Users\\bndy1\\Videos"

class MoveFileHandler(FileSystemEventHandler):
    def modified(self, event):
        with os.scandir(sourceDir) as entries:
            for entry in entries:
                name = entry.name
                destination = sourceDir
                print(entry.name)

# monitors the current directory recursively for file system changes and logs them to the console
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sourceDir
    event_handler = MoveFileHandlerr()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()