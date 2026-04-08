"""
阿里云 OSS 服务
用于上传和下载文件
"""
import oss2
import uuid
from typing import Optional
from app.config import settings


class OSSService:
    """OSS 服务类"""
    
    def __init__(self):
        """初始化 OSS 客户端"""
        auth = oss2.Auth(
            settings.OSS_ACCESS_KEY_ID,
            settings.OSS_ACCESS_KEY_SECRET
        )
        self.bucket = oss2.Bucket(
            auth,
            settings.OSS_ENDPOINT,
            settings.OSS_BUCKET_NAME
        )
    
    def _get_content_type(self, file_extension: str) -> str:
        """根据文件扩展名获取 Content-Type"""
        content_type_map = {
            "mp4": "video/mp4",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "webp": "image/webp",
            "gif": "image/gif",
            "pdf": "application/pdf",
        }
        return content_type_map.get(file_extension.lower(), "application/octet-stream")
    
    async def upload_file(
        self, 
        file_content: bytes, 
        file_extension: str,
        sub_folder: str = "uploads"
    ) -> str:
        """
        上传文件到 OSS
        
        Args:
            file_content: 文件二进制内容
            file_extension: 文件扩展名（如 'jpg', 'mp4'）
            sub_folder: 子文件夹名称（默认 'uploads'）
        
        Returns:
            文件的公网访问 URL
        """
        filename = f"{sub_folder}/{uuid.uuid4()}.{file_extension}"
        
        # 设置文件元数据（Content-Type 和公共读权限）
        content_type = self._get_content_type(file_extension)
        headers = {
            'Content-Type': content_type,
            'x-oss-object-acl': 'public-read'  # 设置为公共读
        }
        
        self.bucket.put_object(filename, file_content, headers=headers)
        
        # 返回公网 URL
        url = f"https://{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}/{filename}"
        return url
    
    async def upload_file_from_url(
        self,
        file_url: str,
        file_extension: str,
        sub_folder: str = "uploads"
    ) -> str:
        """
        从网络 URL 下载文件并上传到 OSS
        
        Args:
            file_url: 网络文件 URL
            file_extension: 文件扩展名
            sub_folder: 子文件夹名称
        
        Returns:
            上传后的 OSS URL
        """
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.get(file_url)
            response.raise_for_status()
            return await self.upload_file(
                response.content,
                file_extension,
                sub_folder
            )
    
    def delete_file(self, file_url: str) -> bool:
        """删除 OSS 中的文件"""
        # 从 URL 中提取文件名
        filename = file_url.split(f"{settings.OSS_BUCKET_NAME}.{settings.OSS_ENDPOINT}/")[-1]
        try:
            self.bucket.delete_object(filename)
            return True
        except Exception:
            return False


# 全局单例
oss_service = OSSService()