# encoding: utf-8
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
from datetime import datetime


def isEmail(email):
    return re.match("^.+@(\\[?)[a-zA-Z0-9\\-.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None


class Actions(object):
    def __init__(self, app):
        self.app = app
        self._db = Db
        self.trade_time = datetime.now().strftime('%Y%m%d%H%M%S%f')

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
        @self.app.route("/deposit/", methods=['GET', 'POST'])
        def index():
            errors = []
            status = 200
            types = 0
            try:
                if not isEmail(request.form["email"]):
                    errors.append("Error email address")
                try:
                    float(request.form["number"])
                except ValueError:
                    errors.append("Numbers Error!")
                try:
                    types = int(request.form["type"])
                except ValueError:
                    errors.append("Unknow Error!")
            except KeyError:
                errors.append("Error form!")

            if not errors:
                email = request.form["email"]
                amount = float(request.form["number"])
                tid = self._db.createTrade(amount, email)
                if types == 0:
                    return redirect(url_for('deposit', tid=tid))
                else:
                    return redirect(url_for('code', tid=tid))

            if request.method == "GET":
                errors = []
            else:
                status = 422
            if types == 1:
                return json.dumps({"ok": 0, "errors": errors}), 422
            return render_template("index.html", errors=errors), status

        @self.app.route("/deposit/code/<tid>")
        def code(tid):
            try:
                billing_id = str(2113447) + str(self.trade_time)
                tid = int(tid)
                if self._db.isTradeFinished(tid):
                    return redirect(url_for('index'))
                amount = self._db.getAmount(tid)
                return render_template("code.html",
                                       url="https://api.jsjapp.com/plugin.php?id=add:alipay2&addnum=%s&total=%s&apiid=%s&apikey=%s&uid=%s&showurl=%s" % (
                                           billing_id, amount, Config.ALIPAY_ID, hashlib.md5(Config.ALIPAY_KEY).hexdigest(), tid,
                                           Config.SITE_ADDR + url_for('success') + "?type=1"
                                       ))
            except ValueError:
                return redirect(url_for('index'))

        @self.app.route("/deposit/charge/<tid>")
        def deposit(tid):
            try:
                billing_id = 'alip' + str(13447) + self.trade_time
                tid = int(tid)
                if self._db.isTradeFinished(tid):
                    return redirect(url_for('index'))
                amount = self._db.getAmount(tid)
                return render_template("form.html", config={
                    "uuid": tid,
                    "total": amount,
                    "apiid": Config.ALIPAY_ID,
                    "showurl": Config.SITE_ADDR + url_for('success'),
                    "apikey": hashlib.md5(Config.ALIPAY_KEY).hexdigest(),
                    "addnum": billing_id
                })
            except ValueError:
                return redirect(url_for('index'))

        @self.app.route("/deposit/success", methods=["POST", "GET"])
        def success():
            if request.method == "GET":
                return redirect(url_for('index'))

            try:
                uid = int(request.form["uid"])
                addnum = request.form["addnum"]
                apikey = request.form["apikey"]
                if "type" not in request.args:
                    type = 0
                else:
                    type = 1
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

            self.sendMail("游戏娘 <support@youxiniang.com>", email, "感谢您的订购.", """Hi,
非常感谢您选择了我们的服务.
你的充值码: %s
充值码面额: %s

Thanks,
游戏娘""" % (code, amount))

            template = {
                0: "success.html",
                1: "success_code.html"
            }[type]

            if not addnum.startswith("alip"):
                return render_template(template, email=email, type=True)
            return render_template(template, email=email, type=False)

        @self.app.route("/deposit/success/<tid>", methods=["POST", "GET"])
        def successById(tid):
            try:
                mail = self._db.getMail(tid)
                if not mail:
                    raise ValueError
            except Exception as e:
                return redirect(url_for('index'))
            return render_template("success.html", email=mail, type=False)
