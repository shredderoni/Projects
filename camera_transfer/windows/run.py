import os, shutil, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


raw_formats = [".3fr", ".ari", ".arw", ".srf", ".sr2", ".bay", ".braw", ".cri", ".crw", ".cr2", ".cr3", ".cap", ".iiq", ".eip", \
               ".dcs", ".dcr", ".drf", ".k25", ".kdc", ".dng", ".erf", ".fff", ".gpr", ".jxs", ".mef", ".mdc", ".mos", ".mrw", \
                ".nef", ".nrw", "orf", ".pef", ".ptx", ".pxn", ".R3D", ".raf", ".raw", ".rw2", ".rwl", ".rwz", ".srw", ".tco", ".x3f"]
raw_formats += [word.upper() for word in raw_formats]
raw_formats = tuple(raw_formats)
image_formats = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
image_formats += [word.upper() for word in image_formats]
image_formats = tuple(image_formats)


home_dir = os.path.expanduser('~')
camera_folder = f"{home_dir}\\Pictures\\Camera"
isExist = os.path.exists(camera_folder)
if not isExist:
    os.makedirs(camera_folder)
    os.chdir(camera_folder)
else:
    os.chdir(camera_folder)


def create_dirs(file):
    os.makedirs(f"{file}\\edited", exist_ok=True)
    os.makedirs(f"{file}\\pictures", exist_ok=True)
    os.makedirs(f"{file}\\raw", exist_ok=True)

class Watcher:
    DIRECTORY_TO_WATCH = f"{camera_folder}"
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.event_type == "created":
            os.makedirs("raw", exist_ok=True)
            os.makedirs("pictures", exist_ok=True)
            os.makedirs("edited", exist_ok=True)
            time.sleep(900)
            for file in os.listdir():
                try:
                    source = f'{camera_folder}\\{file}'
                    if file.endswith(image_formats):
                        destination = f'{camera_folder}\\pictures'
                        shutil.move(source, destination)
                        print(f"{file} has been moved to {destination}")
                    elif file.endswith(raw_formats):
                        destination = f'{camera_folder}\\raw'
                        shutil.move(source, destination)
                        print(f"{file} has been moved to {destination}")
                except OSError:
                    print("Something went wrong.")
            time.sleep(30)
        elif event.is_directory:
            time.sleep(900)
            for item in os.listdir():
                if os.path.isfile(item):
                    continue
                elif item == "pictures" or item == "raw" or item == "edited":
                    continue
                else:
                    create_dirs(item)
                    for document in os.listdir(item):
                        try:
                            source = f'{camera_folder}\\{item}\\{document}'
                            if document.endswith(image_formats):
                                destination = f'{camera_folder}\\{item}\\pictures'
                                shutil.move(source, destination)
                                print(f"{document} has been moved to {destination}")
                            elif document.endswith(raw_formats):
                                destination = f'{camera_folder}\\{item}\\raw'
                                shutil.move(source, destination)
                                print(f"{document} has been moved to {destination}")
                        except OSError:
                            print("Something went wrong.")

if __name__ == "__main__":
    w = Watcher()
    w.run()
