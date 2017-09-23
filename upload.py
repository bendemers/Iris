
import time
from picamera import PiCamera
from datetime import datetime
#from azure.storage.file import ContentSettings

camera = PiCamera()

while True:
    camera.capture(filename)
    print("image captured")
    time.sleep(1)
    
