#!/usr/bin/env python3

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


import os
import time
import datetime
import logging

class FileHandler(FileSystemEventHandler):
  def on_created(self, event):
    try:
      now = datetime.datetime.now()
      idealDiff = datetime.timedelta(30)
      for filename in os.listdir(screenshotLocation):
        fileDateCtime = time.ctime(os.path.getatime(screenshotLocation+filename))
        fileDate = datetime.datetime.strptime(fileDateCtime, "%a %b %d %H:%M:%S %Y")
        diff = now - fileDate
        if(diff > idealDiff):
          os.remove(screenshotLocation+filename)
    except Exception:
      logging.error("Error: "+Exception+" at "+now)
screenshotLocation = os.path.expanduser("~/Pictures/")
logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='')
eventHandler = FileHandler()
observer = Observer()
observer.schedule(eventHandler, screenshotLocation, recursive=True)
observer.start()

try:
  while True:
    time.sleep(10)
except KeyboardInterrupt:
  observer.stop()
observer.join()
