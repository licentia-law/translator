# pip install moviepy
# pip install pydub

import os, sys, time, pydub, googletrans, shutil, pyautogui
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr

try:
    # 사용자 이름 가져오기
    id = os.getlogin()
    print("사용자 이름 가져오기 완료")

    # 번역할 파일 이름 변수 생성
    while True:
        file_name = str(pyautogui.prompt('번역하실 mp4 파일을 바탕화면에 놓은 뒤 파일 이름을 기입해주세요.'
                                         '\n(확장자는 생략)'))
        if os.path.isfile("C:/Users/{}/Desktop/{}.mp4".format(id, file_name)) is True:
            break
        elif file_name == 'None':
            print("프로그램 종료")
            sys.exit()
        else:
            r = pyautogui.confirm('바탕화면에서 {}.mp4 파일을 찾을 수 없습니다.'.format(file_name))
            if r == 'Cancel':
                print("프로그램 종료")
                sys.exit()
            else:
                pass
    print("파일 이름 입력 완료")

    start_time = time.time()

    # 메인 폴더 생성
    path_main = "c:/Users/{}/Downloads/Law_Translator".format(id)
    if not os.path.isdir(path_main):
        os.mkdir(path_main)
    path_main = "c:/Users/{}/Downloads/Law_Translator/{}".format(id, file_name)
    if not os.path.isdir(path_main):
        os.mkdir(path_main)

    # 오디오 폴더 생성
    path_audio = "c:/Users/{}/Downloads/Law_Translator/{}/audio".format(id, file_name)
    if not os.path.isdir(path_audio):
        os.mkdir(path_audio)

    # 오디오 조각 폴더 생성
    path_audio_chunks = "c:/Users/{}/Downloads/Law_Translator/{}/audio\\audio-chunks".format(id, file_name)
    if not os.path.isdir(path_audio_chunks):
        os.mkdir(path_audio_chunks)

    # 텍스트 폴더 생성
    path_txt = "c:/Users/{}/Downloads/Law_Translator/{}/txt".format(id, file_name)
    if not os.path.isdir(path_txt):
        os.mkdir(path_txt)
    print("폴더 생성 완료")

    # mp4에서 mp3 추출
    clip = mp.VideoFileClip("c:/Users/{}/Desktop/{}.mp4".format(id, file_name))
    clip.audio.write_audiofile("{}\{}.mp3".format(path_audio, file_name))
    print("mp4에서 mp3 추출 완료")

    # mp3를 wav로 변형
    sound = pydub.AudioSegment.from_mp3("{}\{}.mp3".format(path_audio, file_name))
    sound.export("{}\{}.wav".format(path_audio, file_name), format="wav")
    path_wav = "{}\{}.wav".format(path_audio, file_name)
    print("mp3를 wav로 변형 완료")

    # wav에서 text 추출
    r = sr.Recognizer()
    """
    1. 큰 용량의 오디오를 작은 용량으로 나눈 후
    2. 각각의 조각을 번역하여
    3. txt로 저장
    """
    # wav 불러오기
    sound = AudioSegment.from_wav(path_wav)
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
    f = open("{}/{}_original.txt".format(path_txt, file_name), 'a')
    for i, audio_chunk in enumerate(chunks, start=1):
        # 작은 용량으로 나눈 오디오 조각을 저장
        chunk_filename = os.path.join(path_audio_chunks, "{}/{}_{}.wav".format(path_audio_chunks, file_name, i))
        audio_chunk.export(chunk_filename, format="wav")
        # 작은 용량으로 나눈 오디오 조각을 불러옴
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # 오디오에서 텍스트 추출 후 번역
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                # print()
                pass
            # 번역한 텍스트를 txt에 저장
            else:
                text = f"{text.capitalize()}.\n"
                # print(text)
                f.write(text)
    f.close()
    print("텍스트 저장 완료")

    # 번역 진행 여부 질문
    os.startfile(f"{path_txt}")
    confirm = pyautogui.confirm('번역 하시겠습니까?'
                                '\n번역 하려면 텍스트를 정리하신 후 확인을 눌러주세요'
                                '\n종료 하려면 취소를 눌러주세요')

    translator = googletrans.Translator()
    # 확인 선택 시 진행
    if confirm == 'OK':
        print("번역 진행")
        with open("{}/{}_original.txt".format(path_txt, file_name), 'r') as f: # 번역할 파일 불러오기
            lines = f.readlines()
        for line in lines:
            text = translator.translate(line, src='en', dest='ko') # 불러온 문장 번역
            text = f"{text.text}\n" # 번역한 문장에서 text만 추출
            # print(text)
            with open("{}/{}_translated.txt".format(path_txt, file_name), 'a', encoding='utf=8') as f:# 번역한 문장을 문서에 저장
                f.write(text)
        print("번역 완료")
    # 취소 선택 시 진행
    else:
        print("번역 안함")
        pass

    # 번역 소요 시간 측정
    end_time = time.time() # 완료 시간
    whole_time = end_time - start_time # 소요 시간
    time_required_m_s = divmod(int(whole_time), 60) # 소요 초 산출
    time_required_h_m = divmod(time_required_m_s[0], 60) # 소요 시, 분 산출
    # 시, 분, 초 각각 변수에 바인딩
    h = time_required_h_m[0]
    m = time_required_h_m[1]
    s = time_required_m_s[1]
    if h > 0 : # 시간이 0보다 크면 아래 문장 출력
        time_required = "소요 시간 : {}시간 {}분 {}초".format(h, m, s)
    elif m > 0 : # 분이 0보다 크면 아래 문장 출력
        time_required = "소요 시간 : {}분 {}초".format(m, s)
    else: # 시와 분이 0이면 아래 문장 출력
        time_required = "소요 시간 : {}초".format(s)
    pyautogui.alert(title="Law's Translator", text='번역이 완료되었습니다!'
                                                   '\n{}'.format(time_required))
    os.startfile(f"{path_txt}")
    print("완료 메세지 팝업 완료")
except Exception as e:
    print("에러 발생", e)
    pyautogui.alert(text='에러가 발생했습니다.'
                         '\n에러 내용 : {}'.format(e))