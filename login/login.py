from flask import Flask, request
import redis
import os
import random 
import json

users = redis.Redis(host=os.environ["USERS"], port=6379, decode_responses=True)
sessions = redis.Redis(host=os.environ["SESSIONS"], port=6381, decode_responses=True)

app = Flask(__name__)

@app.route("/api/signup", methods=['POST'])
def signup():
    content = request.json
    success = users.hsetnx(
        content['username'],
        "password",
        value=content["password"],
    )
    if success == 0:
        res = {
            "code" : -1,
            "message" : "Username already in use. Please try another one"
        }
        return json.dumps(res)
    else:
        users.hmset(
            content['username'],
            {
                "email": content['email'],
                "password": content["password"]
            })
        res = {
            "code" : 0,
            "message" : "Successfully signed up! :D"
        }
        return json.dumps(res)

@app.route("/api/login", methods=['POST'])
def login():
    content = request.json
    uname = content["username"]
    if not users.exists(uname):
        res = {
            "code" : -1,
            "message" : "Username doesn't exist"
        }
        return json.dumps(res)
    else:
        password = users.hmget(uname, "password")
        token = sessions.hget(uname, "token")
        if token != None:
            print(token)
            res = {
                "code" : -1,
                "message" : "User already logged in"
            }
            return json.dumps(res)
        else:
            token = random.randint(10000,90000)
            sessions.hset(uname, "token", token)
            tkn = {
                "code" : 0,
                "message" : token
            }
            return json.dumps(tkn)

@app.route("/api/logout", methods=['POST'])
def logout():
    content = request.json
    token = content["token"]
    uname = content["username"]
    token_match = sessions.hget(uname, "token")
    print(token_match)
    if token_match ==None:
        res = {
            "code" : -1,
            "message" : "User is not logged in"
        }
        return json.dumps(res)
    if str(token) == token_match:
        result = sessions.hdel(uname, "token")
        res = {
            "code" : 0,
            "message" : "Successfully logged out! :D"
        }
        return json.dumps(res)
    else:
        res = {
            "code" : -1,
            "message" : "Wrong token! :("
        }
        return json.dumps(res)
    
@app.route("/api/cleardb", methods=["GET", "POST"])
def clear():
    for key in users.keys():
        users.delete(key)
    return "Everything deleted"