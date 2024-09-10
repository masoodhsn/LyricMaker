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

# پخش آهنگ
pygame.mixer.music.play()

# پرچم برای تعیین وضعیت پخش یا توقف
is_paused = False


out=''

print("Press 'p' to play/pause, 'left arrow' to rewind, 'right arrow' to forward")

# تابع برای نمایش زمان پخش بر حسب میلی‌ثانیه و تبدیل به ثانیه
def show_time():
    milliseconds = pygame.mixer.music.get_pos()
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    print(f"Music time: {minutes:02}:{seconds:02}")
    return f'[00:{minutes:02}:{seconds:02}]'


def get_lyric():
    global out
    input()
    i = input()
    out = out + show_time() + i + '\n'
    print(show_time() + i)

# حلقه برای گوش دادن به ورودی صفحه کلید
while True:
    try:
        # اگر کلید p فشار داده شود
        if keyboard.is_pressed('p'):
            # اگر آهنگ پخش شود، متوقف کن
            if not is_paused:
                pygame.mixer.music.pause()
                is_paused = True
                show_time()  # نمایش زمان توقف
            # اگر آهنگ متوقف است، دوباره پخش کن
            else:
                pygame.mixer.music.unpause()
                is_paused = False
                print("Music Playing")
            
            # برای جلوگیری از چند بار اجرا شدن با یک فشار دکمه، مکث کوتاه اضافه می‌کنیم
            while keyboard.is_pressed('p'):
                pass

        if keyboard.is_pressed('i'):
            get_lyric()
            while keyboard.is_pressed('i'):
                pass

        if keyboard.is_pressed('o'):
            print(out)
            while keyboard.is_pressed('o'):
                pass

        if keyboard.is_pressed('s'):
            with open(f'{filename[0:-4]}.lrc', 'w') as file:
                file.write(out)
            print("Lyrics saved to music.lrc")
            while keyboard.is_pressed('s'):
                pass


    except:
        break
