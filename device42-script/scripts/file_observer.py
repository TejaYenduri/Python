import time
import ConfigParser
import smtplib
import os
import logging
from email import MIMEText
from email import MIMEMultipart
from Device42APIAccess import Device42Svc
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class NewFileHandler(PatternMatchingEventHandler):
    patterns = ["*.csv"]

    def on_created(self, event):
        self._process(event)

    def _process(self, event):
        try:
            destination_success = os.path.join(os.getcwd(), "success")
            destination_failure = os.path.join(os.getcwd(), "failed")

            if not os.path.exists(destination_success):
                os.makedirs(destination_success)
            if not os.path.exists(destination_failure):
                os.makedirs(destination_failure)
            if self._call_api(event):
                destination = destination_success
            else:
                destination = destination_failure
            timestamp = time.strftime("%Y%m%d%H%M%S")
            file_name = os.path.basename(event.src_path)
            split_name = os.path.splitext(file_name)
            new_file_name = "/" + split_name[0] + timestamp + split_name[1]
            os.rename(event.src_path, destination + new_file_name)
        except (OSError, IOError) as err:
            print err

    def _call_api(self, event):
        file_name = event.src_path
        is_valid = self.validate_file(file_name)
        if is_valid:
            cfg_name = os.path.join(os.pardir, 'credentials.cfg')
            device42 = Device42Svc(cfg_name)
            success = device42.post_devices_csv(file_name)
            device42.logger.info(file_name + " created in the files folder")
            return success
        else:
            return False

    def validate_file(self, file_name):
        try:
            required_headers = {'device', 'building', 'room', 'rack', 'start_at'}
            device_rack_params = {'device', 'rack_id', 'start_at'}
            with open(file_name) as file_handler:
                keys_string = file_handler.readline()
                is_valid = False
                if keys_string:
                    keys_string = keys_string.lower()
                    keys = keys_string.split(',')
                    if 'building' in keys:
                        if all(header in keys for header in required_headers):
                            is_valid = True
                    if 'rack_id' in keys:
                        if all(header in keys for header in device_rack_params):
                            is_valid = True
                    if not is_valid:
                        self.email("Missing required headers")
                        return is_valid
                else:
                    self.email("Missing column headers")
                    return is_valid
            for line in self.read_from_csv(file_handler):
                values = line.split(',')
                if any(map(lambda x: x is None or x == '', values)):
                    self.email("Values are empty or none")
                    return False
        except IOError as err:
            logger.info(err)

    def email(self, message):
        try:
            config = ConfigParser.SafeConfigParser()
            config.read('email_credentials.cfg')
            from_addr = config.get('email', 'FROM_ADDR')
            to_addr = config.get('email', 'TO_ADDR')
            password = config.get('email', 'PASSWORD')
            sub = "Test"
            msg = MIMEMultipart()
            msg['From'] = from_addr
            msg['To'] = to_addr
            msg['Subject'] = sub

            body = message
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_addr, password)
            text = msg.as_string()
            server.sendmail(from_addr, to_addr, text)
            server.quit()
        except ConfigParser.Error as err:
            logger.info(err)

    def read_from_csv(self, file_handler):
        while True:
            data = file_handler.readline()
            if not data:
                break
            yield data


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    log_name = os.path.join(str(time.strftime('%Y%m%d%H%M%S')), '.log')
    handler = logging.FileHandler(log_name)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    event_handler = NewFileHandler()
    observer = Observer()
    path = os.path.join(os.getcwd(), "files")
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
