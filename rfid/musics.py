import datetime

## List of available all season musics

music_it_s_a_small_world = '-f 164.813778456 -l 223.3 -n -f 174.614115717 -l 223.3 -n -f 195.997717991 -l 501.7 -n -f 329.627556913 -l 501.7 -n -f 261.625565301 -l 501.7 -n -f 293.664767917 -l 223.3 -n -f 261.625565301 -l 223.3 -n -f 261.625565301 -l 501.7 -n -f 246.941650628 -l 501.7 -n -f 246.941650628 -l 501.7 -n -f 146.832383959 -l 223.3 -n -f 164.813778456 -l 223.3 -n -f 174.614115717 -l 501.7 -n -f 293.664767917 -l 501.7 -n -f 246.941650628 -l 501.7 -n -f 261.625565301 -l 223.3 -n -f 246.941650628 -l 223.3'

music_imperial_march = '-f 800 -l 200 -D 300 -n -f 392 -l 350 -D 100 -n -f 392 -l 350 -D 100 -n -f 392 -l 350 -D 100 -n -f 311.1 -l 250 -D 100 -n -f 466.2 -l 25 -D 100 -n -f 392 -l 350 -D 100 -n -f 311.1 -l 250 -D 100 -n -f 466.2 -l 25 -D 100 -n -f 392 -l 700 -D 100'

# list general all season pool of music
musics = [music_it_s_a_small_world, music_imperial_march]

# addition of time specific musics and condition to add them
music_chrismas_song = '-f 800 -l 200 -D 300 -n -f 659 -l 200 -D 25 -n -f 659 -l 200 -D 25 -n -f 659 -l 400 -D 25 -n -f 659 -l 200 -D 25 -n -f 659 -l 200 -D 25 -n -f 659 -l 400 -D 25 -n -f 659 -l 200 -D 25 -n -f 783 -l 200 -D 25 -n -f 523 -l 200 -D 25 -n -f 587 -l 200 -D 25 -n -f 659 -l 400 -D 25'

def get_musics():
    if (datetime.datetime.now().month == 12):
        musics + [music_chrismas_song]
    else:
        musics
