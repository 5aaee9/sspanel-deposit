import cymysql
import Config
from cymysql.converters import escape_string as escape


def getCursor(db):
    def _call(func):
        def __call(*args, **kwargs):
            _conn = cymysql.connect(host=Config.DB_HOST, port=Config.DB_PORT, user=Config.DB_USER,
                                    passwd=Config.DB_PASS, db=db, charset='utf8')
            _conn.autocommit(True)
            cur = _conn.cursor()
            ret = func(cur, *args, **kwargs)
            cur.close()
            _conn.close()
            return ret
        return __call
    return _call


@getCursor(Config.DB_PAYBASE)
def createTrade(cur, amount, email):
    """
    Create a trade of Alipay

    :param conn: connect
    :param cur: Connect of Db
    :type amount: int
    :param amount: The amount of money
    :param email: The user email
    :return: Created id
    """
    cur.execute("INSERT INTO `trade` (`status`, `amount`, `email`) VALUES ('0', '" + str(amount) + "', " + escape(email) + ");")
    cur.execute("select LAST_INSERT_ID();")
    rows = cur.fetchone()
    if rows is None:
        return -1
    return rows[0]


@getCursor(Config.DB_PAYBASE)
def finishTrade(cur, tid, addsum):
    """
    Finish a trade

    :param conn: connect
    :param cur: Connect of Db
    :param addsum: The addsum that api return
    :param tid: The trade's id
    :return: Nil
    """
    cur.execute("UPDATE `trade` SET `status` = 1, `addsum` = " + escape(addsum) + " WHERE `id`=" + str(tid) + ";")


@getCursor(Config.DB_PAYBASE)
def isTradeFinished(cur, tid):
    """
    Check trade is finished
    Because one trade maybe use may times

    :param cur: Connect of Db
    :param tid: Trade id
    :return: The status of trade
    :rtype: bool
    """
    cur.execute("SELECT status FROM `trade` WHERE `id`=" + str(tid) + ";")
    rows = cur.fetchone()
    if rows is not None and rows[0] == 0:
        return False
    else:
        return True


@getCursor(Config.DB_BASE)
def createMoneyCode(cur, code, amount):
    """
    Create the money code

    :param cur: Connect of Db
    :param code: The code you want to create
    :param amount: The amount the code has
    :return: Code's ID
    :rtype: int
    """
    cur.execute("INSERT INTO `code` (`code`, `type`, `number`, `isused`, `userid`, `usedatetime`) VALUES ('" + str(
        code) + "', -1, " + str(float(amount)) + ", 0, 0, '1989:06:04 02:30:00')")
    cur.execute("select LAST_INSERT_ID();")
    rows = cur.fetchone()
    if rows is None:
        return -1
    return rows[0]


@getCursor(Config.DB_BASE)
def getMoneyCode(cur, tid):
    """
    Get the card id of code

    :param cur: connect
    :param tid: Code id
    :return: Card ID
    """
    cur.execute("SELECT code FROM `code` WHERE `id`=" + str(tid) + ";")
    rows = cur.fetchone()
    if rows is None:
        return ""
    return rows[0]


@getCursor(Config.DB_PAYBASE)
def getAmount(cur, tid):
    """
    Get the amount of trade

    :param cur: connect
    :param tid: Trade id
    :return: Trade amount
    """
    cur.execute("SELECT amount FROM `trade` WHERE `id`=" + str(tid) + ";")
    rows = cur.fetchone()
    if rows is None:
        return -1
    return rows[0]


@getCursor(Config.DB_PAYBASE)
def getMail(cur, tid):
    """
    Get the email of trade

    :param cur: connect
    :param tid: Trade id
    :return: Trade amount
    """
    cur.execute("SELECT email FROM `trade` WHERE `id`=" + str(tid) + ";")
    rows = cur.fetchone()
    if rows is None:
        return -1
    return rows[0]
