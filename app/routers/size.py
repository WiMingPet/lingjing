"""
尺码推荐路由
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import tempfile
import os
from app.database import get_db
from app.schemas.task import APIResponse, TaskResponse
from app.services.size_service import SizeService
from app.models.user import User  # 新增导入

router = APIRouter(prefix="/size", tags=["尺码推荐"])


@router.post("/recommend", response_model=APIResponse)
async def recommend_size(
    image: UploadFile = File(...),
    height: Optional[float] = Form(170.0),
    db: Session = Depends(get_db),
):
    """
    尺码推荐

    - **image**: 全身照片（必填）
    - **height**: 身高（厘米），默认170
    """
    # 保存上传的图片到临时文件
    content = await image.read()
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
        f.write(content)
        image_path = f.name
    
    print(f"[DEBUG] 图片已保存: {image_path}")
    print(f"[DEBUG] 身高: {height}cm")
    
    try:
        user_id = 1
        
        # ========== 确保用户存在，如果不存在则自动创建 ==========
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id, username=f"user_{user_id}")
            db.add(user)
            db.commit()
            print(f"[DEBUG] 自动创建了用户: id={user.id}")
        # ========== 新增代码结束 ==========
        
        task = await SizeService.recommend_size(db, user_id, image_path, height)
        
        return APIResponse(
            code=200,
            message="尺码推荐任务已提交",
            data=TaskResponse.model_validate(task)
        )
    finally:
        # 清理临时文件
        if os.path.exists(image_path):
            try:
                os.unlink(image_path)
                print(f"[DEBUG] 临时文件已删除: {image_path}")
            except:
                pass


@router.get("/task/{task_id}", response_model=APIResponse)
def get_size_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    """获取尺码推荐任务状态"""
    task = SizeService.get_task_result(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return APIResponse(
        code=200,
        message="获取成功",
        data=TaskResponse.model_validate(task)
    )