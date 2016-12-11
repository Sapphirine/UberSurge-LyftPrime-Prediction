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
client_id = config.get('lyft_api', 'client_id')
client_secret = config.get('lyft_api', 'client_secret')
lyft_oauth_url = config.get('lyft_api', 'lyft_oauth_url')
lyft_url = config.get('lyft_api', 'lyft_url')

table_name = "LyftPrime"
lyft_table = dynamo_handler.get_table("LyftPrime")
plus_table = dynamo_handler.get_table("LyftPlusPrime")
premier_table = dynamo_handler.get_table("LyftPremierPrime")

gps_points = gps_coordiantes.get_gps_list((40.818532, -73.961047), (40.709576, -74.036749), (40.695784, -73.989540),
                                          25, 4)  # Manhattan

while True:
    try:
        oauth_para = {"grant_type": "client_credentials", "scope": "public"}
        oauth_user = str(client_id) + ":" + str(client_secret)
        oauth_response = requests.post(lyft_oauth_url, data=oauth_para, auth=(client_id, client_secret))
        bearer_token = json.loads(oauth_response.content)["access_token"]

        for point in gps_points:
            start_latitude = end_latitude = point[0]
            start_longitude = end_longitude = point[1]
            headers = {'Authorization': 'bearer ' + bearer_token}
            parameters = {
                'start_lat': start_latitude,
                'start_lng': start_longitude,
                'end_lat': end_latitude,
                'end_lng': end_longitude,
                # 'ride_type': 'lyft'
            }
            response = requests.get(lyft_url, headers=headers, params=parameters)
            data = response.json()

            if "cost_estimates" in data:
                for cost in data["cost_estimates"]:
                    item = json.loads('{"Time":"%f","Lat":"%f","Lng":"%f","Low":"%f","High":"%f","Prime":%s}' % (
                        time.time(), start_latitude, start_longitude, cost["estimated_cost_cents_min"],
                        cost["estimated_cost_cents_max"], cost["primetime_percentage"].split("%")[0]))
                    if cost["ride_type"] == "lyft":
                        dynamo_handler.insert(lyft_table, item)
                    elif cost["ride_type"] == "lyft_plus":
                        dynamo_handler.insert(plus_table, item)
            else:
                print(data)
    except Exception as e:
        print (e.message)

    print("Done with " + str(time.localtime(time.time())))
    # time.sleep(180)
