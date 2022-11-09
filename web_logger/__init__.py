from fastapi import FastAPI, Request
from Devices.Arduino import Arduino
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import logging

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
devices = [Arduino('/dev/ttyUSB0')]
logging.info("Added arduino to device list")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html",{"request": request})

@app.get("/Devices")
def ListDevices():
    """Gives a list of all devices and their dimensions"""
    device_dim = {}
    for dev in devices:
        device_dim[dev.name] = dev.get_dimensions()
    return {'Devices': device_dim}

@app.get("/Devices/{device_id}")
def ListDeviceDims(device_id: int):
    """Gives dimensions and current values for device by id (index of devices list)"""
    return devices[device_id].get_current_value()

@app.get("/Devices/{device_id}/units")
def ListDeviceUnits(device_id: int):
    """Gives units for device by id (index of devices list)"""
    return devices[device_id].get_units()

@app.get("/Devices/{device_id}/n={n}")
def TimeSeries(device_id: int, n : int):
    return devices[device_id].get_time_series(n)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', filename='example.log', level=logging.DEBUG)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6969)
