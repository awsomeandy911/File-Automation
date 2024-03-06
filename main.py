from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# fill in below folder to track e.g. Windows: "C:\\Users\\UserName\\Downloads" 
# mine is here just for an example (double \\ to not run into Unicode error)
sourceDirectory = "C:\\Users\\bndy1\\Downloads"
destinationSFX = "C:\\Users\\bndy1\\Music\\SFX"
destinationMusic = "C:\\Users\\bndy1\\Music"
destinationImage = "C:\\Users\\bndy1\\Pictures" 
destinationVideo = "C:\\Users\\bndy1\\Videos"
destinationDocument = "C:\\Users\\bndy1\\Documents"

# all image types
imageExtensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# all video types
videoExtensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# all audio types
audioExtensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# all document types
documentExtensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

# function makes files unique if there are duplicates
def makeUnique(destination, name):
    filename, extension = splitext(name)
    counter = 1
    # if file exists, function adds 1 to make unique
    while exists(f"{destination}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name

# function moves files
def moveFile(destination, entry, name):
    if exists(f"{destination}/{name}"):
        uniqueName = makeUnique(destination, name)
        oldName = join(destination, name)
        newName = join(destination, uniqueName)
        rename(oldName, newName)
    move(entry, destination)

# class handles the moving of files depending on file type
class MoverFileHandler(FileSystemEventHandler):
    def modified(self, event):
        with scandir(sourceDirectory) as entries:
            for entry in entries:
                name = entry.name
                self.checkAudio(entry, name)
                self.checkVideo(entry, name)
                self.checkImage(entry, name)
                self.checkDocument(entry, name)

    # fucntion checks all audio files
    def checkAudio(self, entry, name):  
        for audioExtension in audioExtensions:
            if name.endswith(audioExtension) or name.endswith(audioExtension.upper()):
                # allows for 10MB SFX
                if entry.stat().st_size < 10_000_000 or "SFX" in name:  
                    destination = destinationSFX
                else:
                    destination = destinationMusic
                moveFile(destination, entry, name)
                logging.info(f"Moved audio file: {name}")

    # fucntion checks all video files
    def checkVideo(self, entry, name):  
        for videoExtension in videoExtensions:
            if name.endswith(videoExtension) or name.endswith(videoExtension.upper()):
                moveFile(destinationVideo, entry, name)
                logging.info(f"Moved video file: {name}")

    # fucntion checks all image files
    def checkImage(self, entry, name):  
        for imageExtension in imageExtensions:
            if name.endswith(imageExtension) or name.endswith(imageExtension.upper()):
                moveFile(destinationImage, entry, name)
                logging.info(f"Moved image file: {name}")

    # fucntion checks all document files
    def checkDocument(self, entry, name):  
        for documentExtension in documentExtensions:
            if name.endswith(documentExtension) or name.endswith(documentExtension.upper()):
                moveFile(destinationDocument, entry, name)
                logging.info(f"Moved document file: {name}")

# monitors the current directory recursively for file system changes and logs them to the console (do not change!)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sourceDirectory
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