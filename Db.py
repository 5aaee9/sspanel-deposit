import cymysql
import Config


class Db(object):
    _conn = None
    _pconn = None

    def __init__(self, connect=True):
        if connect:
            self.connect()

    def connect(self):
        """
        Connect to mysql Server

        :return: Nil
        """
        if not self._conn:
            self._conn = cymysql.connect(host=Config.DB_HOST, port=Config.DB_PORT, user=Config.DB_USER,
                                         passwd=Config.DB_PASS, db=Config.DB_BASE, charset='utf8')
        if not self._pconn:
            self._pconn = cymysql.connect(host=Config.DB_HOST, port=Config.DB_PORT, user=Config.DB_USER,
                                          passwd=Config.DB_PASS, db=Config.DB_PAYBASE, charset='utf8')
        self._conn.autocommit(True)
        self._pconn.autocommit(True)

    def disconnect(self):
        """
        Disconnect from MySQL Server

        :return: Nil
        """
        self._conn.close()
        self._pconn.close()

    def createTrade(self, amount, email):
        """
        Create a trade of Alipay

        :type amount: int
        :param amount: The amount of money
        :param email: The user email
        :return: Created id
        """
        cur = self._pconn.cursor()
        cur.execute("INSERT INTO `trade` (`status`, `amount`, `email`) VALUES ('0', '" + str(amount) + "', " + self._pconn.escape(email) + ");")
        cur.execute("select LAST_INSERT_ID();")
        rows = cur.fetchone()
        cur.close()
        if rows is None:
            return -1
        return rows[0]

    def finishTrade(self, tid, addsum):
        """
        Finish a trade

        :param addsum: The addsum that api return
        :param tid: The trade's id
        :return: Nil
        """
        cur = self._pconn.cursor()
        cur.execute("UPDATE `trade` SET `status` = 1, `addsum` = " + self._pconn.escape(addsum) + " WHERE `id`=" + str(tid) + ";")
        cur.close()

    def isTradeFinished(self, tid):
        """
        Check trade is finished
        Because one trade maybe use may times

        :param tid: Trade id
        :return: The status of trade
        :rtype: bool
        """
        cur = self._pconn.cursor()
        cur.execute("SELECT status FROM `trade` WHERE `id`=" + str(tid) + ";")
        rows = cur.fetchone()
        cur.close()
        if rows is not None and rows[0] == 0:
            return False
        else:
            return True

    def createMoneyCode(self, code, amount):
        """
        Create the money code

        :param code: The code you want to create
        :param amount: The amount the code has
        :return: Code's ID
        :rtype: int
        """
        cur = self._conn.cursor()
        cur.execute("INSERT INTO `code` (`code`, `type`, `number`, `isused`, `userid`, `usedatetime`) VALUES ('" + str(code) + "', -1, " + str(float(amount)) + ", 0, 0, '1989:06:04 02:30:00')")
        cur.execute("select LAST_INSERT_ID();")
        rows = cur.fetchone()
        cur.close()
        if rows is None:
            return -1
        return rows[0]

    def getMoneyCode(self, tid):
        """
        Get the card id of code

        :param tid: Code id
        :return: Card ID
        """
        cur = self._conn.cursor()
        cur.execute("SELECT code FROM `code` WHERE `id`=" + str(tid) + ";")
        rows = cur.fetchone()
        cur.close()
        if rows is None:
            return ""
        return rows[0]

    def getAmount(self, tid):
        """
        Get the amount of trade

        :param tid: Trade id
        :return: Trade amount
        """
        cur = self._pconn.cursor()
        cur.execute("SELECT amount FROM `trade` WHERE `id`=" + str(tid) + ";")
        rows = cur.fetchone()
        cur.close()
        if rows is None:
            return -1
        return rows[0]

    def getMail(self, tid):
        """
        Get the email of trade

        :param tid: Trade id
        :return: Trade amount
        """
        cur = self._pconn.cursor()
        cur.execute("SELECT email FROM `trade` WHERE `id`=" + str(tid) + ";")
        rows = cur.fetchone()
        cur.close()
        if rows is None:
            return -1
        return rows[0]

    def __del__(self):
        self.disconnect()
