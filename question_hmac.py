import hmac
import hashlib

subject = input("제목을 입력하세요")
content = input("내용을 입력하세요")
key = input("key를 입력하세요")

my_hmac = hmac.new(key, f"{subject}{content}", hashlib.sha256)
print(f"my_hmac : {my_hmac}")