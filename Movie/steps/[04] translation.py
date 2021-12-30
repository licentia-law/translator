import googletrans, os

file_name = 'snowflake_test'



def translate_original_to_text():
    translator = googletrans.Translator()
    # 번역한 파일 저장할 폴더 생성
    folder_name = "output_text" # 생성할 폴더 이름 지정
    if not os.path.isdir(folder_name): # 만약 지정한 이름의 폴더가 없으면
        os.mkdir(folder_name) # 지정한 폴더 이름으로 폴더 생성

    f = open("output_text\{}_original.txt".format(file_name), 'r') # 번역할 파일 불러오기
    lines = f.readlines()
    f.close()

    for line in lines:
        text = translator.translate(line, src='en', dest='ko') # 불러온 문장 번역
        text = f"{text.text}\n" # 번역한 문장에서 text만 추출
        print(text)

        f = open("{}_translated.txt".format(file_name), 'a', encoding='utf=8') # 번역한 문장을 문서에 저장
        f.write(text)
        f.close()

translate_original_to_text()