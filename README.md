# Shadowsocks Panel Deposit
An Panel to auto-progress shadowsocks panel deposit.

[![](https://images.microbadger.com/badges/image/indexyz/sspanel-deposit.svg)](https://microbadger.com/images/indexyz/sspanel-deposit "Get your own image badge on microbadger.com") 

## Support
[ss-panel-v3-moded](https://github.com/esdeathlove/ss-panel-v3-mod)

[金沙江 API](https://api.web567.net)

## Usage
### Run with source code
1. Frist, Install python-pip and git
```bash
# CentOS
yum install epel-release -y
yum install git python-pip -y
```
2. Run
```bash
git clone https://github.com/Indexyz/sspanel-deposit.git
cd sspanel-deposit
pip install -r requirements.txt
```
3. Config your setting (like mail key and apiid)
```bash
nano Config.py
```
Config Values
```
DB_HOST         // MySQL Host
DB_PORT         // MySQL Port
DB_USER         // MySQL User
DB_PASS         // MySQL User Password
DB_BASE         // sspanel's database
DB_PAYBASE      // deposit event's database

SITE_ADDR       // Your site address (For callback)
ALIPAY_ID       // Payment API ID
ALIPAY_KEY      // Payment API Key
MAIL_KEY        // Mail key (Mailgun)
MAIL_DOAM       // The domain you want to send mail
```
4. Run server
```
python Alipay-Panel.py
```
### Run with docker
```bash
# Using -e to set your config
docker run -p 8080:5000 \
       indexyz/sspanel-deposit
```
