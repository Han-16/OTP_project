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

    key = ""
    totp_obj = generate_totp(key)
    totp_value = totp_obj.now()
    print(type(totp_value))
    print(totp_value)

