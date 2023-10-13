import os, shutil, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

directory = "D:\Downloads"
os.chdir(directory)

class Watcher:
    DIRECTORY_TO_WATCH = "D:\Downloads"
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
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
        if event.event_type == 'created':
            time.sleep(15)
            for file in os.listdir():
                if os.path.isdir(f'D:\Downloads\{file}'):
                    continue
                else:
                    if file.endswith(('.exe', '.msi')):
                        os.makedirs('Executables', exist_ok=True)
                        shutil.move(f'D:\Downloads\{file}', 'D:\Downloads\Executables')
                    elif file.endswith('.torrent'):
                        os.makedirs('Torrents', exist_ok=True)
                        shutil.move(f'D:\Downloads\{file}', 'D:\Downloads\Torrents')
                    elif file.endswith(('.zip', '.7zip', '.rar')):
                        os.makedirs('Archives', exist_ok=True)
                        shutil.move(f'D:\Downloads\{file}', 'D:\Downloads\Archives')
                    elif file.endswith('.iso'):
                        os.makedirs('OS Images', exist_ok=True)
                        shutil.move(f'D:\Downloads\{file}', 'D:\Downloads\OS Images')

if __name__ == '__main__':
    run = Watcher()
    run.run()