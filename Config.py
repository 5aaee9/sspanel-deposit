import os
DB_HOST    =     os.getenv("DB_HOST", "127.0.01")
DB_PORT    = int(os.getenv("DB_PORT", 3306))
DB_USER    =     os.getenv("DB_USER", "root")
DB_PASS    =     os.getenv("DB_PASS", "")
DB_BASE    =     os.getenv("DB_BASE", "shadowsocks")
DB_PAYBASE =     os.getenv("DB_PAYBASE", "payment")

SITE_ADDR  = os.getenv("SITE_ADDR", "")
ALIPAY_ID  = os.getenv("ALIPAY_ID", "")
ALIPAY_KEY = os.getenv("ALIPAY_KEY", "")
MAIL_KEY   = os.getenv("MAIL_KEY", "")
MAIL_DOAM  = os.getenv("MAIL_DOAM", "")