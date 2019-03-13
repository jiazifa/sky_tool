from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mssql import FLOAT, TEXT, INTEGER, DECIMAL, SMALLINT
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound, \
    UnmappedColumnError
from sqlalchemy import Sequence
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, g, render_template, current_app
from flask_uploads import UploadSet, DEFAULTS
from flask_socketio import SocketIO
import redis
from apscheduler.schedulers.background import BackgroundScheduler


# 定时执行
scheduler = BackgroundScheduler()
socket_app = SocketIO()
db = SQLAlchemy()

fileStorage = UploadSet(extensions=DEFAULTS)

pool = redis.ConnectionPool(port=6379)
redisClient = redis.Redis(connection_pool=pool)

__all__ = ["Column", "ForeignKey", "String", "FLOAT",
           "TEXT", "INTEGER", "DECIMAL", "SMALLINT",
           "NoResultFound", "MultipleResultsFound",
           "UnmappedColumnError", "Sequence",
           "Flask", "request", "redisClient", "db",
           "fileStorage", "jsonify", "g", "render_template",
           "scheduler", "current_app", "celery_app", "socket_app"]