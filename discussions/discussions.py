from flask import Flask, request
import redis
import os
import json
from datetime import datetime

app = Flask(__name__)

users = redis.Redis(host = os.environ["USERS"], port=6379, decode_responses=True)
sessions = redis.Redis(host=os.environ["SESSIONS"], port=6381, decode_responses=True)
messages = redis.Redis(host=os.environ["MESSAGES"], port=6380, decode_responses=True)

@app.route("/messages", methods=["GET", "POST"])
def messages_sent():
    mess_list = []
    for key in messages.keys():
        if str(key) != "message_id":
            print(key)
            res = messages.hmget(key, "message", "username", "date")
            mess_instance = {
                "message" : res[0],
                "username" : res[1],
                "date" : res[2]
            } 
            mess_list.append(mess_instance)
    res = {
        "code" : 0,
        "messages" : mess_list
    }
    return json.dumps(res)
