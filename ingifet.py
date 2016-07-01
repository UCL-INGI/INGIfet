#coding: utf-8

import web, datetime, pyqrcode, pickle
from utils import datetime2str, get_object_or_404, float2str, urlize
from io import BytesIO

import settings
from models import User, Operation, Entry
from forms import CreditForm, ConsumeInlineForm, ConsumeForm, UserForm, TemplateForm, UserSelectForm

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
    '/users/rfid/(\w+)', 'user_rfid',
    '/credit/(\d+)', 'credit',
    '/consume/(\d+)', 'consume',
    '/qr/(\d+)', 'qr',
    '/sheet', 'sheet',
    '/rfid/(\w+)', 'rfid',
    '/mail/(\d+)', 'mail',
    '/mail', 'mail',
    '/mail/template', 'mail_tpl',
)

template_globals = {'datetime2str':datetime2str, 'float2str':float2str, 'urlize': urlize, 'str': str}

render = web.template.render('templates/', globals=template_globals, base='base')

class users:
    def GET(self):
        active_users = User.filter(active=True, order_by='firstname')
        inactive_users = User.filter(active=False, order_by='firstname')
        return render.users(active_users, inactive_users, CreditForm(), ConsumeInlineForm())

class user:
    def GET(self, id):
        user = get_object_or_404(User, id=id)
        operations = Operation.filter(user_id=id, order_by='date DESC')

        return render.user(user, operations)

class edit_user:
    def GET(self, id=None):
        form = UserForm()

        user = None
        rfid = web.input(rfid=None).rfid
        if id is not None:
            user = get_object_or_404(User, id=id)
            form.fill(firstname=user.firstname, lastname=user.lastname, email=user.email, rfid=user.rfid, active=user.active)
        elif rfid:
            form.fill(rfid=rfid)

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
        user.active = form.d.active
        user.rfid = form.d.rfid
        user.save()

        raise web.seeother('/users/{}'.format(user.id))

class user_rfid:
    def GET(self, rfid):
        form = UserSelectForm(User.all())()

        return render.user_rfid(form, rfid)

    def POST(self, rfid):
        form = UserSelectForm(User.all())()

        if form.validates():
            user_id = form.d.user
            user = get_object_or_404(User, id=user_id)
            user.rfid = rfid
            user.save()

            raise web.seeother('/')

        return render.user_rfid(form, rfid)

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
        qr.svg(buf, scale=1.5)

        return buf.getvalue()

class sheet:
    def GET(self):
        users = User.filter(active=True)
        return web.template.render('templates/', globals=template_globals).sheet(users)


class rfid:
    def GET(self, id):
        try:
            user = User.get(rfid=id)
            amount = settings.CONSUMPTION_UNIT
            Operation.new(user_id=user.id, amount=-amount, date=datetime.datetime.now()).save()
            user.balance -= float(amount)
            user.save()

            return "OK"
        except Entry.DoesNotExist:
            body = settings.MAIL_TPL_UNKNOWN_CARD.format(
                    new_user_url = urlize('/users/add/?rfid={}'.format(id)),
                    existing_user_url = urlize('/users/rfid/{}'.format(id)),
                    hour=datetime.datetime.now().strftime('%H:%M'))

            web.sendmail(settings.MAIL_ADDRESS,
                settings.SECRETARY_MAIL_ADDRESS,
                '[INGIfet] Carte inconnue {}'.format(id),
                body)

            raise web.notfound()


class mail:
    def GET(self, id=None):
        #if id is None, email every active user with his balance

        if id is not None:
            users = [get_object_or_404(User, id=id)]
        else:
            users = User.filter(active=True)

        try:
            f = open(settings.MAIL_FILE_TEMPLATE, 'rb')
            tpl = pickle.load(f)
            f.close()
        except (IOError, pickle.PickleError):
            tpl = settings.MAIL_DEFAULT_TEMPLATE

        for u in users:
            body = tpl.format(solde = u.balance, prenom = u.firstname, nom = u.lastname)

            web.sendmail(settings.MAIL_ADDRESS, u.email, 'Your INGI cafetaria balance', body)

        userside = web.input(u=0).u != 0
        if userside:
            render = web.template.render('templates/', globals=template_globals)
            return render.consume('BALANCE', u)

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

