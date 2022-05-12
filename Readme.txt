챗봇에서 사용한 라이브러리
Flask
pandas
csv

click==8.0.4
colorama==0.4.4
dataclasses==0.8
Flask==2.0.3
importlib-metadata==4.8.3
itsdangerous==2.0.1
Jinja2==3.0.3
MarkupSafe==2.0.1
numpy==1.19.5
pandas==1.1.5
python-dateutil==2.8.2
pytz==2022.1
six==1.16.0
typing_extensions==4.1.1
Werkzeug==2.0.3
zipp==3.6.0

고정 ip 34.64.220.22

##변경된 내용##
# 1. 별점, 사용자 문의 CSV 저장 코드 추가
# 2. 테스트 템플릿 화면(index.html) 추가
# 3. 템플릿으로 CSV 내용 보내는 코드 추가 : def result()
# 4. 사용자 입력, FAQ 매칭, 부정/긍정/중립 비율, 만족도 점수를 웹페이지에 반영
# 5. 도표로 나타내기 위해서 CSV파일을 각각 생성하였음
# 6. 모델에서 predict 함수에 대한 summary가 필요함
# 7. 모델에서 predict 함수에서 np.argmax(logits) 값이 필요함


## 챗봇 소개
변경 내용 없음

## 처음으로
변경 내용 없음

## FAQ 재질문 처리(스킬 : FAQ재질문) - 폴백블록
predict 함수에서 np.argmax(logits) 값을 가져와야지 csv파일에 저장 가능 --> 코드를 추가해야됨
# emotion = predict 함수에서 np.argmax(logits)반환 값

모델에서
if문으로 np.argmax(logits)을 분류 했기 때문에 비슷한 방식으로 분류함 --> emotion_value에 '긍정'/'부정'/'중립' 저장

CSV에 파일에는 해당 부분에 count + 1을 하도록 구현

추가로 summary 값을 가져와야지 FAQ 답변 처리에서 반영이 가능함
# "extra": {'request_True': "예", 'user_reply': _string, "FAQ": answer, 'summary': summary}


## FAQ 답변 처리(스킬 : FAQ 재질문 처리)
summary 변수 처리 해야됨
# requestion1 = faq_data['summary'][result_loc] + '에 관한 질문이신가요?'
# --> summary 부분이 반환되어야 함
# summary = body['action']['clientExtra']['summary']

사용자 질문을 voc.csv에 저장하는 코드 추가
매칭된 FAQ 목록에 count하는 코드 추가

## FAQ 자세한 답변
변경내용 없음

## 만족도 조사를 위한 block
변경내용 없음

## 별점을 입력하기 위한 block
고객만족도 점수 CSV에 저장하는 코드 추가

## csv파일을 웹페이지에 반영
부정/긍정/중립 dataframe을 리스트로 변환후 emotions=temp_table로 html로 전달
고객만족도 점수 dataframe을 리스트로 변환후 results=temp_table2로 html로 전달
FAQ 매칭현황 dataframe을 리스트로 변환후 faq_results=temp_table3로 html로 전달
사용자 질문 내용을 가져오기는 vocs=temp_table4로 html로 전달
