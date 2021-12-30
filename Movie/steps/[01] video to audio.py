# pip install moviepy

import moviepy.editor as mp
import os

folder_name_audio = "output_audio"
if not os.path.isdir(folder_name_audio):
    os.mkdir(folder_name_audio)

def translation_mp4_to_mp3():
    while True:
        file_name = str(input('Please input file name to translate : ')).lower().strip()
        if os.path.isfile("{}.mp4".format(file_name)):
            break
        else:
            print('{}.mp4 could not be found.'.format(file_name))

    clip = mp.VideoFileClip("{}.mp4".format(file_name))
    clip.audio.write_audiofile("output_audio\{}.mp3".format(file_name))

translation_mp4_to_mp3()
