# AI Creative Platform Backend

## 项目结构

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI应用入口
│   ├── config.py               # 配置管理
│   ├── database.py             # 数据库连接
│   ├── models/                 # SQLAlchemy模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── digital_human.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── task.py
│   │   └── digital_human.py
│   ├── routers/                # API路由
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── image.py
│   │   ├── video.py
│   │   ├── size.py
│   │   ├── tryon.py
│   │   └── digital_human.py
│   ├── services/               # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── image_service.py
│   │   ├── video_service.py
│   │   ├── size_service.py
│   │   ├── tryon_service.py
│   │   └── digital_human_service.py
│   ├── workers/                # 异步任务
│   │   ├── __init__.py
│   │   └── tasks.py
│   ├── utils/                  # 工具函数
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── file_utils.py
│   │   └── mediaPipe_utils.py
│   └── dependencies.py         # 依赖注入
├── tests/                      # 测试
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```

## 功能模块

### 1. 通用图片生成
- 输入提示词
- 可选上传参考图
- 调用AI生成图片

### 2. 通用视频生成
- 上传图片（衣服、家电等）
- 选择视频类型：video_clothing_show, video_tryon, video_product_show等
- 生成动态视频

### 3. 尺码推荐
- 上传全身照
- 使用MediaPipe提取特征
- 随机森林模型预测尺码

### 4. 多角度试穿
- 上传多张照片
- 生成统一角色的多角度试穿视频

### 5. 商家数字人定制
- 上传模特视频
- 创建专属数字人
- 试穿视频可选择数字人

## 技术栈
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis + RQ
- JWT认证
- MediaPipe

## 快速启动

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件
```

3. 启动数据库
```bash
docker-compose up -d
```

4. 运行应用
```bash
uvicorn app.main:app --reload
```

5. 运行worker
```bash
python -m app.workers.tasks
```
