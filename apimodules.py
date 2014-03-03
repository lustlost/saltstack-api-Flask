# -*- coding: utf-8 -*-
from flask.ext.restful import Resource,reqparse
from flask import request
import hashlib, time, commands
import salt.client

class Token():
    def __init__(self):
        self.now_time = time.strftime('%Y-%m-%d-%H',time.localtime(time.time()))
    def getToken(self,key):
        md5 = hashlib.md5()
        md5.update(self.now_time+key)
        return md5.hexdigest()
    def authToken(self,one_token,two_token):
        if one_token == two_token:
            return True
        else:
            return False


class saltApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('tgt',type=str)
        self.parser.add_argument('fun',type=str)
        self.parser.add_argument('timeout',type=int)
        self.parser.add_argument('args',type=str)
        self.parser.add_argument('token',type=str)
        self.parser.add_argument('server_config',type=str)
        self.parser.add_argument('expr_form',type=str)
        self.parser.add_argument('ret',type=str)
        self.request_args = self.parser.parse_args()
        self.local = salt.client.LocalClient()
        
    def post(self):
        self.tgt = self.request_args['tgt']
        self.fun = self.request_args['fun']
        self.timeout = self.request_args['timeout']
        self.args = self.request_args['args']
        self.token = self.request_args['token']
        self.expr_form = self.request_args['expr_form']
        self.ret = self.request_args['ret']
        self.server_config = self.request_args['server_config']
        key = 'haha'
        auth_state = Token().authToken(self.token,Token().getToken(key))
        if not auth_state: return "Auth Wrong... Don't crack, or I will fuck you..."
        if not self.args:
            return self.local.cmd(self.tgt,
                                 self.fun,
                                 expr_form=self.expr_form,
                                 ret=self.ret,
                                 timeout=self.timeout,
                                )
        else:
            return self.local.cmd(self.tgt,
                                 self.fun,
                                 [self.args],
                                 expr_form=self.expr_form,
                                 ret=self.ret,
                                 timeout=self.timeout,
                                )
