from flask import Flask, jsonify, Response, url_for, send_from_directory, render_template, Markup, make_response, request, Blueprint
from flask_restful import Api, Resource, reqparse
from .Devices.Arduino import Arduino

app = Flask(__name__)
api = Api(app)

devices = [Arduino('COM4')]

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

class TimeSeries(Resource):
    def get(self, id, n):
        return devices[id].get_time_series(n)


api.add_resource(DeviceList, '/Devices')
api.add_resource(DeviceDims, '/Devices/<int:id>')
api.add_resource(TimeSeries, '/Devices/<int:id>/n=<int:n>')

if __name__ == "__main__":
    app.run()