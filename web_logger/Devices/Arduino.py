from serial.serialutil import SerialException
from .IDevice import IDevice
import serial
import time
import threading
import io
import logging

class Arduino(IDevice):
    def __init__(self, port, name="Arduino", poll_period=10):
        logging.info("Initialised arduino")
        super().__init__()
        self.name = name
        self.port = port
        self.poll_period = poll_period
        self.dimensions = {"Humidity": -1, "Temperature" : -999, "Presssure" : -1}
        self.units = {"Humidity": '%', "Temperature": '*C', "Pressure": "Pa"}

        initial_con_thread = threading.Thread(target=self.reconnect)
        initial_con_thread.start()
        

    def com(self, msg):
        self.sio.write(str(msg))
        self.sio.flush()
        data = self.sio.readline()
        return str(data).rstrip('\r\n')

    def poll(self, poll_period):
        sleep_time = time.time()
        try:
            while True:
                self.dimensions["Humidity"]  = self.com('h')
                self.dimensions["Temperature"]  = self.com('t')
                self.dimensions["Preassure"] = self.com('p')
                self.log()
                sleep_time+=poll_period
                time.sleep(sleep_time - time.time())
        except SerialException as e:
            logging.error(e)
            self.available = False
            self.reconnect()

    def poll_thread(self, poll_period):
        polling_thread = threading.Thread(target=self.poll, args=(poll_period,))
        polling_thread.daemon = True
        polling_thread.start()
        logging.info("Polling thread started")

    def reconnect(self):
        while True:
            try:
                self.con = serial.Serial(self.port, timeout=1)   
                self.sio = io.TextIOWrapper(io.BufferedRWPair(self.con, self.con))
                break
            except SerialException as e:
                if "[Errno 2] No such file or directory: '/dev/ttyUSB0'" in str(e):
                    self.port = '/dev/ttyUSB1'
                elif "[Errno 2] No such file or directory: '/dev/ttyUSB1'" in str(e):
                    self.port = '/dev/ttyUSB0'
                logging.warning('Unable to connect to arduino\n{0}'.format(e))
                time.sleep(10)
        time.sleep(3)
        logging.info("Arduino reconnected")
        self.available = True
        self.poll_thread(self.poll_period)
        
        
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', filename='example.log', level=logging.DEBUG)
    ard = Arduino('COM4')
    print(ard.get_time_series(3))
    while True:
        time.sleep(1)