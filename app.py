from flask import Flask, request
import requests as r
import redis
import os
import datetime
import json

redisUrl = os.environ.get('REDISURL')
password, host, port = redisUrl.replace(
    'redis://', '').replace('@', '|').replace(':', '|').split('|')

r = redis.Redis(host=host, password=password, port=port, ssl=True)

app = Flask(__name__)

app.route('/mhyy', methods=['GET'])


def parser():
    client_type = request.args.get('type')
    version = request.args.get('version')
    android = request.args.get('android')
    deviceid = request.args.get('deviceid')
    devicename = request.args.get('devicename')
    devicemodel = request.args.get('devicemodel')
    appid = request.args.get('appid')
    curr_time = datetime.datetime.now()
    timestamp = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
    data = {
        'client_type': client_type,
        'version': version,
        'android': android,
        'deviceid': deviceid,
        'devicename': devicename,
        'devicemodel': devicemodel,
        'appid': appid,
        'submit_time': timestamp
    }
    res = r.get(deviceid)
    if res != None:
        r.set(deviceid, data)
        return json.dumps({"code": 200, "msg": 'OK'})
    else:
        return json.dumps({"code": 200, "msg": "Duplicated"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)