# pip install pytesseract

from PIL import Image
import pytesseract
import numpy as np

file_name = 'armis'
folder_name = "output_Image"
num = 2

# tesseract 실행파일위치
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 이미지에서 텍스트 추출
try: # 이미지가 여러장이면 실행
    num = np.arange(int(f"{num}"))
    for n in num: # 이미지 수만큼 반복
        text = pytesseract.image_to_string(Image.open("{}\{}_{}.jpg".format(folder_name, file_name, n+1))) # 이미지에서 텍스트 추출
        with open("{}_{}_original.txt".format(file_name, n+1), "w", encoding='utf8') as f: # 저장
            f.write(text)
except FileNotFoundError: # 이미지가 한장이면 실행
    text = pytesseract.image_to_string(Image.open("{}\{}_1.jpg".format(folder_name, file_name))) # 이미지에서 텍스트 추출
    with open("{}_1_original.txt".format(file_name), "w", encoding='utf8') as f: # 저장
        f.write(text)

# text = pytesseract.image_to_string(Image.open("test.jpg"), lang="Kor") # 한글 이미지의 경우 lang 옵션 추가
# print(text.replace("  ", "")) # 공백 제거

