#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import model
import csv
import pandas as pd

# import 모델.py

##변경된 내용##
# 1. 별점, 사용자 문의 CSV 저장 코드 추가
# 2. 테스트 템플릿 화면(index.html) 추가
# 3. 템플릿으로 CSV 내용 보내는 코드 추가 : def result()
# 4. 사용자 입력, FAQ 매칭, 부정/긍정/중립 비율, 만족도 점수를 웹페이지에 반영
# 5. 도표로 나타내기 위해서 CSV파일을 각각 생성하였음
# 6. 모델에서 predict 함수에 대한 summary가 필요함
# 7. 모델에서 predict 함수에서 np.argmax(logits) 값이 필요함

app = Flask(__name__)
# 챗봇 intro, 처음으로 이동, FAQ 재질문 처리, FAQ 답변 처리, FAQ 자세히 보기, 만족도조사, 별점나타내기
blockIds = ['6267872745b5fc3106449eb5', '6267b76716b99e0c3380399f', '6267d76116b99e0c33803b71',
            '627802629ac8ed7844162015', '62698aa99ac8ed7844158e2c', '626a23e116b99e0c3380681a',
            '626a241004a7d7314aeaa547']

# Sub 블록아이디
# blockIds = ['626a23e116b99e0c3380681c','627a68ea9ac8ed7844165962', '627a690a04a7d7314aeb7235',
#             '627a69269ac8ed7844165966','627a694604a7d7314aeb7238', '626a3b5e04a7d7314aeaab36',
#             '626a3b7545b5fc310644de6a']

total_score = 0
count = 0


# 별점 CSV 파일(rating.csv) 초기화 - 처음 환경 세팅 시에만 사용, 이후에는 주석 처리하여 사용
# df1 = pd.DataFrame({'rating' : [1, 2, 3, 4, 5], 'count' : [0, 0, 0, 0, 0]})
# df1.to_csv('rating.csv')

# 사용자 문의 CSV 파일(voc.csv) 초기화 - 처음 환경 세팅 시에만 사용, 이후에는 주석 처리해서 사용
# df2 = pd.DataFrame({'키워드' : [], '실제질문' : []})
# df2.to_csv('voc.csv')

# 챗봇 소개
@app.route('/api/introBot', methods=['POST'])
def introBot():
    body = request.get_json()
    # print(body)

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕하세요. 고객님!\nLG U+ 챗봇에 오신것을 환영합니다!\n""무엇을 도와드릴까요?\nLG U+ 챗봇이 도와드립니다~"
                    }
                }
            ]
        }
    }
    return responseBody


# 처음으로
@app.route('/api/botStart', methods=['POST'])
def botStart():
    body = request.get_json()
    # print(body)

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "무엇을 도와드릴까요?\n무엇이든 말씀만 해주세요!\nLG U+ 챗봇이 도와드립니다~"
                    }
                }
            ],
        }
    }
    return responseBody


# FAQ 재질문 처리(스킬 : FAQ재질문) - 폴백블록
@app.route('/api/FAQ_reply', methods=['POST'])
def FAQ_reply():
    body = request.get_json()  # 봇 시스템 요청 body(SkillPayload)
    _string = body['userRequest']['utterance']
    # print(body)  # SkillPayload 출력
    sentiment_result = model.sentiment(_string)  # 재질문 처리
    requestion, answer = model.faq(_string)  # FAQ 내용

    # emotion = predict 함수에서 np.argmax(logits)반환 값
    emotion_value = None
    # predict 함수에서 np.argmax(logits) 값을 가져와야지 csv파일에 저장 가능

    # summary = requestion1 = faq_data['summary'][result_loc] + '에 관한 질문이신가요?' 에서 반환된 summary
    # predict 함수에서 requestion1 = faq_data['summary'][result_loc] + '에 관한 질문이신가요?' 해당하는 summary

    # if emotion == 0:
    #     emotion_value = '긍정'
    # elif emotion == 1:
    #     emotion_value = '중립'
    # elif emotion == 2:
    #     emotion_value = '부정'

    # # TODO : CSV 저장(코드 혹은 함수호출)
    # df1 = pd.read_csv('emotion_rating.csv')
    # df1.loc[df1['emotion'] == emotion_value, 'count'] += 1
    # df1.to_csv('emotion_rating.csv', index=False)

    # 예시용 매칭된 FAQ 답변
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": sentiment_result + "\n고객님 " + requestion
                    }
                }
            ],
            "quickReplies": [
                {
                    "messageText": "예",
                    "action": "block",
                    "blockId": blockIds[3],  # 답변 블록으로
                    "label": "예",
                    "extra": {'request_True': "예", 'user_reply': _string, "FAQ": answer}
                    # "extra": {'request_True': "예", 'user_reply': _string, "FAQ": answer, 'summary': summary}
                    # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                },
                {
                    "messageText": "아니오",
                    "action": "block",
                    "blockId": blockIds[3],  # 재질문 블록으로
                    "label": "아니오",
                    "extra": {'request_True': "아니요", 'user_reply': _string, "FAQ": answer}
                    # "extra": {'request_True': "예", 'user_reply': _string, "FAQ": answer, 'summary': summary}
                    # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)

                }
            ]
        }
    }

    return responseBody


# FAQ 답변 처리(스킬 : FAQ 재질문 처리)
@app.route('/api/request_answer', methods=['POST'])
def request_answer():
    body = request.get_json()
    # print(body)
    responseBody = {}
    request_True = body['action']['clientExtra']['request_True']  # 예 or 아니오
    user_reply = body['action']['clientExtra']['user_reply']  # 사용자 입력
    FAQ = body['action']['clientExtra']['FAQ']  # FAQ 답변 내용
    summary = '추가'
    # summary = body['action']['clientExtra']['summary']

    # requestion1 = faq_data['summary'][result_loc] + '에 관한 질문이신가요?'
    # --> summary 부분이 필요함

    if request_True == "아니요":
        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "죄송합니다 고객님 궁금하신 내용을 구체적으로 질문해 주시면\n더 정확한 답을 찾아볼게요~"
                        }
                    }
                ]
            }
        }
    elif request_True == "예":  # 여기에서 문의 내용 관련 기록 (CSV에 저장) : 키워드(summary), 실제질문(user_reply)

        # 사용자 질문을 voc.csv에 저장
        # TODO : CSV 저장(코드 혹은 함수호출)
        df2 = pd.read_csv('voc.csv')
        df2 = df2.append({'키워드': 'summary', '실제질문': user_reply}, ignore_index=True)  # summary(키워드) 받아오는 부분 구현 필요
        df2.to_csv('voc.csv', index=False)

        # 매칭된 FAQ 목록에 count
        # # TODO : CSV 저장(코드 혹은 함수호출)
        # df3 = pd.read_csv('faq_rating.csv')
        # df3.loc[df3['summary'] == summary, 'count'] += 1
        # df3.to_csv('faq_rating.csv', index=False)

        responseBody = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "문의하신 \"" + user_reply + "\" 에 대한 FAQ 답변입니다."
                        }
                    },
                    {
                        "basicCard": {
                            "title": summary,
                            "description": FAQ,
                            "thumbnail": {
                                "imageUrl": "https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fb7nRkz%2FbtqJDXMMc4B%2FqnBpNTJJMeE4P1tZL8PpDK%2Fimg.png"
                            },
                            "buttons": [
                                {
                                    "label": "자세히 보기",
                                    "messageText": "자세히 보기",
                                    "action": "block",
                                    "blockId": blockIds[4],
                                    "extra": {"description": FAQ}
                                },
                                {
                                    "action": "webLink",
                                    "label": "홈페이지로 이동",
                                    "webLinkUrl": "https://www.uplus.co.kr/css/orub/erms/FaqList.hpi"
                                }
                            ]
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "label": "처음으로",
                        "messageText": "처음으로",
                        "action": "block",
                        "blockId": blockIds[1]
                    },
                    {
                        "label": "만족도 조사",
                        "messageText": "만족도 조사",
                        "action": "block",
                        "blockId": blockIds[5]  # 수정
                        # "blockId": blockIds[6]
                    }
                ]
            }
        }
    return responseBody


# FAQ 자세한 답변
@app.route('/api/FAQ_result', methods=['POST'])
def FAQ_result():
    body = request.get_json()  # 봇 시스템 요청 body (SkillPayload)
    # print(body)  # SkillPayload출력
    # blockId = body['userRequest']['block']['id']  # block id
    # print(blockId)
    descriptor = body['action']['clientExtra']['description']  # FAQ 답변에서 extra로 가져온 FAQ 본문

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": descriptor
                    }
                }
            ],
            "quickReplies": [
                {
                    "label": "처음으로",
                    "messageText": "처음으로",
                    "action": "block",
                    "blockId": blockIds[1]
                },
                {
                    "label": "만족도 조사",
                    "messageText": "만족도 조사",
                    "action": "block",
                    "blockId": blockIds[5]
                }
            ]
        }
    }
    return responseBody


# 만족도 조사를 위한 block
@app.route('/api/CSAT', methods=['POST'])
def CSAT():
    body = request.get_json()  # 봇 시스템 요청 body (SkillPayload)
    # print(body)  # SkillPayload출력

    # blockId = body['userRequest']['block']['id']  # block id
    # print(blockId)

    _string = body['userRequest']['utterance']  # 사용자 발화
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "다음 보기중에 골라주세요!"
                    }
                }
            ],
            # 바로가기 버튼
            "quickReplies": [
                {
                    "messageText": "5점",
                    "action": "block",
                    "blockId": blockIds[6],
                    "label": "5점",
                    "extra": {"score": 5}  # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                },
                {
                    "messageText": "4점",
                    "action": "block",
                    "blockId": blockIds[6],
                    "label": "4점",
                    "extra": {"score": 4}  # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                },
                {
                    "messageText": "3점",
                    "action": "block",
                    "blockId": blockIds[6],
                    "label": "3점",
                    "extra": {"score": 3}  # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                },
                {
                    "messageText": "2점",
                    "action": "block",
                    "blockId": blockIds[6],
                    "label": "2점",
                    "extra": {"score": 2}  # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                },
                {
                    "messageText": "1점",
                    "action": "block",
                    "blockId": blockIds[6],
                    "label": "1점",
                    "extra": {"score": 1}  # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                },
                {
                    "messageText": "0점",
                    "action": "block",
                    "blockId": blockIds[6],
                    "label": "0점",
                    "extra": {"score": 0}  # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                }
            ]
        }
    }
    return responseBody


# 별점을 입력하기 위한 block
@app.route('/api/CSAT_result', methods=['POST'])
def CSAT_result():
    global total_score, count
    body = request.get_json()  # 봇 시스템 요청 body (SkillPayload)
    # print(body)  # SkillPayload출력
    #
    # blockId = body['userRequest']['block']['id']  # block id
    # print(blockId)

    score = body['action']['clientExtra']['score']  # 만족도 조사에서 입력된 점수(int형)
    # print(score)
    count += 1  # 횟수 추가
    total_score = (total_score * (count - 1) + score) / count  # 평균 별점

    # 고객만족도 점수 CSV에 저장
    # TODO : CSV 저장(코드 혹은 함수호출)
    df4 = pd.read_csv('score_rating.csv')
    df4.loc[df4['rating'] == score, 'count'] += 1
    df4.to_csv('rating.csv', index=False)

    # print(total_score)
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": str(score) + "점이 입력되었습니다.\n감사합니다."
                    }
                }
            ],
            "quickReplies": [
                {
                    "label": "처음으로",
                    "messageText": "처음으로",
                    "action": "block",
                    "blockId": blockIds[1]
                }
            ]
        }
    }
    return responseBody


# 블록 ID 확인 (각 블록에서 해당 스킬을 호출하면 블록ID 확인 가능!)
@app.route('/api/blockId', methods=['POST'])
def blockId():
    body = request.get_json()
    # print(body)
    # userRequest = body.userRequest
    # blockId = body.block.id
    blockId = body['userRequest']['block']['id']

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "블록ID 입니다",
                        "description": blockId
                    }
                }
            ]
        }
    }
    return responseBody


@app.route("/")
def index():
    return '<HTML><BODY><H1>hello world</H1></BODY></HTML>'


# csv파일을 웹페이지에 반영
@app.route('/result')
def result():
    temp_table4 = []
    
    # 부정/긍정/중립 dataframe을 리스트로 변환
    CSV1 = pd.read_csv('emotion_rating.csv', names=['index', 'rating', 'count'], encoding='CP949')
    CSV1 = CSV1.drop(0)
    emotion_count = CSV1['count']
    emotion_count_value = emotion_count.values
    temp_table = emotion_count_value.tolist()
    temp_table = list(map(int, temp_table))

    # 고객만족도 점수 dataframe을 리스트로 변환
    CSV2 = pd.read_csv('score_rating.csv', names=['index', 'rating', 'count'], encoding='CP949')
    CSV2 = CSV2.drop(0)
    score_count_num = CSV2['count']
    score_count_value = score_count_num.values
    temp_table2 = score_count_value.tolist()
    temp_table2 = list(map(int, temp_table2))

    # FAQ 매칭현황 dataframe을 리스트로 변환
    CSV3 = pd.read_csv('faq_rating.csv', names=['index', 'rating', 'count'], encoding='CP949')
    CSV3 = CSV3.drop(0)
    faq_count_num = CSV3['count']
    faq_count_value = faq_count_num.values
    temp_table3 = faq_count_value.tolist()
    temp_table3 = list(map(int, temp_table3))
    
    # 사용자 질문 내용을 가져오기
    with open('voc.csv', 'r', encoding="UTF-8") as fi:
        mydata = csv.reader(fi)
        for row in mydata:
            temp_table4.append(item for item in row)

    return render_template('index.html', emotions=temp_table, results=temp_table2,
                           faq_results=temp_table3, vocs=temp_table4)


if __name__ == '__main__':
    # debug mode : 운영 환경에서는 절대 사용X
    app.run(host='0.0.0.0', port=8000)
    # app.run(host='0.0.0.0', port=5000)
