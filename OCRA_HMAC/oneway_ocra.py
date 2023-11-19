import hmac
import hashlib
from datetime import datetime
#  hmac.new(bytes(key, 'utf-8'),

def OCRA(key, data):
  h=hmac.new(bytes(key, 'utf-8'), data, hashlib.sha256).hexdigest()
  return h

sha256_hash = hashlib.sha256()

k = input("key를 입력하세요 : ")
C = input("서버가 보내준 챌린지 값 : ")
subject = input("제목을 입력하세요 : ")
content = input("내용을 입력하세요 : ")
author = input("작성자를 입력하세요 : ")
date = input("작성날짜를 입력하세요 : ")

msg = f"{subject}{content}{author}{date}"
sha256_hash.update(msg.encode('utf-8'))
m = sha256_hash.hexdigest()

t = datetime.now().strftime("%Y-%m-%d")

pw= input("비밀번호 : ")
p_h = hashlib.sha1(bytes(pw, 'utf-8')).digest()
data=bytes(f'{C}{p_h}{m}{t}','utf8')

R = OCRA(k, data)
print(f"OCRA is : {R}")

