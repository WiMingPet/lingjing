import requests
import base64
import urllib.request
import tempfile

API_KEY = "oGxCc4qrkiUWJc6JHhnahoLJ3Im1f7So8mvKLM92"

# 下载一张测试图片
url = "https://picsum.photos/id/100/512/512"
with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
    urllib.request.urlretrieve(url, f.name)
    image_path = f.name

# 读取图片并转为 base64
with open(image_path, 'rb') as f:
    img_base64 = base64.b64encode(f.read()).decode('utf-8')

# 调用 API - 使用正确的端点
api_url = "https://api.api-ninjas.com/v1/pose"
headers = {"X-Api-Key": API_KEY}
payload = {"image": img_base64}

print("正在调用 API Ninjas...")
response = requests.post(api_url, json=payload, headers=headers, timeout=30)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text}")



