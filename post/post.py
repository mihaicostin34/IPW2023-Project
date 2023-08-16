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

@app.route("/post", methods=["POST"])
def post_message():
    content = request.json
    msg = content["message"]
    uname = content["username"]
    token = content["token"]
    token_check = sessions.hget(uname, "token")
    print(token)
    print(token_check)
    if str(token) == token_check:
        #token is correct
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        messages.incr("message_id")
        messages.hmset(messages.get("message_id"),
            {
                "username" : uname,
                "date" : dt_string,
                "message" : msg
            }
        )
        res = {
            "code" : 0,
            "message" : "Message successfully uploaded"
        }
        return json.dumps(res)
    else:
        #token is incorrect
        res = {
            "code" : -1,
            "message" : "Incorrect user token!"
        }
        return json.dumps(res)

@app.route("/post/pm", methods=["POST"])
def private_message():
    content = request.json
    uname = content["username"]
    dest = content["destination"]
    msg = content["message"]
    if dest in users.keys():
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        pms.incr("message_id")
        pms.hmset(pms.get("message_id"),
            {
                "username" : uname,
                "destination" : dest,
                "date" : dt_string,
                "message" : msg
            }
        )
        res = {
            "code" : 0,
            "message" : "Message successfully uploaded"
        }
        return json.dumps(res)
    else:
        res = {
            "code" : -1,
            "message" : "This user doesn't exist"
        }
        return json.dumps(res)