#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask, request

##추가된 내용##
# 1.자주하는 질문 목록 -> SMS만 구현
# 2.FAQ답변이 76글자수로 제한 되어 있어 FAQ를 자세히 설명하는 block을 만듬
# 3.만족도 조사 -> 별점 나타내기로 연결
# 4.별점 나타내기에서는 입력된 점수를 보여주고 감사합니다로 마무리

app = Flask(__name__)
# FAQ답변, 단순이미지, 챗봇호출, 블록아이디, 챗봇소개, 메인메뉴, 자주하는 질문, FAQ자세히, 만족도조사, 별점나타내기
blockIds = ['6243fdda43ba6c4de14f4034', '', '6262039504a7d7314aea1461', '62679f5045b5fc310644a6a7',
            '6267872745b5fc3106449eb5', '6267b76716b99e0c3380399f', '6267d76116b99e0c33803b71',
            '62698aa99ac8ed7844158e2c', '626a23e116b99e0c3380681a', '626a241004a7d7314aeaa547']

# 감정표현
test_eval = [
    "대단히 죄송합니다.",  # 공포
    "서비스 사용에 불편을 드려 죄송합니다.",  # 놀람
    "대단히 죄송합니다.",  # 분노
    "LGU+ 서비스를 이용해주셔서 감사합니다.",  # 슬픔
    "LGU+ 서비스를 이용해주셔서 감사합니다.",  # 중립
    "이용해주셔서 감사합니다.",  # 행복
    "대단히 죄송합니다.",  # 혐오
]

# FAQ 답변
answer_list = [
    '기업메시징 서비스에서 제공되는 SMS는 80byte로 규정되어 있습니다. 140byte의 경우 휴대폰에서 휴대폰으로 전송하는 개인 문자 서비스일 경우에만 지원되며, 기업메시징 서비스는 80byte까지 지원합니다. 이통사 또는 단말기에 따라 최대 90byte까지 수신되는 경우가 있으나, 공식적으로는 80byte까지만 지원되므로 서비스 이용에 참고하여 주시기 바랍니다.',
    'U+ SMS 에서는 해킹/제3자 도용의 피해를 막기 위해 ID별로 로그인시 인증문자를 수신받을 사람의 휴대폰번호를 사전 등록하도록 하고 있습니다. 따라서 SMS인증창에서 본인의 휴대폰번호를 입력하였으나 인증 대상자가 아니라고 표시될 경우 먼저 본인의 휴대폰번호가 웹이용자로 등록되어 있는지 해당 ID의 서비스담당자에게 확인하여 주시기 바랍니다. (서비스 담당자는 ID관리자로서, 1544-5992(메시징고객센터)로 연락하시면 확인 가능합니다) 웹이용자로 등록되어 있을 경우에도 SMS인증 대상자가 아니라고  표시될 경우, 아래 내용으로 조치를 시도해 주십시오. [조치내용] 1. 인터넷브라우저>도구>인터넷옵션점검>일반Tab에서 검색기록을 삭제합니다. (검색기록 삭제 시 본서비스 웹사이포함 모든 로그인 요하는 웹사이트에 아이디저장 체크하였던 내용 삭제되므로 유의하여 주시기 바랍니다. ) 2. 인터넷브라우저>도구>인터넷옵션>고급Tab에서 Internet Explorer 기본설정복구 원래대로 버튼(또는 고급설정 복원 버튼)을 클릭하여 브라우저를 초기화합니다. 3. Internet Explorer 재실행 후 도구>팝업차단설정 해제 후 사용합니다. 위 조치내용으로 처리 시 대부분 정상 로그인 가능하지만, 조치 이후에도 동일 할 경우에는 PC 개별 문제가 대부분으로 PC A/S가 필요 할 수 있습니다.',
    '이통사나 단말기에서 스팸차단이 될 경우 질문과 같은 상황이 발생할 수 있습니다. <수신차단 사유> 1.이통사 스팸 차단 정책으로 인한 미수신(특정 단어, 발신번호 등) 2. 고객 단말기 설정 (스팸단어,스팸번호,스팸차단)으로 인한 미수신 3. 이통사에서 제공하는 스팸필터링 서비스 신청으로 인한 미수신 -스팸필터링의 경우는 이통사에서 제공하는 스팸필터링 부가서비스에 신청된 경우 고객 휴대폰에 메시지는 정상수신된것으로 간주하나, 실제로 고객단말에 전송이 되지 않습니다. 차단된 문자를 확인 하시려면 수신자 본인이 단말기 및 이동통신사 홈페이지에서 확인해 주셔야 합니다. (문자 확인과 같이 개인정보관련 내용은 본인 이외 타인은 조회할 수 없으므로, 수신자 본인이 직접 확인하셔야 합니다.)  본인에게 수신된 스팸메시지 확인 방법은 아래와 같습니다. [SKT 가입자] 홈페이지: Tworld→부가서비스→통화→통화필터링→스팸필터링→스팸내역조회 단말기: T스팸필터링 앱→스팸리스트  [KT 가입자] 홈페이지: olleh.com→상품→모바일→통화→사생활보호→스팸차단서비스 단말기: olleh버튼(구 핸드폰은 SHOW / 매직엔) > 고객센터 > 부가서비스 > 사생활 > 스팸차단  [LG U+ 가입자] 홈페이지: 개인→모바일→부가서비스→통화보호→스팸차단→스팸내역조회 메시징고객센터로 수신불가 관련 문의접수시 아래의 프로세스에 따라 처리됩니다.  1. 당사 시스템에서 이통사로 정상 발송여부 확인(실시간) 2. 당사 시스템에서 정상 발송되었고, 이통사로 부터 받은 결과가 [정상]인 경우 이통사에 수신 불가 사유 요청 3. 이통사에서 결과가 수신될 때까지 기다림(30분 ~ 3일) 4. 이통사로부터 결과 수신시 고객에게 수신차단 사유 전달',
    '이통사 문자함에서 제공되지 않는 규격입니다.',
    '하나의 ID를 여러 명이 사용하는 경우가 많으므로 고객님의 편의를 위해 비밀번호 변경 문자알림 서비스를 실시하고 있습니다. 비밀번호 변경시, 해당 ID에 등록된 웹이용자의 휴대폰번호로 비밀번호를 변경한 사람의 휴대폰번호 및 변경일시를 알려드립니다.',
    '인증문자 수신자는 여러 명 등록이 가능합니다.',
    '결제방식(선불/후불)에 따라 다른 아이디 체계로 운영되고 있으므로 선불/후불 변경을 위해서는 신규 가입 신청을 해 주셔야 합니다.',
    '문자발송 후 전송중 또는 대기인 건의 유형은 아래와 같습니다.',
    'U+ SMS에서는 080수신거부 서비스를 제공하고 있지 않습니다.',
    '서버에서 메시지 발송이 되지 않을 경우. 아래 사항을 확인 및 점검하여 주십시오. 1. 클라이언트와 U+ SMS 서버 접속 상태 확인, 2. DB 접속관련 확인사항, 3. 위의 사항이 모두 문제 없을 경우 발송테이블에 상태값을 확인',
    'SMS 서버를 이전하실 경우, 아래와 같은 사항을 확인 및 점검하셔야 합니다. 1. 발송모듈 이전시 확인 사항 - 방화벽 확인, JAVA 1.5 version 이상 설치 유무 확인, 2. DB 이전시 확인 사항 - 방화벽 확인, 발송모듈의 config에 변경할 DB정보 setting 후 모듈 재기동',
    '이통사나 단말기에서 스팸차단이 될 경우 질문과 같은 상황이 발생할 수 있습니다.<수신차단 사유> 1. 이통사 스팸단어 차단 정책으로 인한 미수신 2. 고객 단말기 설정 (스팸단어,스팸번호,스팸차단)으로 인한 미수신 3. 이통사의 스팸필터링 서비스 신청으로 인한 미수신',
    '아닙니다. 중복된 번호가 있어도 중복체크를 선택해주시면, 전송전에 중복체크를 하여 하나의 번호에 1개의 메시지만 전송됩니다. 현재 중복체크 기능은 기본적으로 체크되어 있습니다.',
    '메일머지란, 메시지에 일정한 내용을 추가할 수 있는 기능으로 주소록 그룹을 선택한 경우에만 사용할 수 있습니다.',
    'MMS란 Multimedia Message Service의 약자로 90Byte(한글45자내외)로 한정되어있던 SMS와 달리 1000자의 텍스트, 이미지, 사운드, 동영상을 첨부해 보내는 멀티미디어 문자 메시지 서비스 입니다.',
    '메시지 전송 메뉴에서 SMS 전송창에는 2개의 창으로 구성되어 있어서, 메시지 내용이 길어질 경우(90Byte 초과시) 아래창에 연속적으로 쓸 수 있도록 되어 있습니다.',
    'MMS는 SMS와 같이 메시지를 받는 분께는 비용이 청구되지 않습니다.',
    '회원가입은 온라인 서비스 신청과 오프라인 서비스 신청방식이 있습니다. 온라인 가입시에는 [서비스 신청]에서 회원가입 약관/스팸동의서/개인정보취급방침을 확인하시고 서비스 신청항목을 선택후, 가입하시면 됩니다. 서비스 신청 완료후 사업자등록증 사본과 대표자 신분증사본을 팩스로 LG U+ SMS 고객센터로 보내주시면 됩니다.(FAX번호: 02-6919-1000)',
]

# FAQ 목록
faq_list = [
    ['SMS는 몇 byte까지 지원되나요?', answer_list[0]],
    ['SMS byte', answer_list[0]],
    ['SMS 바이트', answer_list[0]],
    ['SMS 담당', answer_list[1]],
    ['SMS 담당자', answer_list[1]],
    ['웹사이트 로그인시 SMS인증 담당자가 아니라고 합니다', answer_list[1]],
    ['전송결과는 성공인데 수신자가 문자를 받지 못했다고 합니다', answer_list[2]],
    ['MMS이미지를 클릭시 웹페이지로 이동하는 기능이 제공되나요?', answer_list[3]],
    ['MMS 웹페이지', answer_list[3]],
    ['비밀번호가 변경되었다는 문자가 옵니다', answer_list[4]],
    ['비밀번호', answer_list[4]],
    ['비밀번호변경', answer_list[4]],
    ['인증문자 수신자는 1명밖에 등록할 수 없나요?', answer_list[5]],
    ['후불→선불로(또는 선불→후불로) 변경하고 싶어요', answer_list[6]],
    ['전송중 또는 대기인 건은 어떤 경우에 발생하나요?', answer_list[7]],
    ['전송중', answer_list[7]],
    ['대기', answer_list[7]],
    ['080수신거부 서비스를 제공하나요?', answer_list[8]],
    ['080수신거부', answer_list[8]],
    ['수신거부', answer_list[8]],
    ['서버에서 메시지가 발송되지 않습니다', answer_list[9]],
    ['SMS 서버를 이전할 경우 어떻게 해야 하나요?', answer_list[10]],
    ['SMS 서버 이전', answer_list[10]],
    ['발송결과는 성공인데 수신자가 문자를 못받았다고 합니다.', answer_list[11]],
    ['발송결과 성공 수신자 문자', answer_list[11]],
    ['중복된 번호가 있을경우 2건으로 전송되나요?', answer_list[12]],
    ['중복된 번호', answer_list[12]],
    ['중복 번호', answer_list[12]],
    ['메일머지 기능은 무엇입니까?', answer_list[13]],
    ['MMS(멀티메세지)란 무엇입니까?', answer_list[14]],
    ['MMS 멀티메세지', answer_list[14]],
    ['MMS', answer_list[14]],
    ['SMS를 1건으로 보내기 어려운데 좋은 방법이 있나요?', answer_list[15]],
    ['MMS를 받는 사람도 비용이 드나요?', answer_list[16]],
    ['MMS 비용', answer_list[16]],
    ['회원 가입(서비스신청)은 어떻게 하나요?', answer_list[17]],
    ['회원 가입 어떻게 해요?', answer_list[17]],
    ['회원 가입 방법', answer_list[17]],
    ['서비스 신청', answer_list[17]],
    ['회원 가입', answer_list[17]],
    ['회원가입', answer_list[17]],
]

total_score, count = 0, 0


# 예시용 FAQ 답변 매칭
def find_faq(utterance, title, descriptor):
    faq_list_example = ["SMS", "문자", "MMS", "비밀번호", "인증문자", "후불", "선불", "전송중", "수신거부", "서버", "SMS 서버"]
    if faq_list_example[0] in utterance:
        title.append(faq_list[0][0])
        descriptor.append(answer_list[0])
        title.append(faq_list[1][0])
        descriptor.append(answer_list[1])
        title.append(faq_list[3][0])
        descriptor.append(answer_list[2])


# 메인 메뉴
@app.route('/api/mainMenu', methods=['POST'])
def mainMenu():
    body = request.get_json()
    print(body)

    blockId = body['userRequest']['block']['id']
    print(blockId)

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
            # "quickReplies": [
            #     {
            #         "messageText": "제품 검색",
            #         "action": "block",
            #         "blockId": blockIds[5],
            #         "label": "제품 검색"
            #     },
            #     {
            #         "messageText": "제품 추천",
            #         "action": "block",
            #         "blockId": blockIds[4],
            #         "label": "제품 추천"
            #     },
            #     {
            #         "messageText": "이벤트 안내",
            #         "action": "block",
            #         "blockId": blockIds[4],
            #         "label": "이벤트 안내"
            #     },
            #     {
            #         "messageText": "자주하는 질문",
            #         "action": "block",
            #         "blockId": blockIds[4],
            #         "label": "자주하는 질문"
            #     }
            #
            # ]
        }
    }
    return responseBody


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
                        "text": "안녕하세요. 고객님!\nLG U+ 챗봇 서비스에 오신것을 환영합니다!\n아래의 보기에서 선택해 주세요!."
                    }
                }
            ],
            "quickReplies": [
                {
                    "label": "이용하기",
                    "messageText": "이용하기",
                    "action": "block",
                    "blockId": blockIds[5]
                },
                {
                    "label": "자주하는 질문",
                    "messageText": "자주하는 질문",
                    "action": "block",
                    "blockId": blockIds[6]
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


# 챗봇 호출 응답
@app.route('/api/callBot', methods=['POST'])
def callBot():
    body = request.get_json()
    print(body)

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕하세요! 365일 늘 새로운 LG U+입니다. 우선 제 소개를 잠깐 드려도 될까요? 아주 잠깐이면 됩니다!"
                    }

                }
            ],
            "quickReplies": [
                {
                    "messageText": "좋아!",
                    "action": "block",
                    "blockId": blockIds[4],  # 챗봇 소개 블록 이동
                    "label": "좋아!"
                },
                {
                    "messageText": "싫어!",
                    "action": "block",
                    "blockId": blockIds[5],  # 메인 메뉴 블록 이동
                    "label": "싫어!"
                }
            ]
        }
    }
    return responseBody


# 테스트 API
# 카카오톡 이미지형 응답
@app.route('/api/showHello', methods=['POST'])
def showHello():
    body = request.get_json()  # 봇 시스템 요청 body (SkillPayload)
    print(body)  # SkillPayload출력

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleImage": {
                        "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                        "altText": "hello I'm Ryan"
                    }
                }
            ]
        }
    }
    return responseBody


# 카카오톡 FAQ 응답
@app.route('/api/sayHello', methods=['POST'])
def sayHello():
    body = request.get_json()  # 봇 시스템 요청 body(SkillPayload)
    _string = body['userRequest']['utterance']
    print(body)  # SkillPayload 출력

    title_List = []
    description_List = []

    # 예시용 매칭된 FAQ 답변
    find_faq(_string, title_List, description_List)
    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "입력하신 내용에서 \"" + test_eval[1] + "\" 느껴집니다.\n문의하신 \"" + _string + "\" 에 대한 FAQ 답변입니다."
                    }
                },
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "title": title_List[0],  # "FAQ1",
                                "description": description_List[0],  # "FAQ1 해당 내용",
                                "thumbnail": {
                                    "imageUrl": "https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fb7nRkz%2FbtqJDXMMc4B%2FqnBpNTJJMeE4P1tZL8PpDK%2Fimg.png"
                                },
                                "buttons": [
                                    {
                                        "label": "자세히 보기",
                                        "messageText": "자세히 보기",
                                        "action": "block",
                                        "blockId": blockIds[7],
                                        "extra": {"description": description_List[0]}
                                    },
                                    {
                                        "action": "webLink",
                                        "label": "홈페이지로 이동",
                                        "webLinkUrl": "https://www.uplus.co.kr/css/orub/erms/FaqList.hpi"
                                    }
                                ]
                            },
                            {
                                "title": title_List[1],  # "FAQ2",
                                "description": description_List[1],  # "FAQ2 해당 내용",
                                "thumbnail": {
                                    "imageUrl": "https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fb7nRkz%2FbtqJDXMMc4B%2FqnBpNTJJMeE4P1tZL8PpDK%2Fimg.png"
                                },
                                "buttons": [
                                    {
                                        "label": "자세히 보기",
                                        "messageText": "자세히 보기",
                                        "action": "block",
                                        "blockId": blockIds[7],
                                        "extra": {"description": description_List[1]}
                                    },
                                    {
                                        "action": "webLink",
                                        "label": "홈페이지로 이동",
                                        "webLinkUrl": "https://www.uplus.co.kr/css/orub/erms/FaqList.hpi"
                                    }
                                ]
                            },
                            {
                                "title": title_List[2],  # "FAQ3",
                                "description": description_List[2],  # "FAQ3 해당 내용",
                                "thumbnail": {
                                    "imageUrl": "https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fb7nRkz%2FbtqJDXMMc4B%2FqnBpNTJJMeE4P1tZL8PpDK%2Fimg.png"
                                },
                                "buttons": [
                                    {
                                        "label": "자세히 보기",
                                        "messageText": "자세히 보기",
                                        "action": "block",
                                        "blockId": blockIds[7],
                                        "extra": {"description": description_List[2]}
                                    },
                                    {
                                        "action": "webLink",
                                        "label": "홈페이지로 이동",
                                        "webLinkUrl": "https://www.uplus.co.kr/css/orub/erms/FaqList.hpi"
                                    }
                                ]
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
                    "blockId": blockIds[4]
                },
                {
                    "label": "만족도 조사",
                    "messageText": "만족도 조사",
                    "action": "block",
                    "blockId": blockIds[8]
                }
            ]
        }
    }

    return responseBody


# 카카오톡 자주하는 질문 응답
@app.route('/api/showFAQ', methods=['POST'])
def showFAQ():
    body = request.get_json()  # 봇 시스템 요청 body (SkillPayload)
    print(body)  # SkillPayload출력
    # userRequest = body.userRequest
    # blockId = body.block.id
    blockId = body['userRequest']['block']['id']
    print(blockId)

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [

                {
                    "simpleText": {
                        "text": "자주하는 질문 목록입니다."
                    }
                    # "simpleImage": {
                    #     "imageUrl": "https://t1.daumcdn.net/friends/prod/category/M001_friends_ryan2.jpg",
                    #     "altText": "hello I'm Ryan"
                    # }
                }

            ],
            "quickReplies": [
                {
                    "messageText": "SMS",
                    "action": "message",
                    "blockId": blockIds[1],
                    "label": "SMS"
                },
                {
                    "messageText": "FAQ2",
                    "action": "message",
                    # "blockId": blockIds[4],
                    "label": "문자"
                },
                {
                    "messageText": "FAQ3",
                    "action": "message",
                    # "blockId": blockIds[4],
                    "label": "MMS"
                },
                {
                    "messageText": "FAQ4",
                    "action": "message",
                    # "blockId": blockIds[4],
                    "label": "비밀번호"
                },
                {
                    "messageText": "FAQ4",
                    "action": "message",
                    # "blockId": blockIds[4],
                    "label": "인증문자"
                },
                {
                    "messageText": "FAQ4",
                    "action": "message",
                    # "blockId": blockIds[4],
                    "label": "후불"
                },
                {
                    "messageText": "FAQ4",
                    "action": "message",
                    # "blockId": blockIds[4],
                    "label": "선불"
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
    # userRequest = body.userRequest
    # blockId = body.block.id
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
                    "blockId": blockIds[4]
                },
                {
                    "label": "만족도 조사",
                    "messageText": "만족도 조사",
                    "action": "block",
                    "blockId": blockIds[8]
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
                    "blockId": blockIds[9],
                    "label": "5점",
                    "extra": {"score": 5}  # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                },
                {
                    "messageText": "4점",
                    "action": "block",
                    "blockId": blockIds[9],
                    "label": "4점",
                    "extra": {"score": 4}  # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                },
                {
                    "messageText": "3점",
                    "action": "block",
                    "blockId": blockIds[9],
                    "label": "3점",
                    "extra": {"score": 3}  # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                },
                {
                    "messageText": "2점",
                    "action": "block",
                    "blockId": blockIds[9],
                    "label": "2점",
                    "extra": {"score": 2}  # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                },
                {
                    "messageText": "1점",
                    "action": "block",
                    "blockId": blockIds[9],
                    "label": "1점",
                    "extra": {"score": 1}  # 선택한 블록으로 넘어가면서 점수를 전달함 (int형)
                },
                {
                    "messageText": "0점",
                    "action": "block",
                    "blockId": blockIds[9],
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
                    "blockId": blockIds[4]
                }
            ]
        }
    }
    return responseBody


if __name__ == '__main__':
    # debug mode : 운영 환경에서는 절대 사용X
    app.run(host='0.0.0.0', port=5000)
