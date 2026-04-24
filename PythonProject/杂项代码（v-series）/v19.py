from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

# Base64 解码
ciphertext = base64.b64decode("b2ZuVF1MWlVhcWhldFVTNEJRUWVOV3NtUWlCN2pjM3FneURaVlJJVVFtdlk2V3VUWlA2MzVoNGFkWVl4IQ==")

# 需要您提供正确的密钥（必须与加密时使用的相同）
# 将短密钥重复填充到32字节（临时方案）
key = ("sakuya" * 6)[:32].encode()  # 得到32字节密钥

# 创建解密器（ECB模式示例）
cipher = AES.new(key, AES.MODE_ECB)

# 解密
plaintext = cipher.decrypt(ciphertext)

# 移除填充（如果加密时使用了填充）
try:
    plaintext = unpad(plaintext, AES.block_size)
    print("解密结果:", plaintext.decode('utf-8'))
except ValueError as e:
    print("填充错误:", e)
