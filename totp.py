import pyotp
import base64
import secrets
import time

def generate_symmetric_key(key_length=64):
    key = secrets.token_hex(key_length)
    return key

def hex_to_base32(hex_key):
    # 16진수 -> 바이너리로 디코딩 -> base32로 인코딩
    binary_key = bytes.fromhex(hex_key)
    base32_key = base64.b32encode(binary_key).decode('utf-8')
    return base32_key

def generate_totp(secret_key):
    totp = pyotp.TOTP(secret_key)
    return totp

def verify_totp(totp, user_input):
    return totp.verify(user_input)

if __name__ == "__main__":
    hex_secret_key = generate_symmetric_key()
    base32_secret_key = hex_to_base32(hex_secret_key)
    print(f"대칭키: {base32_secret_key}")
    totp_obj = generate_totp(base32_secret_key)
    
    while True:
        totp_value = totp_obj.now()
        time_remaining = totp_obj.interval - (time.time() % totp_obj.interval)
        print(f"현재 TOTP: {totp_value}, 남은 시간: {time_remaining:.0f}초")
        
        user_input = input("TOTP를 입력하세요: ")
        
        if verify_totp(totp_obj, user_input):
            print("TOTP가 일치합니다. 인증 성공!")
            break
        else:
            print("TOTP가 일치하지 않습니다. 인증 실패.")
        
        time.sleep(1)
    print("------------------------------------------------------------")
    print("서비스 시작")
    time.sleep(1)
    print(".")
    time.sleep(1)
    print(".")
    time.sleep(1)
    print("서비스 종료")
