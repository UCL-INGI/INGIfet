#coding: utf-8

import web, datetime, pyqrcode, pickle
from utils import datetime2str, get_object_or_404, float2str, urlize
from io import BytesIO

import settings
from models import User, Operation
from forms import CreditForm, ConsumeInlineForm, ConsumeForm, UserForm, TemplateForm

web.config.debug = settings.DEBUG

web.config.smtp_server = settings.SMTP_SERVER
web.config.smtp_port = settings.SMTP_PORT
web.config.smtp_username = settings.SMTP_USERNAME
web.config.smtp_password = settings.SMTP_PASSWORD
web.config.smtp_starttls = settings.SMTP_STARTTLS
web.config.debug_level = True

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
    '/mail/(\d+)', 'mail',
    '/mail', 'mail',
    '/mail/template', 'mail_tpl',
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
    def GET(self, id):
        user = get_object_or_404(User, id=id)
        form = ConsumeForm()

        render = web.template.render('templates/', globals=template_globals)
        return render.consume(form, user)


    def POST(self, id):
        user = get_object_or_404(User, id=id)
        form = ConsumeForm()

        if not form.validates():
            raise web.seeother('/users/{}'.format(user.id))

        amount = settings.CONSUMPTION_UNIT*int(form.d.units)
        Operation.new(user_id=id, amount=-amount, date=datetime.datetime.now()).save()
        user.balance -= float(amount)
        user.save()

        if b'userside' in web.data():
            render = web.template.render('templates/', globals=template_globals)
            return render.consume(None, user)
        else:
            raise web.seeother('/')

class qr:
    def GET(self, id):
        url = urlize('/consume/{}'.format(id))

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
        amount = settings.CONSUMPTION_UNIT
        Operation.new(user_id=id, amount=-amount, date=datetime.datetime.now()).save()
        user.balance -= float(amount)
        user.save()

        return "OK"

class mail:
    def GET(self, id=None):
        #if id is None, email everyone with their balance

        if id is not None:
            users = [get_object_or_404(User, id=id)]
        else:
            users = User.all()

        try:
            f = open(settings.MAIL_FILE_TEMPLATE, 'rb')
            tpl = pickle.load(f)
            f.close()
        except (IOError, pickle.PickleError):
            tpl = settings.MAIL_DEFAULT_TEMPLATE

        for u in users:
            body = tpl.format(solde = u.balance)

            web.sendmail(settings.MAIL_ADDRESS, u.email, 'Solde de votre compte cafétaria INGI', body)

        raise web.seeother('/')


class mail_tpl:
    def GET(self):
        try:
            f = open(settings.MAIL_FILE_TEMPLATE, 'rb')
            tpl = pickle.load(f)
            f.close()
        except (IOError, pickle.PickleError):
            tpl = settings.MAIL_DEFAULT_TEMPLATE

        form = TemplateForm()
        form.fill(template=tpl)
        return render.mail_tpl(form)

    def POST(self):
        form = TemplateForm()
        if not form.validates():
            return render.mail_tpl(form)

        f = open(settings.MAIL_FILE_TEMPLATE, 'wb')
        pickle.dump(form.d.template, f)
        f.close()

        raise web.seeother('/mail/template')



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

