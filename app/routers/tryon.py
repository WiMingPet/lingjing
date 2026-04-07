"""
虚拟试穿路由
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.task import APIResponse, TaskResponse
from app.services.tryon_service import TryonService
from app.models.user import User  # 新增导入

router = APIRouter(prefix="/tryon", tags=["虚拟试穿"])


@router.post("/generate", response_model=APIResponse)
async def generate_tryon(
    model_image: UploadFile = File(...),
    garment_image: UploadFile = File(...),
    digital_human_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    """
    虚拟试穿

    - **model_image**: 模特图片（必填）
    - **garment_image**: 服装图片（必填）
    - **digital_human_id**: 数字人ID（可选）
    """
    # 临时使用公网测试图片（直接用你提供的亚马逊图片）
    model_image_url = "https://m.media-amazon.com/images/I/71jgn+xibhL._AC_SY550_.jpg"
    garment_image_url = "https://m.media-amazon.com/images/I/61OarLRya0L._AC_SY550_.jpg"
    
    print(f"[DEBUG] 使用模特图片URL: {model_image_url}")
    print(f"[DEBUG] 使用服装图片URL: {garment_image_url}")
    
    request_data = {
        "model_image_url": model_image_url,
        "garment_image_url": garment_image_url,
        "digital_human_id": digital_human_id
    }
    
    # 临时使用固定用户 ID 1
    user_id = 1
    
    # ========== 确保用户存在，如果不存在则自动创建 ==========
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, username=f"user_{user_id}", email=f"user_{user_id}@temp.com")
        db.add(user)
        db.commit()
        print(f"[DEBUG] 自动创建了用户: id={user.id}")
    # ========== 新增代码结束 ==========
    
    task = await TryonService.generate_tryon(db, user_id, request_data)
    
    return APIResponse(
        code=200,
        message="虚拟试穿任务已提交",
        data=TaskResponse.model_validate(task)
    )


@router.get("/task/{task_id}", response_model=APIResponse)
def get_tryon_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    """获取虚拟试穿任务状态"""
    task = TryonService.get_task_result(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return APIResponse(
        code=200,
        message="获取成功",
        data=TaskResponse.model_validate(task)
    )