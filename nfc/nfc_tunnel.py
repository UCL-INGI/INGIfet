import nfc, urllib2, binascii, traceback, datetime


BASE_URL = 'http://localhost:8080/{id}'
clf = nfc.ContactlessFrontend('usb')

def nfc_tag_connected(tag):
    id = binascii.hexlify(tag.identifier)
    try:
        response = urllib2.urlopen(BASE_URL.format(id=id))
        print("[{}] Request sent for {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id))
    except Exception as e:
        traceback.print_exc()

while 1:
    clf.connect(rdwr={'on-connect': nfc_tag_connected})
