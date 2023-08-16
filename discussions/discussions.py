from flask import Flask, request
import redis
import os
import json
from datetime import datetime

app = Flask(__name__)

users = redis.Redis(host = os.environ["USERS"], port=6379, decode_responses=True)
sessions = redis.Redis(host=os.environ["SESSIONS"], port=6381, decode_responses=True)
messages = redis.Redis(host=os.environ["MESSAGES"], port=6380, decode_responses=True, db=0)
pms = redis.Redis(host=os.environ["MESSAGES"], port=6380, decode_responses=True, db=1)

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
    newlist = sorted(mess_list, key=lambda d: d["date"])
    newlist.reverse()
    res = {
        "code" : 0,
        "messages" : newlist
    }
    return json.dumps(res)

@app.route("/messages/pms", methods=["POST"])
def pms_received():
    content = request.json
    uname = content["username"]
    token = content["token"]
    token_check = sessions.hget(uname, "token")
    private_msgs = []
    if str(token) == token_check:
        for key in pms.keys():
            if str(key) != "message_id":
                val = pms.hmget(key, "username", "destination", "date", "message")
                if val[1] == uname : 
                    mess_instance = {
                        "sender" : val[0],
                        "date" : val[2],
                        "message" : val[3]
                    }
                    private_msgs.append(mess_instance)
        sorted_msgs = sorted(private_msgs, key=lambda d: d["date"])
        private_msgs.reverse()
        res = {
            "code" : 0,
            "messages" : private_msgs
        }
        return json.dumps(res) 
    else:
        res = {
            "code" : -1,
            "Message" : "User is not logged in"
        }
        return json.dumps(res)
