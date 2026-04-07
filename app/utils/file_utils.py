"""
文件上传工具
"""
import os
import uuid
import shutil
from typing import Dict, Optional
from fastapi import UploadFile
from app.config import settings


async def upload_file_helper(file: UploadFile, folder: str = "uploads") -> Dict:
    """
    上传文件到本地存储
    返回: {"file_id": "xxx", "url": "xxx", "filename": "xxx"}
    """
    try:
        # 创建上传目录
        upload_dir = os.path.join(settings.UPLOAD_DIR, folder)
        os.makedirs(upload_dir, exist_ok=True)
        
        # 生成唯一文件名
        file_ext = os.path.splitext(file.filename)[1]
        file_id = str(uuid.uuid4())
        filename = f"{file_id}{file_ext}"
        file_path = os.path.join(upload_dir, filename)
        
        # 保存文件
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # 返回文件信息
        # 注意：这里返回的是本地路径，生产环境应返回 URL
        return {
            "file_id": file_id,
            "url": f"/uploads/{folder}/{filename}",  # 本地访问路径
            "filename": file.filename,
            "path": file_path
        }
        
    except Exception as e:
        print(f"[ERROR] 文件上传失败: {e}")
        raise Exception(f"文件上传失败: {str(e)}")