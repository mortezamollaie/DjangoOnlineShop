from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('424B7266335934664A4176783074516E307A32762F6D6E353335763374523842333051365044464A4A31383D')
        params = {
            'sender': '',  # optional
            'receptor': phone_number,  # multiple mobile number, split by comma
            'message': 'salam',
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
