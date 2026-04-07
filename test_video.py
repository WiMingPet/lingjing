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

# 测试图片 URL
image_url = "https://picsum.photos/id/104/512/512"

# 提交视频任务
url = "https://api-beijing.klingai.com/v1/videos/image2video"
payload = {
    "model_name": "kling-v2-5-turbo",
    "image": image_url,
    "prompt": "猫在草地上奔跑",
    "duration": "5",
    "mode": "std"
}
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

print("提交视频任务...")
response = requests.post(url, json=payload, headers=headers)
result = response.json()
print(f"提交响应: {result}")

if result.get("code") == 0:
    task_id = result["data"]["task_id"]
    print(f"任务ID: {task_id}")
    
    # 轮询结果
    for i in range(60):
        time.sleep(5)
        status_url = f"https://api-beijing.klingai.com/v1/videos/image2video/{task_id}"
        status_resp = requests.get(status_url, headers=headers)
        status_data = status_resp.json()
        print(f"第{i+1}次查询: {status_data}")
        
        task_status = status_data.get("data", {}).get("task_status")
        
        if task_status == "succeed":
            # 打印完整的返回数据，看看视频URL在哪个字段
            print("\n成功！完整返回数据:")
            print(status_data)
            # 尝试获取视频URL
            task_result = status_data.get("data", {}).get("task_result", {})
            print(f"\ntask_result 内容: {task_result}")
            break
        elif task_status == "failed":
            print("生成失败")
            break
else:
    print(f"提交失败: {result}")


