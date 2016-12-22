from __future__ import print_function  # Python 2/3 compatibility

import ConfigParser
import json
import time

import requests

import dynamo_handler
import gps_coordiantes

# load config file
config = ConfigParser.RawConfigParser()
config.read('config.cfg')
server_token = config.get('uber_api', 'server_token')
uber_url = config.get('uber_api', 'uber_url')

uberx_table = dynamo_handler.get_table("UberSurge")
uberxl_table = dynamo_handler.get_table("UberXLSurge")
uberblack_table = dynamo_handler.get_table("UberBlackSurge")

gps_points = gps_coordiantes.get_gps_list((40.818532, -73.961047), (40.709576, -74.036749), (40.695784, -73.989540),
                                          25, 4)  # Manhattan

while True:
    try:
        for point in gps_points:
            start_latitude = end_latitude = point[0]
            start_longitude = end_longitude = point[1]
            parameters = {
                'server_token': server_token,
                'start_latitude': start_latitude,
                'end_latitude': end_latitude,
                'start_longitude': start_longitude,
                'end_longitude': end_longitude
            }
            response = requests.get(uber_url, params=parameters)
            data = response.json()

            if "prices" in data:
                for price in data["prices"]:
                    item = json.loads('{"Time":"%f","Lat":"%f","Lng":"%f","Low":"%f","High":"%f"}' % (
                        time.time(), start_latitude, start_longitude, price["low_estimate"],
                        price["high_estimate"]))
                    if price["display_name"] == "uberX":
                        dynamo_handler.insert(uberx_table, item)
                    elif price["display_name"] == "uberXL":
                        dynamo_handler.insert(uberxl_table, item)
                    elif price["display_name"] == "uberBLACK" or price["display_name"] == "UberBLACK":
                        dynamo_handler.insert(uberblack_table, item)
            else:
                print(data)
    except Exception as e:
        print(e.message)

    print("Done with " + str(time.localtime(time.time())))
    time.sleep(180)
