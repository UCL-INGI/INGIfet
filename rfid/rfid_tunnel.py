import nfc, urllib2, binascii, traceback, datetime, time, os, shlex
from subprocess import call


BASE_URL = 'http://localhost:8080/{id}'
clf = nfc.ContactlessFrontend('usb')

def beep(r=1):
    if r == 1:
        cmd = 'beep -f 164.813778456 -l 223.3 -n -f 174.614115717 -l 223.3 -n -f 195.997717991 -l 501.7 -n -f 329.627556913 -l 501.7 -n -f 261.625565301 -l 501.7 -n -f 293.664767917 -l 223.3 -n -f 261.625565301 -l 223.3 -n -f 261.625565301 -l 501.7 -n -f 246.941650628 -l 501.7 -n -f 246.941650628 -l 501.7 -n -f 146.832383959 -l 223.3 -n -f 164.813778456 -l 223.3 -n -f 174.614115717 -l 501.7 -n -f 293.664767917 -l 501.7 -n -f 246.941650628 -l 501.7 -n -f 261.625565301 -l 223.3 -n -f 246.941650628 -l 223.3'
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
