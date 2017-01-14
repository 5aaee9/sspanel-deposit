from flask import redirect, url_for
from flask import render_template
from flask import request
import requests
import hashlib
import Config
import string
import random
import json
import re
import Db


def isEmail(email):
    return re.match("^.+@(\\[?)[a-zA-Z0-9\\-.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None


class Actions(object):
    def __init__(self, app):
        self.app = app
        self._db = Db.Db(False)

    @staticmethod
    def sendMail(fromP, toP, subject, text):
        return requests.post(
            "https://api.mailgun.net/v3/" + Config.MAIL_DOAM + "/messages",
            auth=("api", Config.MAIL_KEY),
            data={"from": fromP,
                  "to": [toP],
                  "subject": subject,
                  "text": text})

    @staticmethod
    def getRandomChar(size=16):
        return ''.join(random.sample(string.ascii_letters + string.digits, size))

    def init(self):
        @self.app.route("/", methods=['GET', 'POST'])
        def index():
            self._db.connect()
            errors = []
            status = 200
            try:
                if not isEmail(request.form["email"]):
                    errors.append("Error email address")
                try:
                    float(request.form["number"])
                except ValueError:
                    errors.append("Numbers Error!")
            except KeyError:
                errors.append("Error form!")

            if not errors:
                email = request.form["email"]
                amount = float(request.form["number"])
                tid = self._db.createTrade(amount, email)
                return redirect(url_for('deposit', tid=tid))

            if request.method == "GET":
                errors = []
            else:
                status = 422
            return render_template("index.html", errors=errors), status

        @self.app.route("/deposit/<tid>")
        def deposit(tid):
            self._db.connect()
            try:
                tid = int(tid)
                if self._db.isTradeFinished(tid):
                    return redirect(url_for('index'))
                amount = self._db.getAmount(tid)
                return render_template("form.html", config={
                    "uuid": tid,
                    "total": amount,
                    "apiid": Config.ALIPAY_ID,
                    "showurl": Config.SITE_ADDR + url_for('success'),
                    "apikey": hashlib.md5(Config.ALIPAY_KEY).hexdigest()
                })
            except ValueError:
                return redirect(url_for('index'))

        @self.app.route("/success", methods=["POST"])
        def success():
            print
            self._db.connect()
            try:
                uid = int(request.form["uid"])
                addnum = request.form["addnum"]
                apikey = request.form["apikey"]
            except ValueError:
                return redirect(url_for('index'))

            # Trade finished
            if self._db.isTradeFinished(uid):
                return redirect(url_for('index'))

            # APIKey Not Verify
            if not apikey == hashlib.md5(Config.ALIPAY_KEY + addnum).hexdigest():
                return redirect(url_for('index'))

            self._db.finishTrade(uid, addnum)
            code = self.getRandomChar(42)
            amount = self._db.getAmount(uid)
            email = self._db.getMail(uid)

            self._db.createMoneyCode(code, amount)

            self.sendMail("Indexyz <bill@shadowsocks.nu>", email, "Thanks for your product.", """Hi,
Thanks for you product in our service.
Your code is: %s
You deposit: %s
Thanks,
Indexyz""" % (code, amount))

            return render_template("success.html", email=email)