#coding: utf-8

import web, datetime, pyqrcode
from settings import CONSUMPTION_UNIT, APP_URL
from models import User, Operation
from utils import datetime2str, get_object_or_404, float2str
from io import BytesIO
import urllib.parse

urls = (
    '/', 'users',
    '/users/(\d+)', 'user',
    '/users/add', 'edit_user',
    '/users/edit/(\d+)', 'edit_user',
    '/credit/(\d+)', 'credit',
    '/consume/(\d+)', 'consume',
    '/qr/(\d+)', 'qr',
    '/sheet/', 'sheet',
)

template_globals = {'datetime2str':datetime2str, 'float2str':float2str}

render = web.template.render('templates/', globals=template_globals)#, base='layout')

class users:
    def GET(self):
        users = User.all()
        return render.users(users)

class user:
    def GET(self, id):
        user = get_object_or_404(User, id=id)
        operations = Operation.filter(user_id=id, order_by='date DESC')
        form = consume.form()

        return render.user(user, operations, form)

class edit_user:
    form = web.form.Form(
        web.form.Textbox('firstname', web.form.notnull, 
            size=30, 
            description="Prénom :"),
        web.form.Textbox('lastname', web.form.notnull, 
            size=30,
            description="Nom :"),
        web.form.Textbox('email', web.form.notnull, 
            web.form.regexp(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', 'Adresse mail incorrecte'),
            rows=30,
            description="Adresse mail:"),
        web.form.Textbox('fgs', web.form.notnull, 
            web.form.regexp(r'\d{8}', 'Numéro FGS incorrect'),
            rows=8,
            description="Numéro FGS:"),

        web.form.Button('Envoyer'),
    )


    def GET(self, id=None):
        form = self.form()

        user = None
        if id is not None:
            user = get_object_or_404(User, id=id)
            form.fill(firstname=user.firstname, lastname=user.lastname, email=user.email, fgs=user.fgs)

        return render.edit_user(form, user)

    def POST(self, id=None):
        form = self.form()
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
        user.save()

        raise web.seeother('/users/{}'.format(user.id))

class credit:
    form = web.form.Form(
        web.form.Textbox('amount', web.form.notnull, 
            web.form.regexp(r'[+-]?([0-9]*[.])?[0-9]+', "Le montant entré n'est pas un chiffre valide"),
            size=5,
            post="€",
            description="Montant :"),

        web.form.Button('Envoyer'),
    )

    def GET(self, id):
        user = get_object_or_404(User, id=id)
        form = self.form()

        return render.credit(user, form)

    def POST(self, id):
        user = get_object_or_404(User, id=id)
        form = self.form()

        if not form.validates():
            return render.credit(user, form)

        Operation.new(user_id=id, amount=form.d.amount, date=datetime.datetime.now()).save()
        user.balance += float(form.d.amount)
        user.save()

        raise web.seeother('/users/{}'.format(user.id))

class consume:
    form = web.form.Form(
        web.form.Dropdown('units', [(x,x) for x in range(1,11)], description="Nombre de consommations"),
        web.form.Button('Envoyer'),
    )

    def POST(self, id):
        user = get_object_or_404(User, id=id)
        form = self.form()

        if not form.validates():
            raise web.seeother('/users/{}'.format(user.id))

        amount = CONSUMPTION_UNIT*int(form.d.units)
        Operation.new(user_id=id, amount=-amount, date=datetime.datetime.now()).save()
        user.balance -= float(amount)
        user.save()

        raise web.seeother('/users/{}'.format(user.id))

class qr:
    def GET(self, id):
        url = urllib.parse.urljoin(APP_URL, '/users/{}'.format(id))

        buf = BytesIO()
        qr = pyqrcode.create(url)
        qr.svg(buf, scale=1.9)

        return buf.getvalue()

class sheet:
    def GET(self):
        users = User.all()
        return render.sheet(users)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

