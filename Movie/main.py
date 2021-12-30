# pip install moviepy
# pip install pydub

import os, sys, time, pydub, googletrans, shutil, pyautogui
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from datetime import datetime

def Update_user_name():
    id = os.getlogin()
    print(f"[{datetime.today()}] Completed to update user name")
    print(f"[{datetime.today()}] id : ", id)
    return id

def Input_file_name():
    while True:
        file_name = str(pyautogui.prompt('번역하실 mp4 파일을 바탕화면에 놓은 뒤 파일 이름을 기입해주세요.'
                                         '\n(확장자는 생략)'))
        if os.path.isfile("C:/Users/{}/Desktop/{}.mp4".format(id, file_name)) is True:
            break
        elif file_name == 'None':
            print(f"[{datetime.today()}] exit")
            sys.exit()
        else:
            r = pyautogui.confirm('바탕화면에서 {}.mp4 파일을 찾을 수 없습니다.'.format(file_name))
            if r == 'Cancel':
                print(f"[{datetime.today()}] exit")
                sys.exit()
            else:
                pass
    print(f"[{datetime.today()}] Completed to input file name")
    print(f"[{datetime.today()}] file_name : ", file_name)
    return file_name

def Make_folder():
    path_main = "c:/Users/{}/Downloads/Law_Translator".format(id) # 메인 폴더 생성
    if not os.path.isdir(path_main):
        os.mkdir(path_main)
    path_main = "c:/Users/{}/Downloads/Law_Translator/{}".format(id, file_name)
    if not os.path.isdir(path_main):
        os.mkdir(path_main)
    path_audio = "c:/Users/{}/Downloads/Law_Translator/{}/audio".format(id, file_name) # 오디오 폴더 생성
    if not os.path.isdir(path_audio):
        os.mkdir(path_audio)
    path_audio_chunks = "c:/Users/{}/Downloads/Law_Translator/{}/audio\\audio-chunks".format(id, file_name) # 오디오 조각 폴더 생성
    if not os.path.isdir(path_audio_chunks):
        os.mkdir(path_audio_chunks)
    path_txt = "c:/Users/{}/Downloads/Law_Translator/{}/txt".format(id, file_name) # 텍스트 폴더 생성
    if not os.path.isdir(path_txt):
        os.mkdir(path_txt)
    print(f"[{datetime.today()}] completed to make folders")
    return path_main, path_audio, path_audio_chunks, path_txt

def Convert_mp4_to_mp3():
    clip = mp.VideoFileClip("c:/Users/{}/Desktop/{}.mp4".format(id, file_name))
    clip.audio.write_audiofile("{}\{}.mp3".format(path_audio, file_name))
    print(f"[{datetime.today()}] completed to convert mp4 to mp3")

def Convert_mp3_to_wav():
    sound = pydub.AudioSegment.from_mp3("{}\{}.mp3".format(path_audio, file_name))
    sound.export("{}\{}.wav".format(path_audio, file_name), format="wav")
    path_wav = "{}\{}.wav".format(path_audio, file_name)
    print(f"[{datetime.today()}] completed to convert mp3 to wav")
    return path_wav

def Extract_text_from_wav():
    r = sr.Recognizer()
    sound = AudioSegment.from_wav(path_wav) # read wav
    # 큰 용량의 오디오를 작은 용량으로 나누기
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,)
    # 작은 용량으로 나눈 오디오 조각을 하나씩 불러와서 번역 및 저장
    with open("{}/{}_original.txt".format(path_txt, file_name), 'a') as f:
        for i, audio_chunk in enumerate(chunks, start=1):
            # 작은 용량으로 나눈 오디오 조각을 저장
            chunk_filename = os.path.join(path_audio_chunks, "{}/{}_{}.wav".format(path_audio_chunks, file_name, i))
            audio_chunk.export(chunk_filename, format="wav")
            # 작은 용량으로 나눈 오디오 조각을 불러와서 번역 후 저장
            with sr.AudioFile(chunk_filename) as source:
                audio_listened = r.record(source)
                try: # 오디오에서 텍스트 추출 후 번역
                    text = r.recognize_google(audio_listened)
                except sr.UnknownValueError as e:
                    # print()
                    pass
                else: # 번역한 텍스트를 txt에 저장
                    text = f"{text.capitalize()}.\n"
                    # print(text)
                    f.write(text)
    print(f"[{datetime.today()}] completed to extract text")

def Question_for_translation():
    os.startfile(f"{path_txt}")
    confirm = pyautogui.confirm('번역 하시겠습니까?'
                                '\n번역 하려면 텍스트를 정리하신 후 확인을 눌러주세요'
                                '\n종료 하려면 취소를 눌러주세요')
    print(f"[{datetime.today()}] confirm : ", confirm)
    return confirm

def Translation():
    translator = googletrans.Translator()
    # if confirm is OK
    if confirm == 'OK':
        with open("{}/{}_original.txt".format(path_txt, file_name), 'r') as f: # 번역할 파일 불러오기
            lines = f.readlines()
        for line in lines:
            text = translator.translate(line, src='en', dest='ko') # 불러온 문장 번역
            text = f"{text.text}\n" # 번역한 문장에서 text만 추출
            # print(text)
            with open("{}/{}_translated.txt".format(path_txt, file_name), 'a', encoding='utf=8') as f:# 번역한 문장을 문서에 저장
                f.write(text)
        print(f"[{datetime.today()}] completed translation")
    # if confirm is cancel
    else:
        print(f"[{datetime.today()}] no translation")
        pass

def Wrap_up():
    end_time = time.time() # 완료 시간
    whole_time = end_time - start_time # 소요 시간
    time_required_m_s = divmod(int(whole_time), 60) # 소요 초 산출
    time_required_h_m = divmod(time_required_m_s[0], 60) # 소요 시, 분 산출
    # 시, 분, 초 각각 변수에 바인딩
    h, m, s = time_required_h_m[0], time_required_h_m[1], time_required_m_s[1]
    if h > 0 : # 시간이 0보다 크면 아래 문장 출력
        time_required = "소요 시간 : {}시간 {}분 {}초".format(h, m, s)
    elif m > 0 : # 분이 0보다 크면 아래 문장 출력
        time_required = "소요 시간 : {}분 {}초".format(m, s)
    else: # 시와 분이 0이면 아래 문장 출력
        time_required = "소요 시간 : {}초".format(s)
    pyautogui.alert(title="Law's Translator", text='번역이 완료되었습니다!'
                                                   '\n{}'.format(time_required))
    os.startfile(f"{path_txt}")
    print(f"[{datetime.today()}] completed to pop up the completion massage")

start_time = time.time()
try:
    id = Update_user_name()
    file_name = Input_file_name()
    path = Make_folder()
    path_main, path_audio, path_audio_chunks, path_txt = path[0], path[1], path[2], path[3]
    Convert_mp4_to_mp3()
    path_wav = Convert_mp3_to_wav()
    Extract_text_from_wav()
    confirm = Question_for_translation()
    Translation()
    Wrap_up()
except Exception as e:
    print(f"[{datetime.today()}] error : {e}")