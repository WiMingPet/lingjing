import requests
import jwt
import time
import json

ACCESS_KEY = "ACBD8k4dG8HarmLtY9hFFDACfLnCmGYE"
SECRET_KEY = "rG3JJgbFyRaDK3kyyDmgtMTtMBQgDKye"

# 生成 token
header = {"alg": "HS256", "typ": "JWT"}
payload = {
    "iss": ACCESS_KEY,
    "exp": int(time.time()) + 1800,
    "nbf": int(time.time()) - 5
}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256", headers=header)

# 提交任务
url = "https://api-beijing.klingai.com/v1/images/generations"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
data = {
    "model_name": "kling-v1",
    "prompt": "一只可爱的橘猫，4K高清",
    "aspect_ratio": "1:1",
    "n": 1
}

print("提交任务...")
response = requests.post(url, json=data, headers=headers)
result = response.json()
print(f"提交结果: {result}")

if result.get("code") == 0:
    task_id = result["data"]["task_id"]
    print(f"任务ID: {task_id}")
    
    # 轮询结果
    print("等待生成...")
    for i in range(30):  # 最多等待30次
        time.sleep(2)
        status_url = f"https://api-beijing.klingai.com/v1/images/generations/{task_id}"
        status_resp = requests.get(status_url, headers=headers)
        status_data = status_resp.json()
        print(f"状态: {status_data}")
        
        if status_data.get("data", {}).get("task_status") == "succeed":
            images = status_data["data"]["task_result"]["images"]
            print(f"\n成功！图片地址: {images[0]['url']}")
            break
        elif status_data.get("data", {}).get("task_status") == "failed":
            print("生成失败")
            break
else:
    print(f"提交失败: {result}")