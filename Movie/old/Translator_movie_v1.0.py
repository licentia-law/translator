# pip install moviepy
# pip install pydub

import os, time, pydub, googletrans, shutil
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr

# 폴더 생성 : mp3, wav 저장
folder_name_audio = "output_audio"
if not os.path.isdir(folder_name_audio):
    os.mkdir(folder_name_audio)

# 폴더 생성 : 작은 용량으로 나눈 오디오 조각 저장
folder_name_audio_2 = "output_audio\\audio-chunks"
if not os.path.isdir(folder_name_audio_2):
    os.mkdir(folder_name_audio_2)

# 번역할 파일 이름 변수 생성
while True:
    file_name = str(input('Please input file name to translate : ')).lower().strip()
    if os.path.isfile("{}.mp4".format(file_name)):
        break
    else:
        print('{}.mp4 could not be found.'.format(file_name))

start = time.time()

# mp4에서 mp3 추출
def translation_mp4_to_mp3():
    clip = mp.VideoFileClip("{}.mp4".format(file_name))
    clip.audio.write_audiofile("output_audio\{}.mp3".format(file_name))
    print("mp4에서 mp3 추출 완료")

# mp3를 wav로 변형
def translation_mp3_to_wav():
    sound = pydub.AudioSegment.from_mp3("output_audio\{}.mp3".format(file_name))
    sound.export("output_audio\{}.wav".format(file_name), format="wav")
    print("mp3를 wav로 변형 완료")

# wav에서 text 추출
def translation_wav_to_text(path):
    r = sr.Recognizer()
    """
    1. 큰 용량의 오디오를 작은 용량으로 나눈 후
    2. 각각의 조각을 번역하여
    3. txt로 저장
    """
    # wav 불러오기
    sound = AudioSegment.from_wav(path)
    # 큰 용량의 오디오를 작은 용량으로 나누기
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )

    # 작은 용량으로 나눈 오디오 조각을 하나씩 불러와서 번역 및 저장
    f = open("{}_original.txt".format(file_name), 'a')
    for i, audio_chunk in enumerate(chunks, start=1):
        # 작은 용량으로 나눈 오디오 조각을 저장
        chunk_filename = os.path.join(folder_name_audio_2, "{}_{}.wav".format(file_name, i))
        audio_chunk.export(chunk_filename, format="wav")
        # 작은 용량으로 나눈 오디오 조각을 불러옴
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # 오디오에서 텍스트 추출 후 번역
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print()
            # 번역한 텍스트를 txt에 저장
            else:
                text = f"{text.capitalize()}.\n"
                print(text)

                f.write(text)
    f.close()

    print("wav에서 text 추출 완료")

# 원본 텍스트를 한글로 번역
def translation_original_to_text():
    translator = googletrans.Translator()

    f = open("{}_original.txt".format(file_name), 'r') # 번역할 파일 불러오기
    lines = f.readlines()
    f.close()

    for line in lines:
        text = translator.translate(line, src='en', dest='ko') # 불러온 문장 번역
        text = f"{text.text}\n" # 번역한 문장에서 text만 추출
        print(text)

        f = open("{}_translated.txt".format(file_name), 'a', encoding='utf=8') # 번역한 문장을 문서에 저장
        f.write(text)
        f.close()

# 작업 종료 안내
def wrap_up():
    shutil.rmtree("output_audio")
    end = time.time()
    print("번역 작업 완료! {}_translated.txt 파일을 확인하세요.\n"
          "번역 소요 시간 : {} 초".format(file_name, (round((end - start), 1))))

# 함수 한번에 패킹
def main():
    translation_mp4_to_mp3()
    translation_mp3_to_wav()
    translation_wav_to_text('output_audio\{}.wav'.format(file_name))
    translation_original_to_text()
    wrap_up()

# main 함수 실행
main()