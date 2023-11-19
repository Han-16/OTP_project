import hashlib
import hmac

key = input("key : ")
subject = input("제목 : ")
content = input("내용 : ")
my_hmac = hmac.new(bytes(key, 'utf-8'), f"{subject}{content}".encode('utf-8'), hashlib.sha256).hexdigest()
print(f"mac : {my_hmac}")


