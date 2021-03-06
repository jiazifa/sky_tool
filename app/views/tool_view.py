# -*- coding: utf-8 -*-
"""

@file: tool_view.py
@time: 2019-01-28 11:45

"""
import hashlib
import json
from flask import request, redirect, url_for
from ..views import api
from app.utils import response_succ, CommonError, login_require
from app.utils.ext import socket_app, redisClient, db

@api.route("/tool/encryption/<string:encrypt_type>", methods=["POST", "GET"])
def encryption(encrypt_type: str = "md5"):
    """
    指定加密方式
    :param encrypt_type: encryption type default is "md5"...
    support
    'sha1','md5', 'sha256', 'sha224', 'sha512', 'sha384', 'blake2b',
    'blake2s', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
    'shake_128', 'shake_256'
    :return:
    """
    params = request.values or request.get_json() or {}
    print("p = " + str(params))
    source = params.get("source")
    if not source:
        return CommonError.get_error(40000)

    code: str = source
    encrypt_func = getattr(hashlib, encrypt_type, None) or None
    if not encrypt_func:
        return CommonError.get_error(40000)
    result = encrypt_func(code.encode('utf-8')).hexdigest()
    result_map = dict()
    result_map["source"] = source
    result_map["target"] = result
    result_map["type"] = encrypt_type
    return response_succ(body=result_map)


@socket_app.on('rec_client')
def handle_client_message(msg):
    print(msg['data'])
    socket_app.emit('resp_server', {'data': 'i hear you' + str(msg['data'])})
    

@api.route('/tool/email_to', methods=['GET', 'POST'])
@login_require
def email_to():
    params = request.values  or request.get_json() or {}
    subject = params.get('subject')
    body = params.get('body')
    recs = params.get('recipients')
    files = params.get('fileIds')
    if not subject or not body or not recs:
        return CommonError.get_error(40000)
    from celery_tasks.tasks import async_email_to
    receivers = []
    if isinstance(recs, str):
        receivers.append(recs)
    elif isinstance(recs, list):
        receivers.extend(recs)
    fileIds = []
    if isinstance(files, str):
        fileIds.append(files)
    elif isinstance(files, list):
        fileIds.extend(files)
    result = {}
    result['recipients'] = receivers
    task = async_email_to.delay(subject=subject, body=body, recipients=receivers, attaches=fileIds)
    result['task_id'] = task.id
    return response_succ(body=result)

@api.route('/tool/query_task', methods=['GET', 'POST'])
@login_require
def query_task():
    params = request.values  or request.get_json() or {}
    key: str = params.get('key') or 'celery*'
    if not key:
        return CommonError.get_error(40000)
    result = redisClient.get('celery-task-meta-'+str(key))
    if isinstance(result, bytes):
        reuslt = str(result, encoding='utf-8')
        result = json.loads(result)
    else:
        return CommonError.error_toast('no task')
    return response_succ(body=result)
