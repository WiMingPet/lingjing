import requests
import jwt
import time
from datetime import datetime, timedelta

# ！这里换成你的真实密钥！
ACCESS_KEY = "ACBD8k4dG8HarmLtY9hFFDACfLnCmGYE"
SECRET_KEY = "rG3JJgbFyRaDK3kyyDmgtMTtMBQgDKye"

# 生成 token
headers = {"alg": "HS256", "typ": "JWT"}
payload = {
    "iss": ACCESS_KEY,
    "exp": int(datetime.utcnow().timestamp()) + 1800,
    "nbf": int(datetime.utcnow().timestamp()) - 5
}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256", headers=headers)
print("Token 生成成功")

# 调用 API
url = "https://api-beijing.klingai.com/images/generations"
payload = {
    "model_name": "kling-v1",
    "prompt": "一只猫",
    "aspect_ratio": "1:1",
    "n": 1
}
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

print("正在调用 API...")
response = requests.post(url, json=payload, headers=headers)
print("状态码:", response.status_code)
print("响应:", response.text)