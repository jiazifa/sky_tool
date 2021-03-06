import sys
from os import path
import logging

from flask import Flask
import pytest
# 将路径添加到 sys.path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from app import create_app
from celery_tasks.email import Mail, Message

@pytest.fixture("module")
def app():
    app = create_app('testing')
    yield app

@pytest.fixture("module")
def client(app):
    return app.test_client()


def test_md5(client):
    rv = client.get("/api/tool/encryption/md5?source=123456")
    assert rv.status_code == 200
    assert rv.json["data"]["source"] == "123456"
    assert rv.json["data"]["type"] == "md5"
    assert rv.json["data"]["target"] == "e10adc3949ba59abbe56e057f20f883e"

def test_sha512(client):
    rv = client.get("/api/tool/encryption/sha512?source=123456")
    assert rv.status_code == 200
    assert rv.json["data"]["source"] == "123456"
    assert rv.json["data"]["type"] == "sha512"
    assert rv.json["data"]["target"] == "ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413"

# def test_mail():
#     user = "sunshukang30@163.com"
#     password = "a12345678" # 授权码
#     receivers = ["804506054@qq.com", "2332532718@qq.com"]
#     sender = user
#     mail = Mail("smtp.163.com", user, password, 465,  True, sender, 10)
#     message = Message(subject="我是测试主题", recipients=receivers, body="测试Body", sender=sender)
#     mail.send(message)


def test_logging():
    logger_name = "example"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create file handle
    log_path = "./test_log.log"
    file_handle = logging.FileHandler(log_path)
    file_handle.setLevel(logging.WARNING)

    # create formatter
    formatter = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    date_formatter = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(formatter, date_formatter)

    # add handler and formatter to logger
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)

    logger.debug("debuge message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")