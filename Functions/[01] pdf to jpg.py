from pdf2image import convert_from_path
import os

# 번역할 파일 이름 변수 생성
while True:
    file_name = str(input('Please input file name to translate : ')).lower().strip()
    if os.path.isfile("{}.pdf".format(file_name)):
        break
    else:
        print('{}.pdf could not be found.'.format(file_name))

# 이미지 저장할 폴더 생성
folder_name = "output_Image"
if not os.path.isdir(folder_name):
    os.mkdir(folder_name)

# PDF를 이미지로 변환
path = "{}.pdf".format(file_name) # pdf 불러오기
images = convert_from_path(path) # pdf를 PIL object로 변환

# 이미지 저장
num = 0 # 파일 뒤에 붙일 번호 변수 생성
for image in images: # PIL object에서 파일 1개씩 호출
    num += 1 # 파일 뒤에 붙일 번호를 1씩 더함
    image.save('{}\{}_{}.jpg'.format(folder_name, file_name, num)) # 호출한 파일을 jpg로 변환하여 저장
