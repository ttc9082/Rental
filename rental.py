__author__ = 'TTc9082'
import web
from tool import SQL
from tool import AWS
import random
import os

urls = ('/', 'index',
        '/new', 'new',
        '/show', 'show',
        '/test', 'test'
        )

render = web.template.render('templates/')

class index:
    def GET(self):
        db = SQL.SQLtools()
        table = db.lookup('rooms')
        return render.index(table)

class new:
    def GET(self):
        return render.upload()

    def POST(self):
        db = SQL.SQLtools()
        S3 = AWS.AWSS3()
        x = web.input()
