import googletrans
import numpy as np
import pyautogui, os

file_name = 'armis'
num = 2
num = np.arange(int(f"{num}"))
translator = googletrans.Translator()

# 추출한 텍스트 열기
for n in num:
    os.startfile('{}_{}_original.txt'.format(file_name, n+1))

# 번역 진행 여부 질문
confirm = pyautogui.confirm('번역 하시겠습니까?\n번역 하시려면 문장을 정리 후 확인을 눌러주세요')
# 확인 선택 시 진행
if confirm == 'OK':
    try:  # 텍스트가 여러개 실행
        for n in num:  # 이미지 수만큼 반복
            with open("{}_{}_original.txt".format(file_name, n + 1), 'rt', encoding='UTF8') as f:  # 번역할 파일 불러오기
                lines = f.readlines()
            for line in lines:
                try:
                    text = translator.translate(line, src='en', dest='ko')  # 불러온 문장 번역
                    text = f"{text.text}\n"  # 번역한 문장에서 text만 추출
                    print(text)
                    with open("{}_{}_translated.txt".format(file_name, n + 1), 'a',
                              encoding='utf=8') as f:  # 번역한 문장을 문서에 저장
                        f.write(text)
                except IndexError as e:
                    print()
    except FileNotFoundError:  # 텍스트가 한개면 실행
        with open("{}_1_original.txt".format(file_name), 'r') as f:  # 번역할 파일 불러오기
            lines = f.readlines()
        for line in lines:
            try:
                text = translator.translate(line, src='en', dest='ko')  # 불러온 문장 번역
                text = f"{text.text}\n"  # 번역한 문장에서 text만 추출
                print(text)
                with open("{}_1_translated.txt".format(file_name), 'a', encoding='utf=8') as f:  # 번역한 문장을 문서에 저장
                    f.write(text)
            except IndexError:
                print()
# 취소 선택 시 진행
else:
    pass
