import os
import sys
import time
import logging
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# duplicate backslashes so program doesn't run into Unicode error
sourceDir = "C:\\Users\\bndy1\\Downloads"
musicDir = "C:\\Users\\bndy1\\Music" 
imageDir = "C:\\Users\\bndy1\\Pictures"
videoDir = "C:\\Users\\bndy1\\Videos"

def move(destination, event, name):
    # needs work
    fileExists = os.scandir

# class that handles the moving of files
class MoveFileHandler(FileSystemEventHandler):
    def modified(self, event):
        with os.scandir(sourceDir) as entries:
            for entry in entries:
                name = entry.name
                destination = sourceDir
                if name.endswith('.mp3'):
                    destination = musicDir
                    # needs move function
                elif name.endswith('.mp4') or name.endswith('.mov'):
                    destination = videoDir
                    # move function
                elif name.endswith('.png') or name.endswith('.jpeg') or name.endswith('.jpg'):
                    destination = imageDir
                    # move function
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