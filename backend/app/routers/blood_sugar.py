"""血糖记录 API 路由。"""
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Query, HTTPException
from tortoise.expressions import Q
from app.core.health_analyzer import health_analyzer
from app.models.patient import Patient
from app.models.blood_sugar import BloodSugar
from app.schemas.blood_sugar import BloodSugarCreate, BloodSugarUpdate, BloodSugarResponse,BloodSugarStatsResponse

router = APIRouter(prefix="/blood-sugar", tags=["blood-sugar"])

# 创建血糖记录
@router.post("/", response_model=BloodSugarResponse)
async def create_record(data: BloodSugarCreate):
    await Patient.get_or_none(id=data.patient_id) # 检查患者是否存在
    record = await BloodSugar.create(**data.model_dump()) # 创建血糖记录

    return BloodSugarResponse(
        id=record.id,
        patient_id=record.patient_id,
        value=record.value,
        measure_type=record.measure_type,
        measured_at=record.measured_at,
        note=record.note,
        status=record.status,
        created_at=record.created_at
    )

# 获取患者血糖记录
# days: 查询最近多少天的记录，默认7天，范围1-90天
@router.get("/patient/{patient_id}", response_model=List[BloodSugarResponse])
async def get_records(patient_id: int, days:int = Query(7,ge=1,le=90)):
    await Patient.get_or_none(id=patient_id) # 检查患者是否存在
    # 获取指定天数内的血糖记录，从当前时间往前推
    since = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)
    
    records = await BloodSugar.filter(
        Q(patient_id=patient_id) & Q(measured_at__gte=since)
    ).order_by("-measured_at").all()

    return [
        BloodSugarResponse(
            id=record.id,
            patient_id=record.patient_id,
            value=record.value,
            measure_type=record.measure_type,
            measured_at=record.measured_at,
            note=record.note,
            status=record.status,
            created_at=record.created_at
        )
        for record in records
    ]

# 更新血糖记录
@router.put("/{record_id}", response_model=BloodSugarResponse)
async def update_record(record_id: int, data: BloodSugarUpdate):
    record = await BloodSugar.get_or_none(id=record_id) # 检查记录是否存在
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)

    # 写回数据库并重新加载数据
    await record.save()
    await record.refresh_from_db()

    return BloodSugarResponse(
        id=record.id,
        patient_id=record.patient_id,
        value=record.value,
        measure_type=record.measure_type,
        measured_at=record.measured_at,
        note=record.note,
        status=record.status,
        created_at=record.created_at
    )

# 删除血糖记录
@router.delete("/{record_id}")
async def delete_record(record_id: int):
    record = await BloodSugar.get_or_none(id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    await record.delete()
    return {"message": "记录删除成功"}

# 获取患者血糖统计
@router.get("/patient/{patient_id}/stats", response_model=BloodSugarStatsResponse)
async def get_stats(patient_id: int, days:int = Query(7,ge=1,le=90)):
    await Patient.get_or_none(id=patient_id) # 检查患者是否存在
    analysis = await health_analyzer.analyze_blood_sugar(patient_id,days)

    return BloodSugarStatsResponse(**analysis)