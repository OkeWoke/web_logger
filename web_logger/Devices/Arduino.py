from .IDevice import IDevice
import serial
import time
import threading
import io

class Arduino(IDevice):
    def __init__(self, port, name="Arduino", poll_period=10):
        super().__init__()
        self.name = name
        self.con = serial.Serial(port, timeout=1)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.con, self.con))
        time.sleep(3)
        self.dimensions = {"Humidity": -1, "Temperature" : -999}
        polling_thread = threading.Thread(target=self.poll, args=(poll_period,))
        polling_thread.daemon = True
        polling_thread.start()

    def com(self, msg):
        self.sio.write(str(msg))
        self.sio.flush()
        data = self.sio.readline()
        return str(data).rstrip('\r\n')

    def poll(self, poll_period):
        sleep_time = time.time()
        while True:
            self.dimensions["Humidity"]  = self.com('h')
            self.dimensions["Temperature"]  = self.com('t')
            self.log()
            sleep_time+=poll_period
            time.sleep(sleep_time - time.time())


if __name__ == "__main__":
    ard = Arduino('COM4')
    print(ard.get_time_series(3))
