import random
# 감정표현
def sentiment(sentence):
    test_eval = []
    num = random.randrange(1, 3)
    if num == 0:
        test_eval.append("이용해주셔서 감사합니다.")  # 긍정
    elif num == 1:
        test_eval.append("LGU+ 서비스를 이용해주셔서 감사합니다.")  # 중립
    elif num == 2:
        test_eval.append("서비스 사용에 불편을 드려 죄송합니다.")  # 부정
    return test_eval[0]

def faq(sentence):
    requestion = "MMS 비용에 관한 질문이신가요?"
    answer = "MMS는 SMS와 같이 메시지를 받는 분께는 비용이 청구되지 않습니다."
    return requestion, answer