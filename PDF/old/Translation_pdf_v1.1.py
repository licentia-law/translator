# pip install pytesseract
# pip install pdf2image
# pip install pyautogui
# pip install PIL
# pip install numpy

import sys, os, pyautogui, pytesseract, googletrans, time
from pdf2image import convert_from_path
from PIL import Image
import numpy as np

try:
    # tesseract 실행파일 위치 지정
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # 사용자 이름 가져오기
    id = os.getlogin()
    print("사용자 이름 가져오기 완료")

    # 번역할 파일 이름 변수 생성
    while True:
        file_name = str(pyautogui.prompt('번역하실 PDF 파일을 바탕화면에 놓은 뒤 파일 이름을 기입해주세요.'
                                         '\n(확장자는 생략)'))
        if os.path.isfile("C:/Users/{}/Desktop/{}.pdf".format(id, file_name)) is True:
            break
        elif file_name == 'None' :
            print("프로그램 종료")
            sys.exit()
        else:
            r = pyautogui.confirm('바탕화면에서 {}.pdf 파일을 찾을 수 없습니다.'.format(file_name))
            if r == 'Cancel':
                print("프로그램 종료")
                sys.exit()
            else:
                pass
    print("파일 이름 입력 완료")

    start_time = time.time() # 시작 시간

    # 메인 폴더 생성
    path_main = "c:/Users/{}/Downloads/Law_Translator".format(id)
    if not os.path.isdir(path_main):
        os.mkdir(path_main)
    path_main = "c:/Users/{}/Downloads/Law_Translator/{}".format(id, file_name)
    if not os.path.isdir(path_main):
        os.mkdir(path_main)

    # 이미지 폴더 생성
    path_img = "c:/Users/{}/Downloads/Law_Translator/{}/img".format(id, file_name)
    if not os.path.isdir(path_img):
        os.mkdir(path_img)

    # 텍스트 폴더 생성
    path_txt = "c:/Users/{}/Downloads/Law_Translator/{}/txt".format(id, file_name)
    if not os.path.isdir(path_txt):
        os.mkdir(path_txt)
    print("폴더 생성 완료")

    # PDF를 이미지로 변환
    path_pdf = "C:/Users/{}/Desktop/{}.pdf".format(id, file_name) # pdf 불러오기
    images = convert_from_path(path_pdf) # pdf를 PIL object로 변환
    print("PDF를 이미지로 변환 완료")

    # 이미지 저장
    num = 0 # 파일 뒤에 붙일 번호 변수 생성
    for image in images: # PIL object에서 파일 1개씩 호출
        num += 1 # 파일 뒤에 붙일 번호를 1씩 더함
        image.save('{}/{}_{}.jpg'.format(path_img, file_name, num)) # 호출한 파일을 jpg로 변환하여 저장
    print("이미지 저장 완료")

    # 이미지에서 텍스트 추출
    try: # 이미지가 여러장이면 실행
        num = np.arange(int(f"{num}"))
        for n in num: # 이미지 수만큼 반복
            text = pytesseract.image_to_string(Image.open("{}/{}_{}.jpg".format(path_img, file_name, n+1))) # 이미지에서 텍스트 추출
            with open("{}/{}_{}_original.txt".format(path_txt, file_name, n+1), "w", encoding='utf8') as f: # 저장
                f.write(text)
    except FileNotFoundError: # 이미지가 한장이면 실행
        text = pytesseract.image_to_string(Image.open("{}\{}_1.jpg".format(path_img, file_name))) # 이미지에서 텍스트 추출
        with open("{}/{}_{}_original.txt".format(path_txt, file_name, n+1), "w", encoding='utf8') as f: # 저장
            f.write(text)
    # text = pytesseract.image_to_string(Image.open("test.jpg"), lang="Kor") # 한글 이미지의 경우 lang 옵션 추가
    # print(text.replace("  ", "")) # 공백 제거
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
        try:  # 텍스트가 여러개면 실행
            for n in num:  # 이미지 수만큼 반복
                with open("{}/{}_{}_original.txt".format(path_txt, file_name, n+1), 'rt', encoding='UTF8') as f:  # 번역할 파일 불러오기
                    lines = f.readlines()
                for line in lines:
                    try:
                        text = translator.translate(line, src='en', dest='ko')  # 불러온 문장 번역
                        text = f"{text.text}\n"  # 번역한 문장에서 text만 추출
                        # print(text)
                        with open("{}/{}_{}_translated.txt".format(path_txt, file_name, n + 1), 'a',
                                  encoding='utf=8') as f:  # 번역한 문장을 문서에 저장
                            f.write(text)
                    except IndexError as e:
                        # print()
                        pass
        except FileNotFoundError:  # 텍스트가 한개면 실행
            with open("{}/{}_1_original.txt".format(path_txt, file_name), 'r') as f:  # 번역할 파일 불러오기
                lines = f.readlines()
            for line in lines:
                try:
                    text = translator.translate(line, src='en', dest='ko')  # 불러온 문장 번역
                    text = f"{text.text}\n"  # 번역한 문장에서 text만 추출
                    # print(text)
                    with open("{}/{}_1_translated.txt".format(path_txt, file_name), 'a', encoding='utf=8') as f:  # 번역한 문장을 문서에 저장
                        f.write(text)
                except IndexError:
                    # print()
                    pass
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