import speech_recognition as sr
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

file_name = "snowflake_test"

# sr.Recognizer 객체 생성
r = sr.Recognizer()

def get_large_audio_transcription(path):
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

    # output_audio 폴더 생성
    folder_name_audio_1 = "output_audio"
    if not os.path.isdir(folder_name_audio_1):
        os.mkdir(folder_name_audio_1)

    # output_audio\audio-chucks 폴더 생성 : 작은 용량으로 나눈 오디오 조각 저장
    folder_name_audio_2 = "output_audio\\audio-chunks"
    if not os.path.isdir(folder_name_audio_2):
        os.mkdir(folder_name_audio_2)

    # output_text 폴더 생성 : 번역한 txt 파일 저장
    folder_name_text = "output_text"
    if not os.path.isdir(folder_name_text):
        os.mkdir(folder_name_text)

    # 작은 용량으로 나눈 오디오 조각을 하나씩 불러와서 번역 및 저장
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
                f = open("output_text\{}_original.txt".format(file_name), 'a')
                f.write(text)
                f.close()

get_large_audio_transcription('output_audio\{}.wav'.format(file_name))
