import hmac
import hashlib

def OCRA(key, data):
  h=hmac.new(bytes(key, 'utf-8'), data, hashlib.sha256).hexdigest()
  return int(h, 16) % 10000