import nfc, urllib2, binascii, traceback, datetime, time, os, shlex
from subprocess import call


BASE_URL = 'http://localhost:8080/{id}'
clf = nfc.ContactlessFrontend('usb')

def beep(r=1):
    if r == 1:
        cmd = 'beep -l 200 -f 800 -f 659 -l 200 -D 25 -n -f 659 -l 200 -D 25 -n -f 659 -l 400 -D 25 -n -f 659 -l 200 -D 25 -n -f 659 -l 200 -D 25 -n -f 659 -l 400 -D 25 -n -f 659 -l 200 -D 25 -n -f 783 -l 200 -D 25 -n -f 523 -l 200 -D 25 -n -f 587 -l 200 -D 25 -n -f 659 -l 400 -D 25'
    else:
        cmd = 'beep -r {} -d 200 -f 800'.format(r)
    call(shlex.split(cmd))

def nfc_tag_connected(tag):
    id = binascii.hexlify(tag.identifier)
    try:
        response = urllib2.urlopen(BASE_URL.format(id=id))
        print("[{}] Request sent for {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id))
        beep()
    except urllib2.HTTPError as e:
        if e.code == 404:
            beep(r=2)
        else:
            beep(r=3)
            traceback.print_exc()
    except Exception as e:
        beep(r=3)
        traceback.print_exc()

    time.sleep(5)


print("[{}] Starting RFID tunnel ...".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
while 1:
    clf.connect(rdwr={'on-connect': nfc_tag_connected})
