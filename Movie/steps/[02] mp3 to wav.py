# pip install pydub

import pydub

file_name = 'snowflake_test'

def translation_mp3_to_wav():
    sound = pydub.AudioSegment.from_mp3("output_audio\{}.mp3".format(file_name))
    sound.export("output_audio\{}.wav".format(file_name), format="wav")

translation_mp3_to_wav()