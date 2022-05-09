#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
import model

# import 모델.py

##변경된 내용##
# 1.자주하는 질문 목록 -> 삭제
# 2.block id 개선
# 3.FAQ 재질문 처리에서 사용자의 감정 분석 및 재질문 처리 -> FAQ 답변 처리에 답변을 넘김
# 4.FAQ 재질문 처리에서 온 정보를 카드 형식으로 나타냄(3개에서 1개로 바꿈 -> 유사도 이슈로)
# 5.단위 테스트를 위한 홈페이지 제작은 아직 미완성
# 6.모델에 챗봇 api를 올리기 위해서는 import 부분을 수정하면 됨
# 7.추가로 핵십문장(requestion1 = faq_data['summary'][result_loc] + '에 관한 질문이신가요?')처리에서 summary 부분을 추출하여
# FAQ 제목으로 쓰려고 함.

app = Flask(__name__)
# 챗봇 intro, 처음으로 이동, FAQ 재질문 처리, FAQ 답변 처리, FAQ 자세히 보기, 만족도조사, 별점나타내기
blockIds = ['6267872745b5fc3106449eb5', '6267b76716b99e0c3380399f', '6267d76116b99e0c33803b71',
            '627802629ac8ed7844162015', '62698aa99ac8ed7844158e2c', '626a23e116b99e0c3380681a',
            '626a241004a7d7314aeaa547']

# Sub 블록아이디
# blockIds = ['6243fdda43ba6c4de14f4034', '', '6262039504a7d7314aea1461', '62679f5045b5fc310644a6a7',
#             '6267872745b5fc3106449eb5', '6267b76716b99e0c3380399f', '6267d76116b99e0c33803b71',
#             '62698aa99ac8ed7844158e2c', '626a23e116b99e0c3380681a', '626a241004a7d7314aeaa547']

total_score = 0
count = 0


# 챗봇 소개
@app.route('/api/introBot', methods=['POST'])
def introBot():
    body = request.get_json()
    print(body)

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
    print(body)

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


# FAQ 재질문 처리
@app.route('/api/FAQ_reply', methods=['POST'])
def FAQ_reply():
    body = request.get_json()  # 봇 시스템 요청 body(SkillPayload)
    _string = body['userRequest']['utterance']
    print(body)  # SkillPayload 출력
    sentiment_result = model.sentiment(_string)  # 재질문 처리
    requestion, answer = model.faq(_string)  # FAQ 내용
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
                    # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                },
                {
                    "messageText": "아니오",
                    "action": "block",
                    "blockId": blockIds[3],  # 재질문 블록으로
                    "label": "아니오",
                    "extra": {'request_True': "아니요", 'user_reply': _string, "FAQ": answer}
                    # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)

                }
            ]
        }
    }

    return responseBody


# FAQ 답변 처리
@app.route('/api/request_answer', methods=['POST'])
def request_answer():
    body = request.get_json()
    print(body)
    responseBody = {}
    request_True = body['action']['clientExtra']['request_True']  # 예 or 아니오
    user_reply = body['action']['clientExtra']['user_reply']  # 사용자 입력
    FAQ = body['action']['clientExtra']['FAQ']  # FAQ 답변 내용
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
    elif request_True == "예":
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
                            "title": "summary",
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
                        "blockId": blockIds[6]
                    }
                ]
            }
        }
    return responseBody


# FAQ 자세한 답변
@app.route('/api/FAQ_result', methods=['POST'])
def FAQ_result():
    body = request.get_json()  # 봇 시스템 요청 body (SkillPayload)
    print(body)  # SkillPayload출력
    blockId = body['userRequest']['block']['id']  # block id
    print(blockId)
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
    print(body)  # SkillPayload출력

    blockId = body['userRequest']['block']['id']  # block id
    print(blockId)

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
    print(body)  # SkillPayload출력

    blockId = body['userRequest']['block']['id']  # block id
    print(blockId)

    score = body['action']['clientExtra']['score']  # 만족도 조사에서 입력된 점수(int형)
    count += 1  # 횟수 추가
    total_score = (total_score + score) / count  # 평균 별점
    print(total_score)
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
    print(body)
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


if __name__ == '__main__':
    # debug mode : 운영 환경에서는 절대 사용X
    app.run(host='0.0.0.0', port=8000)
