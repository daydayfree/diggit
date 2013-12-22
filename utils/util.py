# -*- coding: utf-8 -*-

import hashlib
import smtplib
from email.MIMEText import MIMEText
import logging
import time
import os.path
import traceback
import datetime
import binascii
import uuid

class Email(object):    
    _smtp_server = 'smtp.sina.net'
    _smtp_port = '25' 
    _smtp_user = 'xueming@top100.cn'  
    _smtp_password = ''
    _receivers = ["daydayfree@gmail.com", "daydayfree@hotmail.com"]

    @staticmethod
    def send(content):
        msg = MIMEText(content)
        msg["Subject"] = "Blade Error"
        msg["From"] = Email._smtp_user
        msg["To"] = str(Email._receivers)

        server = smtplib.SMTP(Email._smtp_server, Email._smtp_port)
        server.ehlo()
        server.login(Email._smtp_user, Email._smtp_password)
        server.sendmail(
            Email._smtp_user, Email._receivers, msg.as_string())
        server.quit()
        

class Log(object):
    @staticmethod
    def get_path(name=None):
        if not name:
            name = time.strftime('%Y%m', time.localtime(time.time()))
        return os.path.join(
            os.path.dirname(__file__), '../log/%s.log' % name)

    @staticmethod
    def error(msg, name="error"):
        format = "%(asctime)-15s %(filename)s Line:%(lineno)d %(message)s"
        logging.basicConfig(format=format, level=logging.ERROR)
        logger = logging.getLogger(name)
        handler = logging.FileHandler(Log.get_path(name))
        logger.addHandler(handler)
        if isinstance(msg, Exception):
            msg = traceback.format_exc()
        logger.error(msg)
        #Email.send(msg)

    @staticmethod
    def info(msg, name="info"):
        format = "%(asctime)-15s %(message)s"
        logging.basicConfig(format=format, level=logging.INFO)
        logger = logging.getLogger(name)
        handler = logging.FileHandler(Log.get_path(name))
        logger.addHandler(handler)
        logger.info(msg)


def sha1(basestring):
    hash = hashlib.sha1()
    hash.update(basestring)
    return hash.hexdigest()


def get_uuid():
    return binascii.b2a_hex(uuid.uuid4().bytes)


def json_encode(content):
    if not content or content == "": return ""
    if not isinstance(content, str): return content
    content = content.decode("utf-8", "ignore")
    result = []
    for i in range(len(content)):
        char = content[i]
        if char == "\"":
            result.append("\\\"")
        elif char == "\\":
            result.append("\\\\")
        elif char == "/":
            result.append("\\/")
        elif char == "\b":
            result.append("\\b")
        elif char == "\f":
            result.append("\\f")
        elif char == "\n":
            result.append("\\n")
        elif char == "\r":
            result.append("\\r")
        elif char == "\t":
            result.append("\\t")
        else:
            result.append(char)
    return "".join(result)


class TimeDeltaFormat(object):
    @staticmethod
    def format(date):
        end = datetime.datetime.now()
        delta = end - date
        days = delta.days
        seconds = delta.seconds
        if days > 365:
            years = int(days / 365)
            return "%d年前" % years
        if days > 30:
            months = int(days / 30)
            return "%d个月前" % months
        if days > 7:
            weeks = int(days / 7)
            return "%d周前" % weeks
        if days > 0:
            return "%d天前" % days
        if seconds > 3600:
            hours = int(seconds / 3600)
            return "%d个小时前" % hours
        if seconds > 60:
            minutes = int(seconds / 60)
            return "%d分钟前" % minutes
        return "1分钟前"
