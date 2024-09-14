import pygame
import keyboard
import os
import glob
import shutil  # برای جابجا کردن فایل
from pydub import AudioSegment

# راه‌اندازی pygame
pygame.mixer.init()

# پیدا کردن اولین فایل mp3 در دایرکتوری 
def find_first_mp3_file():
    mp3_files = glob.glob('*.mp3')
    if mp3_files:
        return mp3_files[0]
    else:
        exit(0)
    return None

# پیدا کردن فایل صوتی
filename = find_first_mp3_file()

if os.path.isdir(filename[0:-4]):
    shutil.rmtree(filename[0:-4])

# ساخت پوشه با نام آهنگ بدون پسوند
os.makedirs(filename[0:-4], exist_ok=True)

if filename:
    # بارگذاری فایل صوتی
    pygame.mixer.music.load(filename)
    print(f'Loaded {filename}')
else:
    print('No MP3 file found in the directory.')
    exit(0)

print('Please enter full lyrics (press Ctrl+Z to finish):')

lines = []
ep = True
line = ''

# دریافت ورودی‌های کاربر برای شعر
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

# پخش آهنگ
pygame.mixer.music.play()

out = ''
counter = 0

print("Press 'p' to place time on lyric line")

# تابع برای نمایش زمان پخش بر حسب میلی‌ثانیه و تبدیل به ثانیه
def show_time():
    milliseconds = pygame.mixer.music.get_pos()
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    print(f"Music time: {minutes:02}:{seconds:02} , lines {counter+1}/{len(lines)}")
    return f'[00:{minutes:02}:{seconds:02}]'

# حلقه برای گوش دادن به ورودی صفحه کلید
while True:
    try:
        # اگر کلید p فشار داده شود
        if keyboard.is_pressed('p'):
            temp = show_time() + lines[counter] + '\n'
            counter = counter + 1
            print(temp)
            out = out + temp
            
            
            # برای جلوگیری از چند بار اجرا شدن با یک فشار دکمه، مکث کوتاه اضافه می‌کنیم
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


pygame.mixer.music.stop()
pygame.mixer.music.unload()
# جابجا کردن فایل به پوشه جدید با استفاده از shutil.move

sound = AudioSegment.from_mp3(filename)
sound.export(filename[0:-4]+'.wav', format="wav")

#demo
audio = AudioSegment.from_mp3(filename)
extracted_part = audio[60000:80000]
extracted_part.export("demo_"+filename[0:-4]+".ogg", format="mp3")


shutil.move(filename[0:-4]+'.lrc', filename[0:-4])
shutil.move(filename[0:-4]+'.wav', filename[0:-4])
shutil.move("demo_"+filename[0:-4]+".ogg", filename[0:-4])
shutil.move(filename, filename[0:-4])
