import pygame
import keyboard
import os
import glob
import shutil  # to move file
from pydub import AudioSegment
import subprocess

# start pygame
pygame.mixer.init()

# finding mp3 file
def find_first_mp3_file():
    mp3_files = glob.glob('*.mp3')
    if mp3_files:
        return mp3_files[0]
    return None


filename = find_first_mp3_file()


if filename:
    pygame.mixer.music.load(filename)
    print(f'Loaded {filename}')
else:
    print('No MP3 file found in the directory.')
    exit(0)



# create directory
if os.path.isdir(filename[0:-4]):
    shutil.rmtree(filename[0:-4])
os.makedirs(filename[0:-4], exist_ok=True)


print('Please enter full lyrics (press Ctrl+Z to finish):')

lines = []
ep = True
line = ''

# input lyric
while True:
    try:
        i = input()
        if not i == '':
            if ep:
                line = i + '<br>'
                ep = False
            else:
                lines.append(line + i)
                ep = True
                line = ''
    except EOFError:
        break

# playing music
pygame.mixer.music.play()

out = ''
counter = 0

print("Press 'p' to place time on lyric line")

# get time in lyric format
def show_time():
    milliseconds = pygame.mixer.music.get_pos()
    seconds = milliseconds // 1000
    milliseconds=milliseconds-seconds*1000
    minutes = seconds // 60
    seconds = seconds % 60
    print(f"Music time: {minutes:02}:{seconds:02} , lines {counter+1}/{len(lines)}")
    return f'[00:{minutes:02}:{seconds:02}.{milliseconds:03}]'

# keyboard loop
while True:
    try:
        # pressing p
        if keyboard.is_pressed('p'):
            temp = show_time() + lines[counter] + '\n'
            counter = counter + 1
            print(temp)
            out = out + temp
            
            
            # lock p
            while keyboard.is_pressed('p'):
                pass

        if not (len(lines) - counter):
            with open(f'{filename[0:-4]}.lrc', 'w', encoding='utf-8') as file:
                file.write(out)
            print("Lyrics saved to .lrc file")

            break

    except Exception as e:
        print(f'Exception: {e}')
        break


# stop music to move it
pygame.mixer.music.stop()
pygame.mixer.music.unload()

sound = AudioSegment.from_mp3(filename)
sound.export(filename[0:-4]+'.wav', format="mp3")

#demo
#####################
audio = AudioSegment.from_mp3(filename)
extracted_part = audio[60000:80000]

temp_wav = "temp.wav"
extracted_part.export(temp_wav, format="wav")

subprocess.run([
    'ffmpeg', '-i', temp_wav, 
    '-c:a', 'libopus', 
    '-b:a', '64k',     
    "demo_"+filename[0:-4]+".ogg"
])
########################


shutil.move(filename[0:-4]+'.lrc', filename[0:-4])
shutil.move(filename[0:-4]+'.wav', filename[0:-4])
shutil.move("demo_"+filename[0:-4]+".ogg", filename[0:-4])
shutil.move(filename, filename[0:-4])
os.remove(temp_wav)
