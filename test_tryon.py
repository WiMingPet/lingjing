import requests
import jwt
import time

ACCESS_KEY = "ACBD8k4dG8HarmLtY9hFFDACfLnCmGYE"
SECRET_KEY = "rG3JJgbFyRaDK3kyyDmgtMTtMBQgDKye"

# 生成 token
headers = {"alg": "HS256", "typ": "JWT"}
payload = {
    "iss": ACCESS_KEY,
    "exp": int(time.time()) + 1800,
    "nbf": int(time.time()) - 5
}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256", headers=headers)

# 测试图片
model_url = "https://m.media-amazon.com/images/I/71jgn+xibhL._AC_SY550_.jpg"
garment_url = "https://m.media-amazon.com/images/I/61OarLRya0L._AC_SY550_.jpg"

url = "https://api-beijing.klingai.com/v1/images/generations"

# 测试不同的 model_name
models = [
    "kolors-virtual-tryon-v1",
    "kolors-virtual-tryon-v1-5",
    "kling-v1"
]

for model_name in models:
    payload = {
        "model_name": model_name,
        "prompt": "virtual tryon",
        "model_image": model_url,
        "garment_image": garment_url,
        "aspect_ratio": "1:1",
        "n": 1
    }
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    print(f"\n测试模型: {model_name}")
    response = requests.post(url, json=payload, headers=headers)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.text}")




