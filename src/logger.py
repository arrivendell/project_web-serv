import sys
import os
import logging
import traceback
from datetime import datetime
from config import CONFIG

config = CONFIG

class CustomLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(config.logger_level)

        self.formatter = logging.Formatter("%(asctime)s - %(levelname)s:: %(message)s")
        self.formatter_out = logging.Formatter("%(asctime)s - %(levelname)s:: %(message)s")

        self.stream = logging.StreamHandler()
        self.stream.setFormatter(self.formatter_out)
        self.stream.setLevel(config.logger_level)
        self.logger.addHandler(self.stream)

    def add_file(self,logname, date = True):
        """
        Creates a log file and binds the logger with the output console and log file
        """
        if date:
            dest_log = "{}.{}.log".format(logname, datetime.strftime(datetime.now(), "%Y-%m-%d_%Hh%Mm%Ss"))
        else:
            dest_log = "{}.log".format(logname)
        dest_dir = os.path.dirname(dest_log)

        if not os.path.exists(dest_dir):
            try:
                os.makedirs(os.path.dirname(dest_log))
            except:
                self.error("failed to add log " + dest_log + " : can't create directory " + dest_dir)
                return

        elif not os.path.isdir(dest_dir):
            self.error("failed to add log " + dest_log + " : " + dest_dir + " is not a directory")
            return

        hdlr = logging.FileHandler(dest_log)
        hdlr.setFormatter(self.formatter)
        hdlr.setLevel(config.logger_level)
        self.logger.addHandler(hdlr)

        return dest_log

    def debug(self, message):
        """
        Write a debug info in the console and the log file
        """
        self.logger.log(logging.DEBUG, message.rstrip("\r\n"))


    def exception(self,e):
        """
        Write an exception stacktrace in the console and the log file
        """
        self.logger.exception(e)
        traceback.print_exc()

    def error(self,message):
        """
        Write an error message in the console and the log file
        """     
        self.logger.log(logging.ERROR, message.rstrip("\r\n"))

    def info(self,message):
        """
        Write an info message in the console and the log file
        """
        self.logger.log(logging.INFO, message.rstrip("\r\n"))

    def warning(self,message):
        """
        Write a warning message in the console and the log file
        """
        self.logger.log(logging.WARNING, message.rstrip("\r\n"))