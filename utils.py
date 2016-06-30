#coding: utf-8

import datetime, web, pyqrcode, pickle
from models import Entry
from settings import APP_URL
import urllib.parse

def urlize(uri):
    return urllib.parse.urljoin(APP_URL, uri)

def float2str(f):
    return "{:.2f}".format(f)

def get_object_or_404(model, **kwargs):
    try:
        obj = model.get(**kwargs)
        return obj
    except Entry.DoesNotExist:
        raise web.notfound()

def datetime2str(dt):
    dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f") #TODO assez moche, dépend du résultat de SQLite..
    return dt.strftime('%d/%m/%y %H:%M')

