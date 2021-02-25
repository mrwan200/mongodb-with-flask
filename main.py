import flask
import pymongo
import hashlib
import datetime
import uuid
import lib.promptpay
import os
from flask import Flask, render_template, request, jsonify, session, redirect

app = Flask("HotelSystem")
app.secret_key = "%^&*(&&^*^*^&%**"

# File Upload Setting
app.config["path"] = os.path.join(os.getcwd(), "bin", "payment")
app.config["allow_image_type"] = ["JPEG","PNG","JPG"]
app.config["max_image_size"] = 3 * (1024 * 1024)

@app.route("/")
def home() :
	connect = connect_to()
	data = connect["hoteldata"]["rooms"].find({})

	return render_template("home.html",rooms=data,session=session)

@app.route("/booking")
def booking() :
	if not "username" in session :
		return redirect("/")

	connect = connect_to()
	find = connect["hoteldata"]["booking"].find({
		"user.username" : session["username"]
	})

	return render_template("booking.html",dataroom=find)

	 
@app.route("/api/logout", methods=["GET"])
def logout() :
	session.clear()
	return jsonify({
		"code" : 200
	})

@app.route("/api/login", methods=["POST"])
def login() :
	connect = connect_to()
	data = connect["hoteldata"]["users"].find_one({
		"username" : request.form["username"],
		"password" : hashlib.md5(request.form["password"].encode("utf-8")).hexdigest()
	})

	if not data is None :
		session["username"] = data["username"]

		return jsonify({
			"code" : 200,
			"message" : "เข้าสู่ระบบสำเร็จ"
		})
	
	return jsonify({
		"code" : 401,
		"message" : "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
	})

@app.route("/api/payment_show", methods=["POST"])
def paymentshow() :
	connect = connect_to()
	if not "username" in session :
		return jsonify({
			"code" : 401,
			"message" : "กรุณาเข้าสู่ระบบ เพื่อดูห้องพัก"
		})

	data = connect["hoteldata"]["booking"].find_one({
		"bookid" : request.form["bookid"],
		"user.username" : session["username"]
	})

	if not data is None :
		qr_payment = lib.promptpay.createqr_promptpay(account="0888888888",one_time=True,money=str(data["payment"]["payment_ammout"]))
		return jsonify({
			"code" : 200,
			"html" : render_template("payment.html",qrcode=qr_payment,bookid=data["bookid"])
		})

@app.route("/api/inforoom", methods=["POST"])
def inforoom() :
	connect = connect_to()
	data = connect["hoteldata"]["rooms"].find_one({
		"roomid" : request.form["roomid"]
	})

	if not data is None :
		return jsonify({
			"code" : 200,
			"html" : render_template("data/inforoom.html",data_room=data)
		})

@app.route("/api/infobooking", methods=["POST"])
def infobooking() :
	connect = connect_to()
	if not "username" in session :
		return jsonify({
			"code" : 401,
			"message" : "กรุณาเข้าสู่ระบบ เพื่อดูห้องพัก"
		})

	data = connect["hoteldata"]["booking"].find_one({
		"bookid" : request.form["bookid"],
		"user.username" : session["username"]
	})

	if not data is None :
		return jsonify({
			"code" : 200,
			"html" : render_template("data/infobooking.html",data_room=data)
		})

@app.route("/api/selectroom", methods=["POST"])
def selectroom() :
	connect = connect_to()
	if not "username" in session :
		return jsonify({
			"code" : 401,
			"message" : "กรุณาเข้าสู่ระบบ เพื่อจองห้องพัก"
		})

	data = connect["hoteldata"]["rooms"].find_one({
		"roomid" : request.form["roomid"]
	})

	if not data is None :
		return jsonify({
			"code" : 200,
			"html" : render_template("data/selectroom.html",data_room=data)
		})

@app.route("/payment/<id>", methods=["GET","POST"])
def paymentpage(id) :
	if not "username" in session :
		return redirect("/")

	connect = connect_to()
	find = connect["hoteldata"]["booking"].find_one({
		"bookid" : str(id)
	})

	if find and "username" in session and "user" in find :
		if find["user"]["username"] == session["username"] :
			return render_template("payment_page.html",bookid=find["bookid"])
		
		return redirect("/")

	return redirect("/")
		

@app.route("/api/payment", methods=["POST"])
def payment() :
	if not "username" in session :
		return jsonify({
			"code" : 401,
			"message" : "กรุณาเข้าสู่ระบบ เพื่อจองห้องพัก"
		})
	
	connect = connect_to()
	
	find = connect["hoteldata"]["rooms"].find_one({
		"roomid" : request.form["roomid"]
	})

	if not find is None :
		if not find["status"] is False :
			start = datetime.datetime.strptime(request.form["start"], "%m/%d/%Y")
			end = datetime.datetime.strptime(request.form["end"], "%m/%d/%Y")

			diff = end - start
			if diff.days >= 1 :
				bookid = str(uuid.uuid4())
				insert = connect["hoteldata"]["booking"].insert_one({
					"date" : datetime.datetime.now(),
					"bookid" : bookid,
					"status" : "NOPAYMENT",
					"details" : {
						"roomid" : request.form["roomid"],
						"start" : start,
						"end" : end
					},
					"payment" : {
						"payment_status" : False,
						"payment_ammout" : diff.days * find["price"],
						"payment_timeout" : datetime.datetime.now() + datetime.timedelta(hours=1)
					},
					"user" : {
						"username" : session["username"]
					}
				})

				if insert :
					# Generate QR Code PromptPay
					qrcode = lib.promptpay.createqr_promptpay(
						account="0888888889",
						money=str(diff.days * find["price"])
					)

					return jsonify({
						"code" : 200,
						"html" : render_template("payment.html",qrcode=qrcode,bookid=bookid)
					})
			
			return jsonify({
				"code" : 400,
				"message" :  "กรุณาเลือกวันถัดไป"
			})

		return jsonify({
			"code" : 400,
			"message" : "ห้องนี้ได้ถูกจองไปแล้ว"
		})

	return jsonify({
		"code" : 404,
		"message" : "ไม่พบห้อง"
	})

@app.route("/api/uploadpayment", methods=["POST"])
def uploadpayment() :
	if not "username" in session :
		return jsonify({
			"code" : 401,
			"message" : "กรุณาเข้าสู่ระบบ เพื่อจองห้องพัก"
		})
	
	connect = connect_to()
	find = connect["hoteldata"]["booking"].find_one({
		"bookid" : request.form["bookid"]
	})

	if find and "username" in session and "user" in find :
		if find["user"]["username"] == session["username"] :
			if "slipt" in request.files :
				slipt = request.files["slipt"]
				slipt_data = slipt.read()

				if check_image_type(slipt.filename) :
					if len(slipt_data) >= app.config["max_image_size"] :
						return({
							"code" : 400,
							"message" : "ไฟล์มีขนาดใหญ่เกินไป กรุณาลองใหม่อีกครั้ง"
						})

					payment = uuid.uuid4()
					with open(os.path.join(app.config["path"], (str(payment) + "." + slipt.filename.rsplit(".",1)[1])),"wb") as w :
						w.write(slipt_data)

					update = connect["hoteldata"]["booking"].update_one({
						"bookid" : request.form["bookid"]
					},
					{
						"$set" : {
							"status" : "WAITINGPAYMENT",
							"payment.paymentid" : (str(payment) + "." + slipt.filename.rsplit(".",1)[1]),
							"payment.payment_timeout" : None
						}
					})

					update_room = connect["hoteldata"]["rooms"].update_one({
						"roomid" : find["details"]["roomid"]
					},
					{
						"$set" : {
							"status" : False
						}
					})

					return ({
						"code" : 200,
						"message" : "อัพโหลดสำเร็จ กรุณารอภาพใน 1 - 2 ในการยืนยันการชำระเงิน",
						"redirect" : "/"
					})
				
				return({
					"code" : 400,
					"message" : "ไฟล์นี้ไม่รองรับการอัพโหลด กรุณาอัพโหลดไฟล์ชนิด PNG และ JPEG เท่านั้น"
				}) 

	return({
		"code" : 401,
		"message" : "เกิดข้อผิดพลาด กรุณาติดต่อฝ่ายผู้ดูแลระบบ"
	})

def check_image_type(file) :
	if "." in file :
		sp_filename = file.rsplit(".",1)[1]

		if sp_filename.upper() in app.config["allow_image_type"] :
			return True 
	
	return False

def connect_to() :
	connect = pymongo.MongoClient("mongodb://root:123456@localhost:27017/admin")
	connect.server_info()

	return connect

app.run(
	host="127.0.0.1",
	port=8000,
	debug=True
)