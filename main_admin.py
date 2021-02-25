import flask
import pymongo
import hashlib
import os
import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, send_from_directory

app = Flask(
    (__name__ + " Admin"),
    static_folder="static_admin",
    template_folder="templates_admin"
)
app.secret_key = ")(*&^%$%^*()("
app.config["PATH_JS"] = os.path.join(os.getcwd(), "bin", "js")
app.config["PATH_IMAGES"] = os.path.join(os.getcwd(), "bin", "payment")

@app.route("/", methods=["GET","POST"])
def login() :
    if request.method == "POST" :
        connect = connect_to()
        find = connect["hoteldata"]["users_admin"].find_one({
            "username" : request.form["username"],
            "password" : hashlib.md5(request.form["password"].encode("utf-8")).hexdigest()
        })

        if not find is None :
            session["username"] = find["username"]
            session["name"] = find["name"]

            return jsonify({
                "code" : 200,
                "message" : "เข้าสู่ระบบสำเร็จ"
            })
        
        return jsonify({
            "code" : 401,
            "message" : "ชื่อผู้ใช้งาน หรือ รหัสผ่านผิด กรุณาลองใหม่อีกครั้ง"
        })

    return render_template("login.html")

@app.route("/dashboard")
def dashboard() :
    if not "username" in session :
        return redirect("/")

    return render_template("dashboard.html",session=session,chart_resonse=summeryweeken())

@app.route("/payments", methods=["GET","POST"])
def payment() :
    if not "username" in session :
        return redirect("/")

    connect = connect_to()
    if request.method == "POST" :
        if request.form["status"] == "true" :
            update = connect["hoteldata"]["booking"].update_one({
                "bookid" : request.form["uuid"]
            },
            {
                "$set" : {
                    "status" : "SUCCESSPAYMENT",
                    "payment.payment_status" : True
                }
            })

            return jsonify({
                "code" : 200,
                "message" : "ยืนยันสำเร็จ"
            })
        elif request.form["status"] == "false" :
            delete = connect["hoteldata"]["booking"].delete_one({
                "bookid" : request.form["uuid"]
            })

            return jsonify({
                "code" : 200,
                "message" : "ลบข้อมูลสำเร็จ"
            })

    find = connect["hoteldata"]["booking"].aggregate(pipeline=[
        {
            "$match" : {
                "status" : "WAITINGPAYMENT"
            }
        },
        {
            "$project" : {
                "_id" : 0,
                "booking" : "$$ROOT"
            }
        },
        {
            "$lookup": {
                "localField" : "booking.user.username",
                "from" : "users",
                "foreignField" : "username",
                "as" : "users"
            }
        }
    ])


    return render_template("payment.html", dataresponse=find)

@app.route("/js/<path:path>")
def jsfile(path) :
    if not "username" in session :
        return redirect("/")

    return send_from_directory(app.config["PATH_JS"], path)

@app.route("/images/<id>")
def get_slipt(id) :
    if not "username" in session :
        return redirect("/")

    try :
        return send_from_directory(app.config["PATH_IMAGES"], id)
    except :
        return "Not Found"

@app.route("/logout")
def logout() :
    session.clear()
    
    return redirect("/")
def connect_to() :
    conn = pymongo.MongoClient("mongodb://root:123456@127.0.0.1:27017/admin")
    conn.server_info()

    return conn

def summeryweeken() :
    chart_lable = []
    chart_data = []

    connect = connect_to()
    data = connect["hoteldata"]["booking"].aggregate(pipeline=[
        {
            "$match" : {
                "date" : {
                    "$gte" : (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0,minute=0,second=0), 
                    "$lt" : datetime.datetime.now().replace(hour=0,minute=0,second=0)
                }
            }
        },
        {
            "$group" : {
                "_id" : {
                    "$dateToString" : {
                        "date" : "$date",
                        "format" : "%d %m %Y"
                    }
                },
                "total" : {
                    "$sum" : "$payment.payment_ammout"
                }
            }
        }
    ])

    for dataresponse in data :
        chart_lable.append(dataresponse["_id"])
        chart_data.append(dataresponse["total"])

    return {
        "lable" : chart_lable,
        "data" : chart_data
    }
app.run(
    host="127.0.0.1",
    port=8005,
    debug=True
)