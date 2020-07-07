import requests

TARGET_URL = 'https://notify-api.line.me/api/notify'


def send_significant_message_by_line(message, token_list):
    send_message_by_line(message,token_list[0])
    send_message_by_line(message,token_list[1])


def send_message_by_line(message, token='1XAzzNOq8tkrDZE7p7f0HEZDs7GuVpbtjgQfNimWs3M'):
    '''
    LINE Notify를 사용한 메세지 보내기
    :param message: 전달할 메세지
    :return: None
    '''
    try:
        response = requests.post(
            TARGET_URL,
            headers={
                'Authorization': 'Bearer ' + token
            },
            data={
                'message': message
            }
        )
        status = response.json()['status']
        # 전송 실패 체크
        if status != 200:
            # 에러 발생시에만 로깅
            raise Exception('Fail need to check. Status is %s' % status)

    except Exception as e:
        raise Exception(e)


if __name__ == '__main__':
    print('test notifier!')
    # send_significant_message_by_line('message', ['Z6XWYJcsVs07WBt6YSAf2tNHMXAeuib6LOFkt3D176n', 'kjSWThDmohZZmm6Z4LrseIerZNtGx2F2DkVkMNTkUUT'])

