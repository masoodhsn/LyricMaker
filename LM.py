from ast import Pass
import pygame
import keyboard
import os
import glob

# راه‌اندازی pygame
pygame.mixer.init()

# پیدا کردن اولین فایل mp3 در دایرکتوری
def find_first_mp3_file():
    mp3_files = glob.glob('*.mp3')
    if mp3_files:
        return mp3_files[0]
    return None

# پیدا کردن فایل صوتی
filename = find_first_mp3_file()

if filename:
    # بارگذاری فایل صوتی
    pygame.mixer.music.load(filename)
    print(f'Loaded {filename}')
else:
    print('No MP3 file found in the directory.')
    exit(0)


print('please entre full lyric (press Ctrl+D or Ctrl+Z to finish):')

lines = []

while True:
    try:
        line = input()
        lines.append(line)
    except EOFError:
        break



# پخش آهنگ
pygame.mixer.music.play()


out=''
counter=0

print("Press 'p' to place time on lyric line, press 's' to save")

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
            temp=show_time()+lines[counter]+'\n'
            counter=counter+1
            print(temp)
            out=out+temp
            
            # برای جلوگیری از چند بار اجرا شدن با یک فشار دکمه، مکث کوتاه اضافه می‌کنیم
            while keyboard.is_pressed('p'):
                pass


        if keyboard.is_pressed('s'):
            
            with open(f'{filename[0:-4]}.lrc', 'w') as file:
                file.write(out)
            print("Lyrics saved to music.lrc")
            break
            while keyboard.is_pressed('s'):
                pass


    except:
        print('exeption')
        break