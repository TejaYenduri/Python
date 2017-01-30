import time
import os
import shutil
import datetime
from Device42APIAccess import Device42Svc
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class NewFileHandler(PatternMatchingEventHandler):
    patterns = ["*.csv"]

    def on_created(self, event):
        self._process(event)

    def _process(self, event):
        destination_success = os.getcwd() + "/success"
        destination_failure = os.getcwd() + "/failure"
        if not os.path.exists(destination_success):
            os.makedirs(destination_success)
        if not os.path.exists(destination_failure):
            os.makedirs(destination_failure)
        if self._call_api(event):
            destination = destination_success
        else:
            destination = destination_failure
        timestamp = str(datetime.datetime.now())
        file_name = os.path.basename(event.src_path)
        split_name = os.path.splitext(file_name)
        new_file_name = "/" + split_name[0] + timestamp + split_name[1]
        os.rename(event.src_path, destination + new_file_name)
        # shutil.move(event.src_path, destination)

    def _call_api(self, event):
        file_name = event.src_path
        device42 = Device42Svc('../credentials.cfg')
        success = device42.post_devices_csv(file_name)
        device42.logger.info(file_name + " created in the files folder")
        return success


if __name__ == "__main__":
    event_handler = NewFileHandler()
    observer = Observer()
    path = os.getcwd() + "/files"
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
