import web
import settings

db = web.database(dbn='sqlite', db=settings.DB_FILE)

TABLES = { #each table must have an 'id' column of type INTEGER AUTOINCREMENT
    'user'  : ('id', 'firstname', 'lastname', 'email', 'active', 'balance', 'rfid'),
    'operation' : ('id', 'user_id', 'amount', 'date')
}

class Model(object):
    columns = ()
    table_name = ""

    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns

    def all(self, *args, **kwargs):
        order = kwargs.pop('order_by', None)

        r = db.select(self.table_name, order=order)
        return [Entry(self, **x) for x in r]

    def new(self, *args, **kwargs):
        return Entry(self, created=False, **kwargs)

    def filter(self, *args, **kwargs):
        order = kwargs.pop('order_by', None)

        r = db.select(self.table_name, order=order, where=kwargs)
        return [Entry(self, **x) for x in r]

    def get(self, *args, **kwargs):
        r = self.filter(*args, **kwargs)
        if len(r) == 0:
            raise Entry.DoesNotExist
        elif len(r) > 1:
            raise Entry.MultipleObjectsReturned
        else:
            return r[0]

    def __repr__(self):
        return "<Model: {}>".format(self.table_name.title())


class Entry(object):
    model = Model

    _data = {}
    _created = False

    class DoesNotExist(Exception):
        pass

    class MultipleObjectsReturned(Exception):
        pass

    def __init__(self, model, created=True, **kwargs):
        self.model = model
        self._created = created
        self._data = {}

        for c in self.model.columns:
            if c in kwargs:
                self._data[c] = kwargs[c]
            else:
                self._data[c] = None

    def __getattr__(self, attr):
        if attr in self.model.columns:
            return self._data[attr]

        return super(Entry, self).__getattribute__(attr)

    def __setattr__(self, attr, value):
        if attr in self.model.columns:
            self._data[attr] = value
        else:
            super(Entry, self).__setattr__(attr, value)

    def __repr__(self):
        return "<{} : id={}>".format(self.model.table_name.title(), self.id)

    def update(self, *args, **kwargs):
        for k,v in kwargs.items():
            if k in self.model.columns:
                self._data[k] = v

        self.save()

    def delete(self):
        db.delete(self.model.table_name, where={'id':self.id})
        self._data = {}

    def save(self):
        if self._created:
            #print(self._data)
            db.update(self.model.table_name, where={'id':self.id}, **self._data)
        else:
            d = self._data.copy()
            d.pop('id')
            self.id = db.insert(self.model.table_name, **d)
            self._created = True



#Initializing
for k,v in TABLES.items():
    m = Model(k, v)
    globals()[k.title()] = m


if __name__ == '__main__':
    import os, datetime

    #Deleting previous DB and creating a fresh one
    try:
        os.remove(settings.DB_FILE)
    except OSError:
        pass
    db = web.database(dbn='sqlite', db=settings.DB_FILE)
    schema = open('schema.sql').read()

    queries = [x+";" for x in schema.split(";")]
    for q in queries:
        db.query(q)
