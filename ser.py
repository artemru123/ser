import os #1
import random; import requests; import aiohttp
import smtplib;from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify;import sqlite3
from flask_limiter import Limiter

from flask_limiter.util import get_remote_address
import base64; from aiogram import Bot, Dispatcher, types, executor; from aiogram.types import Message; from data import Database









from code import codes; db = Database()
from apscheduler.schedulers.background import BackgroundScheduler
key = "thisissecretkeytohidepasswordofusers00901091010010989109890"; bot = Bot(token='7726098741:AAHcBBhE8uhOqYsiZ3lQbjTiskpdG2e0DY8'); dp = Dispatcher(bot)
def get_db_connection():

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row;return conn
from flask_cors import CORS

import jwt
import datetime

app = Flask(__name__)
CORS(app);














limiter = Limiter(
    get_remote_address,
    app=app,

    default_limits=["100 per 5 minutes"]
)


@app.route('/tie', methods=['GET'])
@limiter.limit("1000 per 5 minutes")
def tie():
    data = db.get_tie()
    results = [{"path": row[0], "text": row[1], "price": row[2], "id": row[3]} for row in data]
    return jsonify(results), 200
@app.route('/info', methods=['POST'])
@limiter.limit("1000 per 5 minutes")
def info():

    data = request.json
    name = data.get('name')

    data =db.load_tie(name);count = len(os.listdir(f'tie/{data[0]}'))
    results = [{"path": data[0], "text": data[1], "price": data[2], "id":data[3], "count": count}]


    return jsonify(results), 200

@app.route('/shop', methods=['POST'])
@limiter.limit("1000 per 5 minutes")
def shop():

    data = request.json

    hash = data.get("hash")
    username = db.get_username(hash)
    shopping_cart = []



    info = db.load_shop(username)

    if info:
        shoping = info[0].split("|")

        for shop in shoping:
            inform = db.load_tie_id(shop.split("*")[0])

            if inform:
                 results = {"path": inform[0], "text": inform[1], "price": int(inform[2]) * int(shop.split("*")[1]), "id": inform[3], "count": shop.split("*")[1], "si": shop.split("*")[2], "perOne": inform[2]}
                 shopping_cart.append(results)

    print((shopping_cart))
    return jsonify(shopping_cart), 200

def xor_encrypt_decrypt(input_string, key):
    return ''.join(chr(ord(char) ^ ord(key[i % len(key)])) for i, char in enumerate(input_string))














def encode_base64(input_string):
    return base64.b64encode(input_string.encode()).decode()

@app.route("/cart", methods=['POST'])
@limiter.limit("1000 per 5 minutes")
def cart():


    data = request.json
    tie = data.get("tie")


    hash = data.get("hash")
    username = db.get_username(hash)
    tie1 = int(data.get("tie_1"))


    res = db.load_all(username)
    print(tie, ";;;", tie1)














    if res[0]:
        info = db.load_shop(username)
        for shop in info[0].split("|"):

            print(shop)
            if shop.split("*")[0] == tie.split("*")[0] and shop.split("*")[2] == tie.split("*")[2]:
                count = int(shop.split("*")[1]) + 1 if tie1 == 0 else int(shop.split("*")[1]) - 1

                new_replace = shop.split("*")[0] + "*" + str(count) + "*" + shop.split("*")[2] if count != 0 else ""; print(shop + "|", '|'.join(info[0].split("|")[1:]))
                msg = info[0].replace((shop + "|") if count == 0 else shop, new_replace)


                db.update_shop(username=username, card=msg)

                return "ok", 200



            else:
                print("new")
                msg = f"{tie}|{info[0]}" if tie1 == 0 else info[0]
                print(tie)
                db.update_shop(username=username, card=msg)

        return "ok", 200
    else:
        return 'no', 400













@app.route('/reg', methods=['POST'])
@limiter.limit("555 per 2 minutes")
def reg():

    data = request.json
    username = data.get('username')
    password = data.get('password')

    email = data.get('email')

    data2 = db.user_exists(username)
    if data2:
        return jsonify(error='exists', message='Account already exists!\nTry another login'), 401

    else:
        info = db.select_mail(email)
        if info:


            return jsonify(error='exists', message='mail is linked to another account\nTry another mail '), 401
        else:
            code = ''.join(random.choices('012789', k=6))
            sender_email = 'jklop0224@gmail.com'
            receiver_email = email
            passwordMail = 'yszh aafw ocab uhvo'
            subject = 'Exclusion | Code'
            body = f'Code for registation: {code}\nExpires in 15 minutes'
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            infor = db.select_mail1(email)
            if infor:
                return jsonify(message="Code already sended"), 401
            else:

                try:
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:

                        server.starttls()  # Secure the connection
                        server.login(sender_email, passwordMail)  # Login to the email server

                        server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email
                    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=15)














                    password = xor_encrypt_decrypt(password, key)
                    password = encode_base64(password)
                    db.registry_code(username, code, email, password, expiration_time)

                    return jsonify(message='Check mail for code'), 200
                except Exception as e:
                    print(f'An error occurred: {e}')

                    return jsonify(message='make sure for mail is exists'), 401
scheduler = BackgroundScheduler()
scheduler.add_job(codes, 'interval', minutes=5)  # Check every 5 minutes
scheduler.start()


@app.route('/checkreg', methods=['POST'])
def checkreg():
    data = request.json

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    password = xor_encrypt_decrypt(password, key); password = encode_base64(password)
    code = data.get('code')
    data2 = db.select_password_code(username, code, email)
    if data2:
        db.registry_user(username, password, code)

        return jsonify(message='Account successfull registered!'), 200










    else:
        return jsonify(message='Uncorrect code'), 401

@app.route('/login', methods=['POST'])

@limiter.limit("10 per 5 minutes")
def login():
    data = request.json;username = data.get('username');password = data.get('password')

    password = xor_encrypt_decrypt(input_string=password, key=key)
    password = encode_base64(password)

    data2 = db.password(username, password)
    if data2:

        if not db.select_hash(username):
            hash = enc(username);db.registry_hash(hash,  datetime.datetime.utcnow() + datetime.timedelta(days=7), username);return jsonify({"message": f"Login successful!", 'token': hash}), 200
        else:

            return jsonify({"message": f"Login successful!", 'token': db.load_hash(username)[0]}), 200
    else:


        return jsonify({"message": "Неправильный логин и/или пароль"}), 401










@app.route("/shopify", methods=['POST'])
async def shopify():
    data = request.json

    hash = data.get('hash'); username = db.get_username(hash)

    data2 = db.get_username(hash); bal = 0; oo = []

    name = data.get("name"); name2 = data.get("name2"); name3 = data.get("name3"); home = data.get("home"); method = data.get("method")
    if data2:

        info = db.load_shop(username)[0]
        for shop in info.split("|"):
            id = (shop.split('*')[0])

            o = db.load_tie_id(id); print(o[2] if o != None else o); bal += o[2] * int(shop.split('*')[1]) if o != None else 0; oo.append(o[1])
        #cursor.execute("UPDATE users SET shop=?, name=?, name1=?, namee=?, home=?, method=?, buyed=? WHERE username=?",(0, name, name2, name3, home, method, "1", username))














        #conn.commit()
        check = db.get_sessions(username)
        if check == None:

            msg = str("".join(random.choices('ABCDE', k=5)) + str("".join(random.choices('106', k=5)))); check1 = db.check_comment(msg)
            if check1 == None:

                await bot.send_message(chat_id=727959236, text=f"Новый заказ!\nИнформация о клиенте\nФИО: {name} {name2} {name3}\nАдрес для доставки: {home}\nСпособ отправки: {method}\nСумма: {bal}\nКомментарий: {msg}\n\nЕго корзина:\n {oo}")
                db.registry_buy(msg, username)
                return jsonify(({"message": "OK", "message_pay": msg, "total": bal})), 200
            else:
                return jsonify(({"message": "error\nTry again"})), 401

        else:
            return jsonify(({"message": "che"})), 401
    else:

        return jsonify({"message": "Неправильный логин и/или пароль"}), 401
@app.route("/send_msg", methods=['GET'])
async def send_msg():
    name = "клиент"; name2 = "Клиентов"; name3 = "Клиентович"; home = "Ул пушкина д 1"; method = "СДЭК";
    await bot.send_message(chat_id=727959236, text=f"Новый заказ!\nИнформация о клиенте\nФИО: {name} {name2} {name3}\nАдрес для доставки: {home}\nСпособ отправки: {method}\nСтатус заказа: Ожидает подтверждения перевода")

    return jsonify({"message": "ok", "uid": '1'}), 200
def enc(login):
    special_enc = random.choice(">_|<!:[")

    hash = ''.join(string + random.choice(">_|<!:[") for string in random.choices("ABCDEF10", k=10))+ login + ''.join(string + random.choice(">_|<!:[") for string in random.choices("ABCDEF10-><", k=10)); hash = hash + str(datetime.datetime.utcnow()); return encode_base64(hash)
@app.route("/hash", methods=['POST'])
def hash():
    data = request.json
    hash = data.get("hash")

    hash1 = db.get_hash(hash)
    if hash1:
        return jsonify({"message": "OK"}), 200


















































































































    else:
        return jsonify({"message": "no"}), 403

@app.route("/youtube", methods=['GET'])
async def youtube():













    async with aiohttp.ClientSession() as session:
        async with session.get(url='https://youtu.be') as response:
            print(response);return await response.text()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000);  executor.start_polling(dp, skip_updates=False)