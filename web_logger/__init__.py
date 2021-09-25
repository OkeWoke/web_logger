from flask import Flask, jsonify, Response, url_for, send_from_directory, render_template, Markup, make_response, request, Blueprint
from flask_restful import Api, Resource, reqparse
from .Devices.Arduino import Arduino
import logging
import asyncio
app = Flask(__name__)
api = Api(app)
logging.basicConfig(format='%(asctime)s %(message)s', filename='stats.okewoke.com.log', level=logging.DEBUG)
devices = []
logging.info("Added arduino to device list")

@app.route("/")
def home():
    return render_template("home.html")

class DeviceList(Resource):    
    def get(self):
        """Gives a list of all devices and their dimensions"""
        device_dim = {}
        for dev in devices:
            device_dim[dev.name] = dev.get_dimensions()
        return {'Devices': device_dim}

class DeviceDims(Resource):
    def get(self, id):
        """Gives dimensions and current values for device by id (index of devices list)"""
        return devices[id].get_current_value()

class DeviceUnits(Resource):
    def get(self, id):
        return devices[id].get_units()

class TimeSeries(Resource):
    def get(self, id, n):
        return devices[id].get_time_series(n)


api.add_resource(DeviceList, '/Devices')
api.add_resource(DeviceDims, '/Devices/<int:id>')
api.add_resource(DeviceUnits, '/Devices/<int:id>/units')
api.add_resource(TimeSeries, '/Devices/<int:id>/n=<int:n>')

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', filename='example.log', level=logging.DEBUG)
    app.run()