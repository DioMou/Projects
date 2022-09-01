# import os
# from os.path import join
from time import sleep

# from streamparse import Spout
import storm


class FileReaderSpout(storm.Spout):

    def initialize(self, conf, context):
        self._conf = conf
        self._context = context
        self._complete = False

        storm.logInfo("Spout instance starting...")

        # TODO:
        # Task: Initialize the file reader
        # hint: get the filename from conf argument 
        self.f=open(self._conf["filePath"],'r')
        # End

    def nextTuple(self):
        # TODO:
        # Task 1: read the next line and emit a tuple for it
        # Task 2: don't forget to sleep for 1 second when the file is entirely read to prevent a busy-loop
        lines=self.f.readlines()
        for l in lines:
            storm.logInfo("Emiting %s" %l)
            storm.emit([l])
        sleep(1)
        # End


# Start the spout when it's invoked
FileReaderSpout().run()
