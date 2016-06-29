#coding: utf-8

import web, datetime, pyqrcode
from utils import datetime2str, get_object_or_404, float2str, urlize
from io import BytesIO

from settings import CONSUMPTION_UNIT, APP_URL
from models import User, Operation
from forms import CreditForm, ConsumeInlineForm, ConsumeForm, UserForm

urls = (
    '/', 'users',
    '/users/(\d+)', 'user',
    '/users/add', 'edit_user',
    '/users/edit/(\d+)', 'edit_user',
    '/credit/(\d+)', 'credit',
    '/consume/(\d+)', 'consume',
    '/qr/(\d+)', 'qr',
    '/sheet', 'sheet',
    '/rfid/(\w+)', 'rfid',
)

template_globals = {'datetime2str':datetime2str, 'float2str':float2str, 'urlize': urlize}

render = web.template.render('templates/', globals=template_globals, base='base')

class users:
    def GET(self):
        users = User.all()
        return render.users(users, CreditForm(), ConsumeInlineForm())

class user:
    def GET(self, id):
        user = get_object_or_404(User, id=id)
        operations = Operation.filter(user_id=id, order_by='date DESC')
        form = ConsumeForm()

        return render.user(user, operations, form)

class edit_user:
    def GET(self, id=None):
        form = UserForm()

        user = None
        if id is not None:
            user = get_object_or_404(User, id=id)
            form.fill(firstname=user.firstname, lastname=user.lastname, email=user.email, fgs=user.fgs, rfid=user.rfid)

        return render.edit_user(form, user)

    def POST(self, id=None):
        form = UserForm()
        user = None
        if id is not None:
            user = get_object_or_404(User, id=id)

        if not form.validates():
            return render.edit_user(form, user)

        if user is None:
            user = User.new()
            user.balance = 0

        user.firstname = form.d.firstname
        user.lastname = form.d.lastname
        user.email = form.d.email
        user.fgs = form.d.fgs
        user.rfid = form.d.rfid
        user.save()

        raise web.seeother('/users/{}'.format(user.id))

class credit:
    def POST(self, id):
        user = get_object_or_404(User, id=id)
        form = CreditForm()

        if not form.validates():
            return render.credit(user, form)

        Operation.new(user_id=id, amount=form.d.amount, date=datetime.datetime.now()).save()
        user.balance += float(form.d.amount)
        user.save()

        raise web.seeother('/')

class consume:
    def POST(self, id):
        user = get_object_or_404(User, id=id)
        form = ConsumeForm()

        if not form.validates():
            raise web.seeother('/users/{}'.format(user.id))

        amount = CONSUMPTION_UNIT*int(form.d.units)
        Operation.new(user_id=id, amount=-amount, date=datetime.datetime.now()).save()
        user.balance -= float(amount)
        user.save()

        raise web.seeother('/')

class qr:
    def GET(self, id):
        url = urlize(APP_URL, '/consume/{}'.format(id))

        buf = BytesIO()
        qr = pyqrcode.create(url)
        qr.svg(buf, scale=1.9)

        return buf.getvalue()

class sheet:
    def GET(self):
        users = User.all()
        return web.template.render('templates/', globals=template_globals).sheet(users)


class rfid:
    def GET(self, id):
        user = get_object_or_404(User, rfid=id)
        amount = CONSUMPTION_UNIT
        Operation.new(user_id=id, amount=-amount, date=datetime.datetime.now()).save()
        user.balance -= float(amount)
        user.save()

        return "OK"


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

