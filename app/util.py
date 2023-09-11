from . import YTDLP_PATH
import subprocess

def check_youtube_dl_exist():
    return subprocess.run([YTDLP_PATH, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def move_file(src, dst):
    subprocess.run(['mv', src, dst], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)




