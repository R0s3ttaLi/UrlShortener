import json
import hashlib
import pymysql
from datetime import datetime, date, time, timezone, timedelta
from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS

SHORTEN_HASH_LENGTH = 5
URL = "http://3.104.217.148:5000/"

def create_app():
    app = Flask(__name__)
    from . import db
    db.init_app(app)
    
    def generateKey(original_url):
        cursor = db.get_db().cursor(pymysql.cursors.DictCursor)
        m = hashlib.sha256()
        IS_UNIQUE = False
        ret_hash = ""
        query = "SELECT * FROM url WHERE shorten_hash = %s"
        while IS_UNIQUE is False:
            m.update(original_url.encode("UTF-8"))
            ret_hash = m.hexdigest()[:SHORTEN_HASH_LENGTH]
            cursor.execute(query, (ret_hash))
            IS_UNIQUE = cursor.fetchone() is None
        return ret_hash

    @app.route("/shorten", methods = ["POST"])
    def shortenURL():
        cursor = db.get_db().cursor(pymysql.cursors.DictCursor)
        if request.method == "POST":
            input_url = request.json.get("input_url")
            input_hours = request.json.get("input_hours")
            #print(input_url)
            query = "SELECT * FROM url WHERE original_url = %s"
            cursor.execute(query, (input_url))
            db_result = cursor.fetchone()
            if db_result:
                shorten_hash = db_result["shorten_hash"]
                ret = URL + shorten_hash
                #print("return known url")
                return jsonify({"Short_URL" : ret})#, "Expiration Time" : db_result["expiration_time"]})
            short_hash = generateKey(input_url)
            #exp_time = datetime.now() + timedelta(hours = int(input_hours))
            #formatted_time = exp_time.strftime("%Y-%m-%d %H:%M:%S")
            #print("Exp time: ")
            #print(formatted_time)
            #cursor.execute("INSERT INTO url(original_url, shorten_hash, expiration_time) VALUES (%s, %s, %s)", (input_url, short_hash, formatted_time))
            cursor.execute("INSERT INTO url(original_url, shorten_hash) VALUES (%s, %s)", (input_url, short_hash))
            ret = URL + short_hash
            db.get_db().commit()
            return jsonify({"Short_URL" : ret})#, "Expiration Time" : formatted_time})

   
    @app.route("/<shorten_hash>", methods = ["GET"])
    def redirectToLongUrl(shorten_hash):
        cursor = db.get_db().cursor(pymysql.cursors.DictCursor)
        if request.method == "GET":
            query = "SELECT * FROM url WHERE shorten_hash = %s"
            cursor.execute(query, (shorten_hash))
            db_result = cursor.fetchone()
            if db_result is not None:
                return redirect(db_result["original_url"])
            return jsonify({"Error" : "Invalid URL."})



    CORS(app)

    return app

